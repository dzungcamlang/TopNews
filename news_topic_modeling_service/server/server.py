import news_classes
import numpy as np
import os
import pandas as pd
import pickle
import sys
import tensorflow as tf
import time

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from tensorflow.contrib import predictor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# import packages in ../trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
import news_cnn_model

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = 10

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_processor_save_file'
EXPORT_DIR_FILE = '../model/export_dir'
MAX_DOCUMENT_LENGTH = 200

EXPORT_DIR = '../model/0607_3100'
# global variables
n_words = 0
vocab_processor = None
classfier = None
export_dir = None

# load vocab processor and num of words
def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)
        print ('number of words %d' % n_words)

    with open(EXPORT_DIR_FILE, 'rb') as f:
        global export_dir
        export_dir = pickle.load(f)
        print ('load model from %s' % export_dir)

    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE)

'''
def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)
    df = pd.read_csv('../data/labeled_news.csv', header=None)

    # train model at least once for restored Estimator to work
    train_df = df[0:1900]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)
    print('ML Model updated')
'''

restoreVars()
# loadModel()

print("Initial model loaded")




# monitor change in the ../model dir, reload mod on change

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # reload model
        print('Model update detected, reload new model')
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        restoreVars()
        # loadModel()


observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()


# RPC request, input a piece if news, return a classified topic
def classify(text):

    text_series = pd.Series([text])
    predict_x = np.array(list(vocab_processor.transform(text_series))).flatten()
    print(predict_x)
    print (predict_x.shape)
    with tf.Session() as sess:
        tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], export_dir)
        predict_fn = predictor.from_saved_model(export_dir)
        model_input = tf.train.Example(features=tf.train.Features(
            feature={'words': tf.train.Feature(
                int64_list=tf.train.Int64List(value=predict_x)
            )}
        ))
        model_input = model_input.SerializeToString()
        output_dict = predict_fn({'predictor_inputs':[model_input]})
        predicted_class = output_dict['class'][0]
        print (predicted_class)
        topic = news_classes.class_map[str(predicted_class)]
        return topic
    '''
    text_series = pd.Series([text])
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_x)
    print (predict_x.shape)
    predict_fn = predictor.from_saved_model(export_dir)

    model_input = tf.train.Example(features=tf.train.Features(
        feature={'words': tf.train.Feature(
            int64_list=tf.train.Int64List(value=predict_x)
        )}
    ))
    model_input = model_input.SerializeToString()
    predicted_class = predict_fn({'predictor_inputs':[model_input]})

    print(predicted_class)

    topic = news_classes.class_map[str(y_predicted['class'])]
    return topic
    '''
# set up RPC server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')
print ('Starting RPC server on %s:%d' % (SERVER_HOST, SERVER_PORT))
RPC_SERVER.serve_forever()
