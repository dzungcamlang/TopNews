import news_cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from sklearn import metrics

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = '../model/'
DATA_SET_FILE = '../data/labeled_news.csv'
VARS_FILE = '../model/vars'
EXPORT_DIR_FILE = '../model/export_dir'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_processor_save_file'
MAX_DOCUMENT_LENGTH = 200
N_CLASSES = 10
WORDS_FEATURE = 'words'  # Name of the input words feature.

'''
News Classes:
1. Entertainment
2. Lifestyle
3. Market
4. Business
5. Politics
6. Sports
7. Technology
8. U.S.
9. World
'''

# Training parms
STEPS = 1500
BATCH_SIZE = 4 # non-GPU setting

# for estimator export
def serving_input_receiver_fn():
    serialized_tf_example = tf.placeholder(dtype=tf.string, shape=[None], name='input_tensors')
    receiver_tensors = {'predictor_inputs': serialized_tf_example}
    feature_spec = {'words': tf.FixedLenFeature([MAX_DOCUMENT_LENGTH], tf.int64)}
    features = tf.parse_example(serialized_tf_example, feature_spec)
    return tf.estimator.export.ServingInputReceiver(
        features, receiver_tensors)


def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Prepare training and testing data
    df = pd.read_csv(DATA_SET_FILE, header=None)
    # df = df.sample(frac=1).reset_index(drop=True)
    train_df = df[0:1800]
    test_df = df.drop(train_df.index)


    # x - news title + source, y - class
    x_train = train_df[1] + ' ' + train_df[3].astype(str).map(str.strip)
    y_train = train_df[0]
    x_test = test_df[1] + ' ' + test_df[3].astype(str).map(str.strip)
    y_test = list(test_df[0])

    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))


    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    # Saving n_words and vocab_processor for serving:
    with open(VARS_FILE, 'wb') as f:  # needs to be opened in binary mode.
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    '''
    Version 2
    '''

    # Build model
    model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words)
    classifier = tf.estimator.Estimator(model_fn=model_fn)
    # Train
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={WORDS_FEATURE: x_train},
      y=y_train,
      batch_size=BATCH_SIZE,
      num_epochs=None,
      shuffle=True)
    classifier.train(input_fn=train_input_fn, steps=STEPS)

    # Predict
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={WORDS_FEATURE: x_test},
        num_epochs=1,
        shuffle=False
    )
    y_predicted = list(classifier.predict(input_fn=predict_input_fn))
    predicted_classes = [p['class'] for p in y_predicted]

    # Evaluate w/o 'sports'
    for i in range(30):
        print (predicted_classes[i])
    count = 0
    sports = 0
    for i in range(len(predicted_classes)):
        if (y_test[i] == 6):
            sports += 1
            continue
        if (predicted_classes[i] == y_test[i]):
            count += 1
    total = len(predicted_classes) - sports
    print ('Augmented Accuracy: {0:f}'.format(float(count) / total))

    # Evaluate.
    test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={WORDS_FEATURE: x_test},
      y=np.array(y_test),
      num_epochs=1,
      shuffle=False)
    scores = classifier.evaluate(input_fn=test_input_fn)
    print('Overall Accuracy: {0:f}'.format(scores['accuracy']))

    # Export
    export_dir = classifier.export_savedmodel(
        MODEL_OUTPUT_DIR, serving_input_receiver_fn)

    print ('Model exported to %s' % export_dir)
    with open(EXPORT_DIR_FILE, 'wb') as f:  # needs to be opened in binary mode.
        pickle.dump(export_dir, f)

    '''
    Version 1
    '''
    '''
    # Build model
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Train and predict
    classifier.fit(x_train, y_train, steps=STEPS, batch_size=BATCH_SIZE)

    # Evaluate model
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    for i in range(40):
        print (y_predicted[i])

    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))
    '''

if __name__ == '__main__':
    tf.app.run(main=main)
