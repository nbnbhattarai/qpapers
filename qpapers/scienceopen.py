import requests
import json
from datetime import datetime

from .article import Article


class ScienceOpenSearch(object):
    NAME = 'SCIENCEOPEN'
    ROOT_URL = 'https://www.scienceopen.com'

    def __init__(self, *args, **kwargs):
        self.url = self.ROOT_URL + '/search-servlet'
        self.keyword = kwargs.get('keyword', '')
        self.page = 0
        self.result = 5

    def set_keyword(self, keyword):
        self.keyword = keyword

    def set_results(self, results):
        self.result = results

    @property
    def params(self):
        filters = [
            {
                'kind': 48,
                'query': self.keyword,
            },
            {
                'kind': 39,
                'disciplines': [
                    {
                        'kind': 23,
                        'id': '79f00046-6f95-11e2-bcfd-0800200c9a66',
                    },
                ]
            },
            {
                'kind': 46,
                'record': False,
                'abstract': True,
                'authorSummary': True,
                'article': True,
            }
        ]

        params = {
            'kind': 61,
            'itemsToGet': self.result,
            'firstItemIndex': self.page * self.result,
            'getFacets': False,
            'getFilters': False,
            'search': {
                'v': 3,
                'id': '',
                'isExactMatch': True,
                'context': None,
                'kind': 77,
                'order': 3,
                'orderLowestFirst': False,
                'query': '',
                'filters': filters,
            }
        }

        return {
            'q': json.dumps(params)
        }

    def search(self):
        return requests.get(self.url, params=self.params)

    def get_articles(self):
        response = self.search()
        response_json = response.json()
        # print('response: ', response_json)

        articles = []
        for result in response_json.get('result', {'results': []}).get('results', []):
            title = ' '.join(result.get('_titleSafe', '').replace(
                '\n', ' ').strip().split())
            abstract = ' '.join(result.get('_abstractTextSafe',
                                           '').replace('\n', ' ').strip().split())
            authors = result.get('_authors', [])
            authors = [author.get('_displayNameSafe') for author in authors]
            _date = result.get('_date', 0)
            _date = datetime.utcfromtimestamp(_date//1000)
            submitted_date = _date.strftime('%d %B, %Y')
            href = self.ROOT_URL + result.get('_url')

            article = Article(
                title=title, summary=abstract, authors=authors,
                submitted_date=submitted_date, link=href, source=self.NAME)

            articles.append(article)

        return articles


if __name__ == '__main__':
    sos = ScienceOpenSearch()
    sos.set_keyword('Machine Learning')
    sos.get_articles()
