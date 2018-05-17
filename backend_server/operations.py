import json
import os
import pickle # store python obj to db
import pymongo
import redis
import sys

from bson.json_util import dumps
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TABLE_NAME = '[top-news]' # table name in MongoDb
PAGE_SIZE = 10
NEWS_LIMIT = 100
USER_NEWS_TIME_OUT_IN_SECONDS = 60 # timeout for user's pagination info in Redis

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    # bson.json_util.dumps transform bson to serialized string
    # unserialize string and return json object
    return json.loads(dumps(news))

def getNewsCount():
    db = mongodb_client.get_db()
    count = db[NEWS_TABLE_NAME].count()
    return count

'''
    get paginated news summaries for user
    pagination info is stored in cache
    news are stored in database
    page_num: 1 based page
'''
def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * PAGE_SIZE # inclusive
    end_index = page_num * PAGE_SIZE # exclusive
    sliced_news = []

    # read news digest of next page from cache, then read news from db
    # if no more news in the cache, write next batch of news digests into cache
    if redis_client.get(user_id) is not None:
        # read python obj from db and de-serialize
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index:end_index]
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        batch_news = list(db[NEWS_TABLE_NAME].find().sort('publishedAt', pymongo.DESCENDING).limit(NEWS_LIMIT))
        batch_news_digest = [news['digest'] for news in batch_news]

        redis_client.set(user_id, pickle.dumps(batch_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = batch_news[begin_index:end_index]

    for news in sliced_news:
        # remove text field to save bandwidth (text doesn't display on client)
        del news['text']
        # for fresh news, add a tag to display
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'


    return json.loads(dumps(sliced_news))
