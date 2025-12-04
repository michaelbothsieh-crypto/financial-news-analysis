import os
from financial_analyzer import FinancialAnalyzer
import sys

def test_automation():
    print("🚀 Starting Automated Test...")
    
    # 1. Initialize
    print("1. Initializing Analyzer...")
    analyzer = FinancialAnalyzer()
    if analyzer.sentiment_pipeline:
        print("   ✅ FinBERT loaded successfully")
    else:
        print("   ❌ FinBERT failed to load")
        sys.exit(1)

    # 2. Test URL Fetching
    test_url = "https://finance.yahoo.com/news/nvidia-stock-falls-after-earnings-report-what-investors-need-to-know-123456.html" 
    # Note: The above is a dummy URL structure. Let's use a real one or handle 404.
    # Actually, let's use a reliable URL or just mock the fetch for 'automation' if we can't guarantee a live URL.
    # But the user asked to "automate test items". Let's try to fetch a real page if possible, or just test the analysis part with raw text if fetch fails.
    
    # Let's use a generic tech news site or just a sample text if URL fails, 
    # but the goal is to test the *system*.
    # Let's try a google finance page or similar.
    # For stability, let's use a known existing page if possible, or just a sample text for the 'analysis' part 
    # and a separate test for 'fetch' with a likely stable URL.
    
    print("2. Testing URL Fetching...")
    # Using a very stable URL (e.g., example.com) just to test connectivity, 
    # but for content we might need something real. 
    # Let's try to fetch a Wikipedia page about a company, it's stable.
    url = "https://en.wikipedia.org/wiki/Apple_Inc."
    text = analyzer.fetch_news_from_url(url)
    
    if "Error" in text:
        print(f"   ⚠️ URL Fetch warning: {text}")
        print("   (This might be due to network or anti-bot, continuing with mock text)")
        text = "Apple Inc. reported record revenue of $100 billion. The stock price surged by 5%. Analysts are optimistic."
    else:
        print(f"   ✅ Fetched {len(text)} characters from {url}")

    # 3. Test Sentiment
    print("3. Testing Sentiment Analysis...")
    label, score = analyzer.analyze_sentiment(text)
    print(f"   Result: {label} (Score: {score:.4f})")
    if label in ["positive", "negative", "neutral"]:
        print("   ✅ Sentiment Analysis passed")
    else:
        print("   ❌ Sentiment Analysis failed")

    # 4. Test Extraction (Requires API Key)
    if os.getenv("OPENAI_API_KEY"):
        print("4. Testing Info Extraction (LLM)...")
        info = analyzer.extract_info(text)
        if "error" in info:
             print(f"   ❌ Extraction failed: {info['error']}")
        else:
             print("   ✅ Extraction successful")
             print(f"   Company: {info.get('company_name')}")
    else:
        print("4. Skipping LLM tests (No OPENAI_API_KEY found)")

    print("🎉 Automation Test Completed!")

if __name__ == "__main__":
    test_automation()
