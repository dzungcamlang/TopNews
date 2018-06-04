'''
RPC server that provides service of reading user prefrence
'''

import operator # for sorting key
import os
import sys

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
# import packages from ../common
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

USER_PREFERENCE_TABLE_NAME = '[user-preference]'

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

'''
compare two floats for alomost equality

ref: https://www.python.org/dev/peps/pep-0485/#proposed-implementation
'''
def isClose(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

'''
get user prefrence model in an ordered list
from classes with most weight to least weight
'''
def getPreferenceForUser(user_id):
    db = mongodb_client.get_db()
    model = db[USER_PREFERENCE_TABLE_NAME].find_one({'user_id': user_id})

    if model is None:
        return []
    # get a list of sorted classes/weights
    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_class_list = [x[0] for x in sorted_tuples]
    sorted_weight_list = [x[1] for x in sorted_tuples]

    # check if the weights are uniformly distributed (non-preference user model)
    if isClose(float(sorted_weight_list[0]), float(sorted_weight_list[-1])):
        return []

    return sorted_class_list

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')

print ('Starting RPC server on %s:%s' % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
