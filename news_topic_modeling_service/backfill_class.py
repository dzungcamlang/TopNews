import os
import sys

# import packages from ../common dir
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client


NEWS_TABLE_NAME = '[top-news]'

'''
add classification for all unclassified news in the database
'''
if __name__ == '__main__':
    db = mongodb_client.get_db()
    cursor = db[NEWS_TABLE_NAME].find()
    print ('news in database: %d' % cursor.count())
    count_no_class = 0
    for news in cursor:
        if 'class' not in news:
            count_no_class += 1
            text = news['title']
            description = news['description']
            if (description is not None):
                text = text + ' ' + description
            topic = news_topic_modeling_service_client.classify(text)
            news['class'] = topic
            db[NEWS_TABLE_NAME].replace_one({'digest': news['digest']}, news)

            if (count_no_class % 100 == 0):
                print ('labelled %d news' % count_no_class)
            # verify update success
            '''
            test_obj = db['top-news'].find_one({'digest': news['digest']})
            print ('digest: %s' % test_obj['digest'])
            print ('classified topic: %s' % test_obj['class'])
            '''

    print ('news classified: %d' % count_no_class)
