import pandas as pd
from transformers import pipeline
import openai
import json
import os
import requests
from bs4 import BeautifulSoup

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
        Fetch text content from a URL.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
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
        Analyze sentiment using FinBERT.
        Returns: label (Positive/Neutral/Negative), score
        """
        if not self.sentiment_pipeline:
            try:
                print("Loading FinBERT model...")
                self.sentiment_pipeline = pipeline("text-classification", model="ProsusAI/finbert")
            except Exception as e:
                print(f"Error loading FinBERT: {e}")
                return f"Error loading model: {str(e)}", 0.0
        
        # FinBERT has a max token length, usually 512. We might need to truncate or chunk.
        try:
            # Truncate to 512 tokens (approx) to avoid errors
            result = self.sentiment_pipeline(text[:2000], truncation=True, max_length=512)[0]
            return result['label'], result['score']
        except Exception as e:
            return f"Error: {str(e)}", 0.0

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
