import feedparser
import json

# Yahoo Finance RSS
rss_url = "https://finance.yahoo.com/news/rssindex"

print(f"Fetching {rss_url}...")
feed = feedparser.parse(rss_url)

print(f"Entries found: {len(feed.entries)}")

if feed.entries:
    entry = feed.entries[0]
    print("First entry:")
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
else:
    print("No entries found.")
