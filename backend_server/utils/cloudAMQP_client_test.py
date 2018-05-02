from cloudAMQP_client import CloudAMQPClient

TEST_CLOUDAMQP_URL = 'amqp://xhzhqriu:vo45Xa-LVUGTGeolrsXo1Rg_8eK3v1Ry@otter.rmq.cloudamqp.com/xhzhqriu'
TEST_QUEUE_NAME = 'TopNewsQueue'

def test_cloudamqp_client():
    client = CloudAMQPClient(TEST_CLOUDAMQP_URL, TEST_QUEUE_NAME)

    test_message = {'test': '123test'}
    client.sendMessage(test_message)
    # client.sendMessage(test_message)
    receieved_message = client.getMessage()
    assert test_message == receieved_message
    print ("AMQP client test passed")

if __name__ == '__main__':
    test_cloudamqp_client()
