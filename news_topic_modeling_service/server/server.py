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

N_CLASSES = 9

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_processor_save_file'

MAX_DOCUMENT_LENGTH = 500

# global variables
n_words = 0
vocab_processor = None
classfier = None

def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)
        print ('number of words %d' % n_words)

    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE)


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


restoreVars()
loadModel()

print("Initial model loaded")




# monitor change in the ../model dir, reload mod on change

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # reload model
        print('Model update detected, reload new model')
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        restoreVars()
        loadModel()


observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()


# RPC call, classify a list of news, return a list of topics
def classify(text):
    text_series = pd.Series([text])
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_x)

    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]
    print(y_predicted[0])

    topic = news_classes.class_map[str(y_predicted[0])]
    return topic

# set up RPC server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')
print ('Starting RPC server on %s:%d' % (SERVER_HOST, SERVER_PORT))
RPC_SERVER.serve_forever()
