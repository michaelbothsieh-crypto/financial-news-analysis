import feedparser

rss_url = "https://news.google.com/rss/search?q=finance+when:1d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
print(f"Fetching RSS from: {rss_url}")

try:
    feed = feedparser.parse(rss_url)
    print(f"Status: {feed.get('status', 'Unknown')}")
    print(f"Bozo: {feed.get('bozo', 'Unknown')}")
    print(f"Entries found: {len(feed.entries)}")
    
    if feed.entries:
        print("First entry title:", feed.entries[0].title)
    else:
        print("No entries found.")
        if hasattr(feed, 'bozo_exception'):
            print(f"Bozo exception: {feed.bozo_exception}")
            
except Exception as e:
    print(f"Error: {e}")
