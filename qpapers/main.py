import sys

from .arxiv import ArxivAdvanceSearch

SEARCH_ENGINES = [
    ArxivAdvanceSearch,
]


def main():
    if len(sys.argv) <= 1:
        print("Usage: python qpapers.py <search keywords>")
        sys.exit(0)

    try:
        keyword = ' '.join(sys.argv[1:])

        all_articles = []

        for se_class in SEARCH_ENGINES:
            search_engine = se_class()
            search_engine.set_keyword(keyword)
            articles = search_engine.get_articles()
            all_articles.extend(articles)

            for article in sorted(all_articles, key=lambda a: a.weight, reverse=True):
                print(article, end='\n\n')
    except KeyboardInterrupt:
        print("closing...")


if __name__ == '__main__':
    main()
