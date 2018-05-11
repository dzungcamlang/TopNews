import requests

from json import loads

# v2 is not stable, we use v1
NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = 'f94a31e3d77144f7b4c1109125f97c15'

ARTICLES_API = 'articles'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]
SORT_BY_TOP = 'top'

def _buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=ARTICLES_API):
    return endPoint + apiName

def getNewsFromSources(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):

    # each article schema:
    # digest: MD5 hash of news title(primary key)
    # title, description, text, url, author
    # source (manually create)
    # publishedAt, urlToImage, class
    articles = []

    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }
        # get News and deserialize
        response = requests.get(_buildUrl(), params=payload)
        res_json = loads(response.content.decode('utf-8'))

        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # source has to be manually added
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles
