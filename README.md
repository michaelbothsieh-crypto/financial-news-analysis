# 財經新聞智能分析系統 (Financial Insights AI)

這是一個基於 Streamlit 的 AI 驅動財經新聞分析工具。它利用 **FinBERT** 進行專業的情緒分析，並結合 **OpenAI GPT** 模型來提取關鍵資訊並生成投資建議。

## 功能特色

- **情緒分析**: 使用 `ProsusAI/finbert` 模型準確判斷新聞情緒（正面、負面、中立）。
- **關鍵資訊提取**: 自動從新聞中提取公司名稱、股票代號、財務數據和重大事件。
- **投資策略建議**: 根據新聞內容與情緒分數，生成結構化的短期與長期投資建議。
- **現代化 UI**: 採用深色主題、玻璃擬態（Glassmorphism）設計，提供專業且舒適的視覺體驗。
- **歷史記錄**: 自動儲存分析過的連結，方便隨時回顧。

## 安裝與執行

### 1. 環境設定

確保您已安裝 Python 3.9+。

```bash
# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴套件
pip install -r requirements.txt
```

### 2. 設定 API Key

您需要一組 OpenAI API Key 才能使用進階分析功能。
您可以將其設定為環境變數，或是在應用程式介面中輸入。

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. 啟動應用程式

```bash
streamlit run app.py
```

## 技術架構

- **Frontend**: Streamlit (Custom CSS for styling)
- **NLP Model**: FinBERT (Hugging Face Transformers)
- **LLM**: OpenAI GPT-3.5 Turbo
- **Data Fetching**: Requests + BeautifulSoup

## 專案結構

- `app.py`: 主應用程式邏輯與 UI。
- `financial_analyzer.py`: 核心分析類別（封裝了 FinBERT 與 OpenAI 呼叫）。
- `test_automation.py`: 自動化測試腳本。
