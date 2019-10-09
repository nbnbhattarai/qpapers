'''
qPapers Main File
'''
import sys

from .arxiv import ArxivAdvanceSearch
from .scienceopen import ScienceOpenSearch
from .config import Config

from .article import (
    COLOR_HREF,
    COLOR_NORMAL,
)

SEARCH_ENGINES = {
    'arxiv': ArxivAdvanceSearch,
    'scienceopen': ScienceOpenSearch
}


def print_usage():
    print("Usage: python qpapers.py <search keyword>")


def main():
    '''Entry Point of qPapers'''
    if len(sys.argv) <= 1:
        print_usage()
        sys.exit(1)

    config = Config()
    services_enabled = []
    for service, config in config.enabled_services.items():
        engine = SEARCH_ENGINES.get(service)
        if engine:
            services_enabled.append({
                'engine': engine,
                'results': config.get('results', 5)
            })

    try:
        keyword = ' '.join(sys.argv[1:])

        all_articles = []

        for service in services_enabled:
            search_engine = service.get('engine')()
            search_engine.set_keyword(keyword)
            search_engine.set_results(service.get('results'))
            articles = search_engine.get_articles()
            if not articles:
                print("[{}{}] {}No Results Found".format(
                    COLOR_HREF, search_engine.NAME, COLOR_NORMAL
                ))
            else:
                all_articles.extend(articles)

        for article in sorted(all_articles, key=lambda a: a.weight, reverse=True):
            print(article, end='\n\n')
    except KeyboardInterrupt:
        print("closing...")


if __name__ == '__main__':
    main()
