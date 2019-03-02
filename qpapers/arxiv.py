import requests
import re

from bs4 import BeautifulSoup

from .article import Article


class ArxivDateFilter(object):
    DATE_FILTER_ALL = 'all_dates'
    DATE_FILTER_PAST_12_MONTHS = 'past_12'
    DATE_FILTER_SPECIFIC_YEAR = 'specific_year'
    DATE_FILTER_DATE_RANGE = 'date_range'
    DATE_YEAR = ''
    DATE_FROM_DATE = ''
    DATE_TO_DATE = ''

    SUBMITTED_DATE = 'submitted_date'
    SUBMITTED_DATE_ORIGINAL = 'submitted_date_first'
    ANNOUNCED_DATE = 'announced_date_first'

    def __init__(self):
        self.date_filter_by = self.DATE_FILTER_ALL
        self.filter_sa = self.SUBMITTED_DATE
        self.year = ''
        self.from_date = ''
        self.to_date = ''

    @property
    def fields(self):
        res = {
            'date-filter_by': self.date_filter_by,
        }
        if self.date_filter_by == self.DATE_FILTER_SPECIFIC_YEAR:
            res.update({
                'year': self.year,
            })
            return res
        elif self.date_filter_by == self.DATE_FILTER_DATE_RANGE:
            res.update({
                'from_date': self.from_date,
                'to_date': self.to_date,
            })

        return res


class ArxivAdvanceSearch(object):
    ORDER_ANNOUNCED_DATE_FIRST = 'announced_date_first'
    ORDER_ANNOUNCED_DATE_LAST = '-%s' % ORDER_ANNOUNCED_DATE_FIRST
    ORDER_SUBMITTED_DATE_FIRST = 'announced_date_first'
    ORDER_SUBMITTED_DATE_LAST = '-%s' % ORDER_ANNOUNCED_DATE_FIRST
    CLASSIFICATION_INCLUDE_CROSS_LIST = 'include'
    CLASSIFICATION_EXCLUDE_CROSS_LIST = 'exclude'

    CONFIG = {
        'CLASSIFICATION_COMPUTER_SCIENCE': 'y',
        'CLASSIFICATION_PHYSICS_ARCHIVED': 'all',
    }

    DATE_FILTER_YEAR = 'year'

    def __init__(self, *args, **kwargs):
        self.url = 'https://arxiv.org/search/advanced'

        self.date_filter = ArxivDateFilter()
        self.term = kwargs.get('keyword', '')
        self.term_field = kwargs.get('field', 'title')
        self.classification_cs = self.CONFIG.get(
            'CLASSIFICATION_COMPUTER_SCIENCE')
        self.classification_physics = self.CONFIG.get(
            'CLASSIFICATION_PHYSICS_ARCHIVED')
        self.order_by = self.ORDER_SUBMITTED_DATE_LAST
        self.classification_include_cross_list = True
        self.show_abstracts = 'show'
        self.arxiv_size = 200
        self.page = 0
        self.show = 7

    @property
    def params(self):
        params = {
            'advanced': '',
            'terms-0-term': self.term,
            'terms-0-field': self.term_field,
            'classification-computer_science': self.classification_cs,
            'classification-physics_archives': self.classification_physics,
            'classification-include_cross_list': 'include' if self.classification_include_cross_list else 'exclude',
            'abstracts': self.show_abstracts,
            'size': self.arxiv_size,
            'start': self.page * self.arxiv_size,
            'order': self.order_by
        }
        params.update(self.date_filter.fields)
        return params

    def set_keyword(self, keyword):
        self.term = keyword

    def search(self):
        return requests.get(self.url, params=self.params)

    def get_articles(self):
        response = self.search()

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []

        for result in soup.find_all('li', attrs={'class': 'arxiv-result'}):
            href = '#'
            for link in result.find_all('a'):
                href = link.get('href', '').strip()
                if href:
                    break
            # print('href: ', href)

            title = result.find('p', attrs={'class': 'title'}).text.strip()
            # print('title: ', title)

            top_tags_elem = result.find('div', attrs={'class': 'tags'})
            # print('top_tags_elem: ', top_tags_elem)
            tags = []

            for tag_elem in top_tags_elem.find_all('span', attrs={'class': 'tag'}):
                tag = tag_elem.get('data-tooltip')
                if tag:
                    tags.append(tag)

            # print('tags: ', tags)

            authors = []
            authors_top_elem = result.find('p', attrs={'class': 'authors'})

            for author_elem in authors_top_elem.find_all('a'):
                authors.append(author_elem.text)
            # print('authors: ', authors)

            abstract = result.find(
                'span', attrs={'class': 'abstract-full'}).text

            count = 0
            all_search_hit = result.find_all(
                'span', attrs={'class': 'search-hit'})
            count = len(all_search_hit)

            # print('count: ', count)

            abstract = abstract[:len(abstract) - abstract[::-1].find('.')]

            # print('abstract:', abstract)
            submitted = 'N/A'

            for span_elem in result.find_all('span'):
                if span_elem.text.lower() == 'submitted':
                    parent_text = span_elem.find_parent('p').text
                    parent_text = parent_text.replace('\n', ' ')
                    search = re.search(
                        r'Submitted (\d+ \w+, \d+)', parent_text)
                    submitted = search.groups(
                        0)[0] if search.groups(0) else 'N/A'

            if title and abstract and authors and submitted:
                # print(title, abstract, authors, submitted, tags, href)
                article = Article(
                    title=title, summary=abstract.strip(), authors=authors,
                    submitted_date=submitted, tags=tags, link=href, count=count)
                articles.append(article)

        return list(sorted(articles, key=lambda a: a.weight, reverse=True))[:self.show]


if __name__ == '__main__':
    aaf = ArxivAdvanceSearch(keyword='Machine Learning')

    aaf.search()
