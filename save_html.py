import requests
import feedparser

rss_url = "https://news.google.com/rss/search?q=finance+when:1d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
feed = feedparser.parse(rss_url)

if feed.entries:
    google_url = feed.entries[0].link
    try:
        response = requests.get(google_url, timeout=10)
        with open("google_redirect.html", "w") as f:
            f.write(response.text)
        print("Saved HTML to google_redirect.html")
    except Exception as e:
        print(f"Error: {e}")
