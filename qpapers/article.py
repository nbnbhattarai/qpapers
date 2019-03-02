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
        self.source = kwargs.get('source')
        self.title = kwargs.get('title', '')
        self.summary = kwargs.get('summary', '')
        self.authors = kwargs.get('authors', [])
        self.submitted_date = kwargs.get('submitted_date', 'N/A')
        self.tags = kwargs.get('tags', [])
        self.link = kwargs.get('link', 'N/A')
        self.weight = kwargs.get('weight', 0)

    def __str__(self):
        return "{}{}{}{} < {}{}{}: {}{}{} >\n{}\nhref: {}{}{}".format(
            self.source_formatted, COLOR_TITLE, self.title, COLOR_NORMAL, COLOR_AUTHOR, self.author,
            COLOR_NORMAL, COLOR_DATE, self.date, COLOR_NORMAL, self.summary, COLOR_HREF, self.href, COLOR_NORMAL)

    @property
    def source_formatted(self):
        return "{c_b}[{c_s}{s_r}{c_b}]{c_n} ".format(
            c_b=COLOR_AUTHOR, c_s=COLOR_HREF, s_r=self.source, c_n=COLOR_NORMAL) if self.source else ''

    @property
    def author(self):
        return self.authors[0] if self.authors else 'N/A'

    @property
    def date(self):
        return self.submitted_date if self.submitted_date else 'N/A'

    @property
    def href(self):
        return self.link if self.link else 'N/A'
