from pymongo import MongoClient

MONGO_DB_HOST = 'localhost'
MONGO_DB_PORT = '27017'
DB_NAME = '[top-news]'

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

# Get database, top-new by default
def get_db(db=DB_NAME):
    db = client[db]
    return db
