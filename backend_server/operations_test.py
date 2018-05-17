import operations

def test_getOneNews_basic():
    news = operations.getOneNews()
    print (news)
    assert news is not None
    print ("test_getOneNews_basic passed")

def test_getNewsCount_basic():
    count = operations.getNewsCount()
    print ('count', count)
    assert count > 0
    print ("test_getNewsCount_basic passed")

def test_getNewsSummariesForUser_basic():
    news_list = operations.getNewsSummariesForUser('test_user', 1)
    print ('first page has %d news' % len(news_list))
    for news_entry in news_list:
        print (news_entry['description'])
    assert len(news_list) > 0
    print ("test_getNewsSummariesForUser_basic passed")

def test_getNewsSummariesForUser_pagination():
    news_page_1 = operations.getNewsSummariesForUser('test_user', 1)
    news_page_2 = operations.getNewsSummariesForUser('test_user', 2)

    assert len(news_page_1) > 0
    assert len(news_page_2) > 0

    # test if news on page 1 overlap with those on page 2
    digest_set_page_1 = set([news['digest'] for news in news_page_1])
    digest_set_page_2 = set([news['digest'] for news in news_page_2])

    for digest in digest_set_page_1:
        print (digest)
    assert len(digest_set_page_1.intersection(digest_set_page_2)) == 0
    assert len(digest_set_page_1.union(digest_set_page_2)) == len(digest_set_page_1) + len(digest_set_page_2)

    print ('test_getNewsSummariesForUser_pagination passed')

if __name__ == '__main__':
    test_getOneNews_basic()
    test_getNewsCount_basic()
    test_getNewsSummariesForUser_basic()
