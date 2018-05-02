import operations

def test_getOneNews_basic():
    news = operations.getOneNews()
    print (news)
    assert news is not None
    print ("test_getOneNews_basic passed")

def test_getNewsCount_basic():
    count = operations.getNewsCount()
    print ('count', count)
    assert count == 4
    print ("test_getNewsCount_basic passed")

if __name__ == '__main__':
    test_getOneNews_basic()
    test_getNewsCount_basic()
