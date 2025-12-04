import os
from financial_analyzer import FinancialAnalyzer

def test_localization():
    print("Testing Localization...")
    analyzer = FinancialAnalyzer()
    
    # Mock text
    text = "Apple Inc. reported record revenue. The stock price surged."
    sentiment = "positive"
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping localization test (No API Key)")
        return

    advice = analyzer.generate_advice(text, sentiment)
    print(f"Advice: {advice[:100]}...")
    
    # Check for Chinese characters
    has_chinese = any(u'\u4e00' <= c <= u'\u9fff' for c in advice)
    if has_chinese:
        print("✅ Advice contains Chinese characters.")
    else:
        print("❌ Advice does NOT contain Chinese characters.")

if __name__ == "__main__":
    test_localization()
