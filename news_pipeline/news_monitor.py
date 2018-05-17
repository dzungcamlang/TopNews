# monitor news source and fetch news metadata into first AMQP
# store news digest in Redis to avoid fetching same news multiple times
# powered by NewsAPI.org

import datetime
import hashlib
import os
import sys
import redis

# add system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'business-insider',
    'buzzfeed',
    'cnbc',
    'cnn',
    'entertainment-weekly',
    'espn',
    'focus',
    'fortune',
    'ign',
    'polygon',
    'techcrunch'
    'the-economist',
    'the-huffington-post',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post',
    'wired'
]

# loop all news sources every X seconds
SLEEP_TIME_IN_SECONDS = 900
# news expiration time set to Y days
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# The first AMQP that scores news digest and url to be scraped
SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'TopNewsTitleQueue'

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

# fetch news from NEWS_SOURCES every 60 seconds
def run():
    while True:
        news_list = news_api_client.getNewsFromSources(NEWS_SOURCES)
        num_of_new_news = 0
        # for each news, check duplicity, if pass, send news to AMQP
        for news in news_list:
            # news_digest is primary key of each news (for checking duplicity)
            news_digest = hashlib.md5(news['description'].encode('utf-8')).hexdigest()

            if redis_client.get(news_digest) is None:
                num_of_new_news = num_of_new_news + 1
                news['digest'] = news_digest

                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

                redis_client.set(news_digest, 'True')
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

                cloudAMQP_client.sendMessage(news)

        print('--------------------')
        print('Fetched %d news sources' % num_of_new_news)

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()
