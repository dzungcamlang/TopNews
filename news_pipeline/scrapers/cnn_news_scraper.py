# scrape news body from a specific source website
# FOR VERIFYING XPATH ONLY, actual scraper is located in news_fetcher.py
import os
import random
import requests

from lxml import html

GET_CNN_NEWS_XPATH = """//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"""

# load user agents
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

# create a collection of user agents in random order
with open(USER_AGENTS_FILE, 'rb') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

# generate an HTTP request header
def _get_headers():
    ua = random.choice(USER_AGENTS)
    headers = {
        'Connection': 'close',
        'User-Agent': ua
    }
    return headers


def extract_news(news_url):
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=_get_headers())
    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ' '.join(news) # join paragraphs
    except Exception:
        return {}

    return news
