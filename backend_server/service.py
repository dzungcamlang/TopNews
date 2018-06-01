# Entry point of backend RPC server

import operations
import os
import sys

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

# setting python to import packages from utils directory
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import mongodb_client

''' HOLD

# AMQP for logging user click event, connection is established here to keep it alive
from cloudAMQP_client import CloudAMQPClient
USER_CLICK_LOG_QUEUE_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
USER_CLICK_LOG_QUEUE_NAME = 'UserClickLogQueue'
cloudAMQP_client = CloudAMQPClient(USER_CLICK_LOG_QUEUE_URL, USER_CLICK_LOG_QUEUE_NAME)

'''

# define methods
def add(num1, num2):
    print ("add is called with %d and %d" % (num1, num2))
    return num1 + num2

def getOneNews():
    print ("getOneNews is called")
    return operations.getOneNews()

''' get paginated news summary for a user '''
def getNewsSummariesForUser(user_id, page_num):
    print ("get news summaries for user: %s, page %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)

''' log a news-click event for a user '''
def logNewsClickForUser(user_id, news_id):
    print ("log click event for user %s, on news id %s" % (user_id, news_id))
    return operations.logNewsClickForUser(user_id, news_id)


# setup server and register methods
# second param is the method name exposed by server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(getOneNews, 'getOneNews')
RPC_SERVER.register_function(getNewsSummariesForUser, 'getNewsSummariesForUser')
RPC_SERVER.register_function(logNewsClickForUser, 'logNewsClickForUser')


# start up server
print ("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT))
RPC_SERVER.serve_forever()
