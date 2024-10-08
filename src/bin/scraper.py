import asyncio
import feedparser
from datetime import datetime
from src.core.models.quote_models import Quote_Staging
from src.core.routers.quote import submit_new_quote
from src.core.schema.jobs import insert_daily_quote
from src.core.schema.dal import database

URLS = {'love': 'https://www.brainyquote.com/link/quotelo.rss',
        'nature': 'https://www.brainyquote.com/link/quotena.rss',
        'funny': 'https://www.brainyquote.com/link/quotefu.rss',
        'art': 'https://www.brainyquote.com/link/quotear.rss'}


def check_published_date(feed_info) -> bool:
    published = datetime.strptime(feed_info.published[0:16], '%a, %d %b %Y' )
    print(f'published date: {published.date()}')
    print(f'current timestampt: {datetime.now().date()}')
    if datetime.now().date() == published.date():
        print('published date is a match')
        return True


def get_entries_and_feed_info(url):
    print('getting feed and returning entries')
    feed = feedparser.parse(url)
    entries = feed.get('entries')
    feed_info = feed.get('feed')
    return entries, feed_info


def parse_entry(entries, category):
    new_quotes = []
    for entry in entries:
        print('parsing feed for quotes')
        new_quote = Quote_Staging(
            quote = entry.summary,
            author = entry.title,
            added_by = 'automated_py',
            added_to_quotes = False,
            category = category
        )
        new_quotes.append(new_quote)
    return new_quotes


async def submit_quotes(quotes):
    for quote in quotes:
        print('submitting quote')
        await submit_new_quote(quote)


async def process_url(category, url):
    entries, feed_info = get_entries_and_feed_info(url)
    if check_published_date(feed_info):
        new_quotes = parse_entry(entries, category)

        await submit_quotes(new_quotes)


async def read_feeds():
    print('inserting daily quote')
    try:
        connected = await database.connect()
        if database.is_connected:
            await insert_daily_quote()
            for category, url in URLS.items():
                await process_url(category, url)
        else:
            raise Exception('did not get db connection.')
    finally:
        await database.disconnect()

if __name__ == '__main__':
    asyncio.run(read_feeds())
