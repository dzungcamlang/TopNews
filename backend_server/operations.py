import json
import os
import sys

from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

NEWS_TABLE_NAME = 'news'

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
