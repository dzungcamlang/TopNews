# read messages from 2nd AMQP, filter duplication, store news to mongodb

import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

# 2nd AMQP that stores news with body text, may contain duplicate news
DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'TopNewsQueue'

SLEEP_TIME_IN_SECONDS = 1
# news table in mongodb
NEWS_TABLE_NAME = '[top-news]'

# two entries of news are considered duplicate if tf-idf score >= 0.9
SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

# dudupe messages with other news published within 24 hours' span
def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg
    text = task['text']
    if text is None:
        print('bad message -- no body')
        return

    # get news that were published within 24 hours
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)
    published_at_day_begin = published_at_day_begin - datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    check_news_list = list(db[NEWS_TABLE_NAME].find(
                {'publishedAt': {
                '$gte': published_at_day_begin, '$lt': published_at_day_end}}))
    # check duplicity
    if check_news_list is not None and len(check_news_list) > 0:
        # build documents vector (each doc is a news body)
        documents = [news['text'] for news in check_news_list]
        documents.insert(0, text) # insert self at beginning

        # build tf-idf matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        similarity_matrix = tfidf * tfidf.T

        # print(similarity_matrix)

        rows, _ = similarity_matrix.shape
        # throw away this news if it is similar to another news in the queue
        for row in range(1, rows):
            if similarity_matrix[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print('Duplicated news, ignore')
                return

    # not duplicate, store news to mongodb
    # transform datetime to mongodb datetime format
    task['publishedAt'] = parser.parse(task['publishedAt'])
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)


def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()
