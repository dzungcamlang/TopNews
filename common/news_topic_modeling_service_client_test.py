import news_topic_modeling_service_client as client

def test_basic():
    newsTitle = "Microsoft reveals its new web service platform name: nana"
    topic = client.classify(newsTitle)
    assert topic == "U.S."
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
