import pandas as pd
# from transformers import pipeline
import openai
import json
import os
import feedparser
from bs4 import BeautifulSoup
import time
import requests
from googlenewsdecoder import new_decoderv1
import yfinance as yf
import urllib3

# Suppress SSL warnings for scraper
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FinancialAnalyzer:
    def __init__(self, api_key=None, model_provider="openai"):
        # Try to get API key from env if not provided
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_provider = model_provider
        
        # Initialize FinBERT pipeline
        # Lazy loading: Don't load it here to save memory on startup
        self.sentiment_pipeline = None

    def fetch_news_from_url(self, url):
        """
        Fetches news content from a given URL.
        Handles Google News redirects.
        """
        try:
            # Handle Google News Redirects
            if "news.google.com" in url:
                print(f"DEBUG: Decoding Google News URL: {url}")
                try:
                    decoded = new_decoderv1(url)
                    if decoded.get("status"):
                        url = decoded.get("decoded_url")
                        print(f"DEBUG: Decoded URL: {url}")
                    else:
                        print("DEBUG: Failed to decode Google News URL")
                except Exception as e:
                    print(f"DEBUG: Error decoding Google News URL: {e}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            print(f"DEBUG: Fetching {url} with verify=False")
            
            # Use a session to ensure settings are applied
            session = requests.Session()
            session.verify = False
            session.headers.update(headers)
            
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            print(f"DEBUG: Fetch success, status: {response.status_code}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            return f"Error fetching URL: {str(e)}"

    def analyze_sentiment(self, text):
        """
        Analyze sentiment using OpenAI (lighter than FinBERT for deployment).
        Returns: label (positive/neutral/negative), score (confidence)
        """
        if not self.api_key:
            return "neutral", 0.0
        
        truncated_text = text[:4000]
        
        prompt = f"""
        請分析以下財經新聞的情緒。
        請只輸出 JSON 格式，包含兩個欄位：
        - label: "positive", "neutral", 或 "negative"
        - score: 0.0 到 1.0 之間的情緒強度分數

        新聞內容：
        {truncated_text}
        """

        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial sentiment analyst. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            content = response.choices[0].message.content
            # Clean up code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
                
            result = json.loads(content.strip())
            return result.get("label", "neutral"), result.get("score", 0.5)
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return "neutral", 0.0

    def extract_info(self, text):
        """
        Extract key information using LLM.
        Returns: JSON object or dict
        """
        if not self.api_key:
            return {"error": "API Key is missing (Set OPENAI_API_KEY env var)"}

        # Truncate text for LLM to avoid token limits (simple truncation)
        truncated_text = text[:4000]

        prompt = f"""
        請分析以下財經新聞，並提取關鍵資訊。請務必使用**繁體中文**回答。請以 JSON 格式輸出，包含以下欄位：
        - company_name: 公司名稱 (List of strings)
        - stock_code: 股票代號 (List of strings)
        - financial_data: 財務數據 (Dictionary, e.g., {{"revenue": "...", "eps": "..."}})
        - events: 重大事件 (List of strings)
        - time_info: 時間資訊 (String)

        新聞內容：
        {truncated_text}
        """

        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            content = response.choices[0].message.content
            # Clean up code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content.strip())
        except Exception as e:
            return {"error": str(e)}

    def generate_advice(self, text, sentiment_label):
        """
        Generate investment advice based on text and sentiment.
        """
        if not self.api_key:
            return "API Key is missing. Cannot generate advice."

        truncated_text = text[:4000]

        prompt = f"""
        基於以下財經新聞內容以及情緒分析結果（{sentiment_label}），請給出結構化的投資建議。請務必使用**繁體中文**回答。
        建議應包含：
        1. 短期觀察重點
        2. 長期投資潛力
        3. 風險提示

        新聞內容：
        {truncated_text}
        """

        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional investment advisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating advice: {str(e)}"

    def fetch_trending_news(self, limit=5):
        """
        Fetch trending financial news from Google News RSS.
        Returns: List of dicts {title, link, published}
        """
        rss_url = "https://news.google.com/rss/search?q=finance+when:1d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
        try:
            feed = feedparser.parse(rss_url)
            news_items = []
            for entry in feed.entries[:limit]:
                news_items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published
                })
            return news_items
        except Exception as e:
            print(f"Error fetching trending news: {e}")
            return []

    def fetch_market_data(self):
        """
        Fetch current market data for key indices.
        Returns: Dict of {symbol: {price, change_percent}}
        """
        tickers = {
            "^GSPC": "S&P 500",
            "^IXIC": "Nasdaq",
            "^TWII": "台灣加權",
            "BTC-USD": "Bitcoin"
        }
        data = {}
        try:
            for symbol, name in tickers.items():
                ticker = yf.Ticker(symbol)
                # Get fast info first (faster than history)
                info = ticker.fast_info
                if info and info.last_price:
                    price = info.last_price
                    prev_close = info.previous_close
                    change_percent = ((price - prev_close) / prev_close) * 100
                    data[name] = {
                        "price": price,
                        "change_percent": change_percent
                    }
            return data
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return {}
