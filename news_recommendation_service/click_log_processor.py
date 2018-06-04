'''
service which consumes user-click log in AMQP and generate user preference model
user preference model has:
    userId
    prefrence: dict of news_class and weight
'''
import os
import sys

import news_classes

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

'''
time decay model: initially each class has a weight p = 1 / NUM_CLASSES

after one click, clicked class has weight (1-a)p + a
other classes has weight (1-a)p

the total weight maintains as invariant of 1
'''
NUM_OF_CLASSES = 9
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.2 # set to a bigger value in test mode

USER_PREFERENCE_TABLE_NAME = '[user-preference]'
NEWS_TABLE_NAME = '[top-news]'

USER_CLICK_LOG_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
USER_CLICK_LOG_QUEUE_NAME = 'UserClickLogQueue'

SLEEP_TIME_IN_SECONDS = 1

cloudAMQP_client = CloudAMQPClient(USER_CLICK_LOG_QUEUE_URL, USER_CLICK_LOG_QUEUE_NAME)


'''
read a user-click log from AMQP
update/create user preference model in mongoDB
'''
def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print ('[User Preference Model] Message is broken')
        return
    if ('userId' not in msg or 'newsId' not in msg or 'timestamp' not in msg):
        print (msg)
        print ('[User Preference Model] Unauthenticated Access')
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # fetch user prefrence model
    db = mongodb_client.get_db()
    model = db[USER_PREFERENCE_TABLE_NAME].find_one({'userId': userId})

    # create a new user preference model if not exist
    if model is None:
        print ('[User Preference Model] Creating model for %s' % userId)
        new_model = {'userId': userId}
        prefrence = {}
        for i in news_classes.classes:
            prefrence[i] = float(INITIAL_P)
        new_model['preference'] = prefrence
        model = new_model

    # update a current user preference model
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None or 'class' not in news or news['class'] not in news_classes.classes):
        print ('[User Preference Model] Invalid news class, skip processing...')
        return
    clicked_class = news['class']
    old_p = model['preference']['clicked_class']
    model['preference']['clicked_class'] = float( (1 - ALPHA) * old_p + ALPHA )

    for i, prob in model['preference'].items():
        if not i == clicked_class:
            model['preference'][i] = float( (1 - ALPHA) * model['preference'][i] )

    # create/update user pref model in DB
    db[USER_PREFERENCE_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)


def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print ('[User Preference] Exception raised in handle_message as below:')
                    print (e)
                    pass
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()
