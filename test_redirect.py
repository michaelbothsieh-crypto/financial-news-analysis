import requests
import feedparser

# 1. Fetch a URL from the RSS feed
rss_url = "https://news.google.com/rss/search?q=finance+when:1d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
feed = feedparser.parse(rss_url)

if feed.entries:
    google_url = feed.entries[0].link
    print(f"Original Google URL: {google_url}")
    
    # 2. Try to resolve it using googlenewsdecoder
    try:
        from googlenewsdecoder import new_decoderv1
        
        interval_time = 0 # Optional
        decoder = new_decoderv1(interval_time)
        
        if google_url:
            decoded_url = decoder.decode(google_url)
            print(f"Original URL: {google_url}")
            print(f"Decoded URL: {decoded_url.get('decoded_url')}")
            print(f"Status: {decoded_url.get('status')}")
            
    except Exception as e:
        print(f"Error resolving URL: {e}")
else:
    print("No entries found in RSS feed.")
