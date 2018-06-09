import tensorflow as tf

EMBEDDING_SIZE = 40
N_FILTERS = 64
WINDOW_SIZE = 20
FILTER_SHAPE1 = [WINDOW_SIZE, EMBEDDING_SIZE]
FILTER_SHAPE2 = [WINDOW_SIZE, N_FILTERS]
POOLING_WINDOW = 4
POOLING_STRIDE = 2

LEARNING_RATE = 0.01

def generate_cnn_model(n_classes, n_words):
    """2 layer ConvNet to predict from sequence of words to a class."""
    def cnn_model(features, labels, mode):
      # Convert indexes of words into embeddings.
      # This creates embeddings matrix of [n_words, EMBEDDING_SIZE] and then
      # maps word indexes of the sequence into [batch_size, sequence_length,
      # EMBEDDING_SIZE].
      # labels = tf.one_hot(labels, n_classes, 1, 0)
      word_vectors = tf.contrib.layers.embed_sequence(
          features['words'], vocab_size=n_words, embed_dim=EMBEDDING_SIZE)
      word_vectors = tf.expand_dims(word_vectors, 3)
      with tf.variable_scope('CNN_layer1'):
        # Apply Convolution filtering on input sequence.
        conv1 = tf.layers.conv2d(
            word_vectors,
            filters=N_FILTERS,
            kernel_size=FILTER_SHAPE1,
            padding='VALID',
            # Add a ReLU for non linearity
            activation=tf.nn.relu)
        # Max pooling across output of Convolution+Relu.
        pool1 = tf.layers.max_pooling2d(
            conv1,
            pool_size=POOLING_WINDOW,
            strides=POOLING_STRIDE,
            padding='SAME')
        # Transpose matrix so that n_filters from convolution becomes width.
        pool1 = tf.transpose(pool1, [0, 1, 3, 2])
      with tf.variable_scope('CNN_layer2'):
        # Second level of convolution filtering.
        conv2 = tf.layers.conv2d(
            pool1,
            filters=N_FILTERS,
            kernel_size=FILTER_SHAPE2,
            padding='VALID')
        # Max across each filter to get useful features for classification.
        pool2 = tf.squeeze(tf.reduce_max(conv2, 1), axis=[1])

      # Apply regular WX + B and classification.
      logits = tf.layers.dense(pool2, n_classes, activation=None)

      # Mode : predict
      predicted_classes = tf.argmax(logits, 1)
      if mode == tf.estimator.ModeKeys.PREDICT:
          return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={
                'class': predicted_classes,
                'prob': tf.nn.softmax(logits)
            },
            # Describe the output signatures to be exported to savedmodel
            export_outputs={'predict_output': tf.estimator.export.PredictOutput({
                'class': predicted_classes,
                'prob': tf.nn.softmax(logits)
            })})

      # Mode: train
      loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
      if mode == tf.estimator.ModeKeys.TRAIN:
          optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE)
          train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
          return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)

      # Mode: Evaluate
      eval_metric_ops = {
        'accuracy': tf.metrics.accuracy(
            labels=labels,
            predictions=predicted_classes
        )
      }
      return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


    return cnn_model
