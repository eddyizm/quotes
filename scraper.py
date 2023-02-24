import feedparser
from datetime import datetime
from pprint import pprint


URLS = {'love': 'https://www.brainyquote.com/link/quotelo.rss',
        'nature': 'https://www.brainyquote.com/link/quotena.rss',
        'funny': 'https://www.brainyquote.com/link/quotefu.rss',
        'art': 'https://www.brainyquote.com/link/quotear.rss'}


feed = feedparser.parse(URLS['love'])
entries = feed.get('entries')
feed_info = feed.get('feed')


def check_published_date(feed_info) -> bool:
    published = datetime.strptime(feed_info.published[0:16], '%a, %d %b %Y' )
    if datetime.now().date() == published.date():
        print('load records')
        return True

check_published_date(feed_info)

# for entry in entries:
#     print(entry.summary)
#     print(entry.title)

def read_feeds():
    for category, url in URLS.items():
        print(category, url)

# read_feeds()
