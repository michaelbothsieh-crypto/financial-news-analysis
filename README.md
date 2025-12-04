# 財經新聞智能分析系統 (Financial News AI Analyzer)

這是一個基於 Streamlit 和 OpenAI 的財經新聞智能分析系統。它能夠自動抓取新聞內容，進行情緒分析，提取關鍵資訊，並生成投資建議。

## 功能特色

-   **自動抓取**: 輸入新聞網址即可自動提取內容。
-   **情緒分析**: 使用 FinBERT 模型分析新聞情緒（正面/負面/中性）。
-   **關鍵資訊萃取**: 使用 LLM 提取公司名稱、股票代號、財務數據等。
-   **投資建議**: 根據分析結果生成結構化的投資建議。
-   **現代化 UI**: 採用精緻的 Dark Mode 設計，提供最佳的使用者體驗。

## 本地安裝與執行

1.  **Clone 專案**
    ```bash
    git clone <your-repo-url>
    cd financial_news_analysis
    ```

2.  **建立虛擬環境**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **安裝依賴**
    ```bash
    pip install -r requirements.txt
    ```

4.  **設定環境變數**
    專案需要 OpenAI API Key。雖然程式碼中已包含（僅供演示），建議使用環境變數：
    ```bash
    export OPENAI_API_KEY='your-api-key'
    ```

5.  **執行應用程式**
    ```bash
    streamlit run app.py
    ```

## 部署至 Render

本專案已準備好部署至 [Render](https://render.com)。

1.  將程式碼推送到 GitHub。
2.  在 Render Dashboard 點擊 "New +" -> "Web Service"。
3.  連結你的 GitHub Repository。
4.  設定如下：
    -   **Runtime**: Python 3
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5.  點擊 "Create Web Service"。

## 技術棧

-   [Streamlit](https://streamlit.io/)
-   [OpenAI API](https://openai.com/)
-   [Hugging Face Transformers (FinBERT)](https://huggingface.co/ProsusAI/finbert)
-   [Plotly](https://plotly.com/)
