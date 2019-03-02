'''
Article Module for Article Class
'''

COLOR_TITLE = '\033[1;32;40m'
COLOR_AUTHOR = '\033[1;31;40m'
COLOR_NORMAL = '\033[1;37;0m'
COLOR_DATE = '\033[1;33;40m'
COLOR_HREF = '\033[1;34;40m'


class Article(object):
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title', '')
        self.summary = kwargs.get('summary', '')
        self.authors = kwargs.get('authors', [])
        self.submitted_date = kwargs.get('submitted_date', 'N/A')
        self.tags = kwargs.get('tags', [])
        self.link = kwargs.get('link', 'N/A')
        self.weight = kwargs.get('weight', 0)

    def __str__(self):
        return "{}{}{} < {}{}{}: {}{}{} >\n{}\nhref: {}{}{}".format(
            COLOR_TITLE, self.title, COLOR_NORMAL, COLOR_AUTHOR, self.author, COLOR_NORMAL,
            COLOR_DATE, self.date, COLOR_NORMAL, self.summary, COLOR_HREF, self.href, COLOR_NORMAL)

    @property
    def author(self):
        return self.authors[0] if self.authors else 'N/A'

    @property
    def date(self):
        return self.submitted_date if self.submitted_date else 'N/A'

    @property
    def href(self):
        return self.link if self.link else 'N/A'
