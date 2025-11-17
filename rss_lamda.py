import feedparser
import os
from processor import log_event


RSS_FEEDS = os.getenv("RSS_FEEDS", "").split(",")


_seen_items = set()

def lambda_handler(event, context):
    for feed_url in RSS_FEEDS:
        feed_url = feed_url.strip()
        if not feed_url:
            continue

        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            uid = entry.get("id") or entry.get("link")
            if uid not in _seen_items:
                _seen_items.add(uid)

                product = entry.get("title", "Unknown")
                message = entry.get("summary", "No summary")

                log_event(product, message)

    return {"statusCode": 200}
