# test if scrpaer works for the specific website(CNN)
import cnn_news_scraper as scraper

EXPECTED_NEWS = "Steve Rossi, the lead Florida attorney representing the defendant"
CNN_NEWS_URL = "https://www.cnn.com/2018/05/11/politics/rudy-giuliani-florida-court-case/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    print(news)
    assert EXPECTED_NEWS in news
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()
