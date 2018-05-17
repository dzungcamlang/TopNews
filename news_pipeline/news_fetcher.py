# Read news from AMQP, scrape source website, fetch and add news body to next AMQP

import os
import sys

# newspaper3k, need to downgrade html5lib to 1.0b8
from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

# 1st AMQP, stores news digest and url to scrape news body from
SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'TopNewsTitleQueue'
# 2nd AMQP, stores news body for news deduper to consume
DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'TopNewsQueue'

# interval between two processes
SLEEP_TIME_IN_SECONDS = 5
# put both queues to sleep in turn for a certain times
# total pause time (when no msg in Q) 2 * 45 * 10 = 900
PAUSE_INTERVAL_IN_EACH_LOOP = 45
LOOPS = 10

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

# process msg: attach text field (news body), then push it to next AMQP
def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)

# read and process message from AMQP
def run():
    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
                # control scraping pace is important to avoid blocking
                scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
            # pause for an interval if upstreaming queue is empty
            else:
                for i in range(LOOPS):
                    scrape_news_queue_client.sleep(PAUSE_INTERVAL_IN_EACH_LOOP)
                    dedupe_news_queue_client.sleep(PAUSE_INTERVAL_IN_EACH_LOOP)


if __name__ == '__main__':
    run()
