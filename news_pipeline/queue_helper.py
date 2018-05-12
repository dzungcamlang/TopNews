# remove messages from a queue, for convinience of development

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'TopNewsTitleQueue'

def clearQueue(queue_url, queue_name):
    scrape_news_queue_client = CloudAMQPClient(queue_url, queue_name)

    num_of_messages = 0

    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is None:
                print ('Cleared queue with %d messages' % num_of_messages)
                return
            num_of_messages = num_of_messages + 1


if __name__ == '__main__':
    clearQueue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
