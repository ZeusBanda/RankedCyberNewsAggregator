"""
scraper.py

This module loads RSS feeds from feeds.yaml and pulls recent articles
published within a given time window (default: 24 hours).

"""

import feedparser              # Parses RSS and Atom feeds
import yaml                    # Loads feeds.yaml config
from datetime import datetime, timezone
import dateutil.parser         # Parses published timestamps

def is_recent(article, hours_lookback):
    """
    Checks whether an article is recent based on its 'published' date.
    
    Args:
        article (dict): An RSS article with a 'published' field.
        hours (int): Lookback window (in hours).
    
    Returns:
        bool: True if published within `hours`, else False.
    """
    try:
        published_time = dateutil.parser.parse(article['published'])
        if published_time.tzinfo is None:
            published_time = published_time.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = (now - published_time).total_seconds()
        return delta < hours_lookback * 3600
    except Exception as e:
        # Optional: log unparseable article titles/links to a debug log
        return False

def load_feeds(feed_file='Keywords/Public/feeds.yaml'):
    """
    Loads the list of RSS feeds from a YAML file.

    Args:
        feed_file (str): Path to the YAML file.

    Returns:
        list[dict]: List of feeds, each with 'name', 'url', 'type'.
    """
    with open(feed_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data.get('feeds', [])  # fallback if file is malformed

def get_articles(hours_lookback):
    """
    Parses all feeds and returns a list of articles.

    Returns:
        List of article dicts with title, summary, link, source, published
    """
    feeds = load_feeds()
    articles = []

    for feed in feeds:
        parsed = feedparser.parse(feed['url'])

        for entry in parsed.entries:
            article = {
                'title': entry.title,
                'summary': getattr(entry, 'summary', ''),
                'link': entry.link,
                'source': feed['name'],
                'published': getattr(entry, 'published', ''),
                'source_type': feed['type']
            }
            if not is_recent(article,hours_lookback):
                continue
            
            articles.append(article)
    return articles
