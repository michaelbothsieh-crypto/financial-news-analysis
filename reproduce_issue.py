from financial_analyzer import FinancialAnalyzer
import inspect

try:
    analyzer = FinancialAnalyzer()
    if hasattr(analyzer, 'fetch_news_from_url'):
        print("SUCCESS: Method 'fetch_news_from_url' exists.")
    else:
        print("FAILURE: Method 'fetch_news_from_url' does NOT exist.")
        
    # Print all methods
    print("Methods:", [m for m in dir(analyzer) if not m.startswith('__')])
except Exception as e:
    print(f"ERROR: {e}")
