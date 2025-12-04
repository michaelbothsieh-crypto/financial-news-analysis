import streamlit as st
from financial_analyzer import FinancialAnalyzer
import plotly.graph_objects as go
import time
import os

st.set_page_config(page_title="Financial Insights AI", layout="wide", page_icon="⚡")
print("🚀 Starting Financial Insights AI - Version 14e4f38 (Fixing Deployment)")
if not os:
    import os

# Custom CSS for Neo-Modern "Independent Designer" Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #e2e8f0;
    }
    
    /* Background & Main Container */
    .stApp {
        background-color: #0f172a; /* Slate 900 */
        background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 70%);
    }

    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
    }
    
    h1 {
        font-size: 2.2rem !important;
        background: linear-gradient(to right, #f8fafc, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Cards (Bento Grid / News) */
    .info-card, .news-card {
        background-color: #1e293b; /* Slate 800 */
        border: 1px solid #334155; /* Slate 700 */
        border-radius: 12px;
        padding: 20px;
        transition: all 0.2s ease;
    }
    
    .news-card:hover {
        border-color: #64748b; /* Slate 500 */
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Primary Button */
    .stButton>button {
        width: 100%;
        background-color: #3b82f6; /* Blue 500 */
        color: white;
        font-weight: 500;
        border-radius: 8px;
        height: 48px;
        border: none;
        transition: background-color 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #2563eb; /* Blue 600 */
        border: none;
    }
    
    .stButton>button:disabled {
        background-color: #334155;
        color: #94a3b8;
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020617 !important; /* Slate 950 */
        border-right: 1px solid #1e293b;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        color: #f8fafc !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    /* Adjust Top Padding for Streamlit Cloud Toolbar */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0f172a; 
    }
    ::-webkit-scrollbar-thumb {
        background: #334155; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #475569; 
    }
</style>

</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div style="margin-bottom: 20px; text-align: center;">', unsafe_allow_html=True)
st.title("財經新聞智能分析系統")
st.markdown('<p style="color: #94a3b8; font-size: 1.2rem; margin-top: -10px;">新世代 AI 市場洞察</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)



# Sidebar for Settings
with st.sidebar:
    st.header("⚙️ 設定")
    user_api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-proj-...")
    st.markdown("---")
    st.markdown("### 關於")
    st.markdown("此系統使用 OpenAI GPT 模型進行全方位的情緒分析與深度解讀。")
    
    # History Section
    st.markdown("---")
    st.header("📜 歷史記錄")
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    # Display history in reverse order (newest first)
    for i, url in enumerate(reversed(st.session_state['history'])):
        if st.button(f"🔗 {url[:30]}...", key=f"hist_{i}", help=url):
            st.session_state['url_input'] = url
            st.rerun()

# Initialize Analyzer
@st.cache_resource
def get_analyzer_v3(api_key_input):
    import os # Defensive import
    print("DEBUG: get_analyzer_v3 called with input:", api_key_input)
    # Priority: User Input > Environment Variable
    api_key = api_key_input or os.getenv("OPENAI_API_KEY")
    return FinancialAnalyzer(api_key=api_key)

analyzer = get_analyzer_v3(user_api_key)

# Market Overview Ticker
if "market_data" not in st.session_state:
    st.session_state["market_data"] = analyzer.fetch_market_data()

market_data = st.session_state["market_data"]
if market_data:
    cols = st.columns(len(market_data))
    for i, (name, data) in enumerate(market_data.items()):
        cols[i].metric(
            label=name, 
            value=f"{data['price']:,.2f}", 
            delta=f"{data['change_percent']:.2f}%"
        )
st.markdown("---")

# Main Layout - Centered Search
col_main_1, col_main_2, col_main_3 = st.columns([1, 2, 1])

with col_main_2:
    # Check if we have a URL from history click
    default_url = st.session_state.get('url_input', "")
    # Clear the session state trigger to avoid stuck input
    if 'url_input' in st.session_state:
        del st.session_state['url_input']
        
    url_input = st.text_input("", value=default_url, placeholder="請在此貼上新聞連結...", label_visibility="collapsed")
    
    # Check if API Key is available
    has_api_key = bool(user_api_key or os.getenv("OPENAI_API_KEY"))
    
    if not has_api_key:
        st.warning("⚠️ 請先在左側設定欄輸入 OpenAI API Key 才能開始分析")
        
    analyze_btn = st.button(
        "分析市場情緒", 
        type="primary", 
        disabled=not has_api_key,
        help="請先輸入 API Key" if not has_api_key else "點擊開始分析"
    )

st.markdown("---")

# Auto-trigger analysis if requested
if st.session_state.get('trigger_analysis', False):
    st.session_state['trigger_analysis'] = False # Reset flag
    analyze_btn = True # Force trigger

if analyze_btn:
    if not url_input:
        st.warning("請輸入新聞連結")
    else:
        with st.status("正在分析...", expanded=True) as status:
            st.write("🌐 正在讀取新聞內容...")
            news_text = analyzer.fetch_news_from_url(url_input)
            
            if news_text.startswith("Error"):
                st.error(news_text)
                status.update(label="分析失敗", state="error")
            else:
                st.write("🧠 神經網絡處理中...")
                sentiment_label, sentiment_score = analyzer.analyze_sentiment(news_text)
                
                # Translate Sentiment Label
                sentiment_map = {
                    "positive": "正面",
                    "negative": "負面",
                    "neutral": "中立"
                }
                sentiment_label_zh = sentiment_map.get(sentiment_label, sentiment_label)
                
                st.write("🔍 正在萃取關鍵實體...")
                info = analyzer.extract_info(news_text)
                
                st.write("💡 正在合成投資策略...")
                advice = analyzer.generate_advice(news_text, sentiment_label_zh)
                
                status.update(label="分析完成", state="complete")
                
                st.session_state['results'] = {
                    'text': news_text,
                    'sentiment': (sentiment_label_zh, sentiment_score),
                    'info': info,
                    'advice': advice
                }
                
                # Add to history if not exists
                if url_input not in st.session_state['history']:
                    st.session_state['history'].append(url_input)

# Results Dashboard
if 'results' in st.session_state:
    results = st.session_state['results']
    sentiment_label, sentiment_score = results['sentiment']
    info = results['info']
    
    # Bento Grid Layout
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Sentiment Card
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="info-label">市場情緒</div>', unsafe_allow_html=True)
        
        color = "#94a3b8"
        color = "#94a3b8"
        if sentiment_label == "正面":
            color = "#4ade80" # Green
        elif sentiment_label == "負面":
            color = "#f87171" # Red
        else:
            color = "#facc15" # Yellow
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = sentiment_score * 100,
            title = {'text': sentiment_label.upper(), 'font': {'color': color, 'size': 24, 'family': "Plus Jakarta Sans"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': "#94a3b8", 'tickwidth': 1},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 100], 'color': "rgba(255, 255, 255, 0.05)"}
                ],
            },
            number = {'font': {'color': '#f8fafc', 'size': 40, 'family': "Plus Jakarta Sans"}}
        ))
        fig.update_layout(
            height=280, 
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "#94a3b8", 'family': "Plus Jakarta Sans"}
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Investment Advice Card
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="info-label">策略洞察</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="info-value" style="font-size: 1rem;">{results["advice"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Key Info Cards (Stacked)
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">目標實體</div>
            <div class="info-value">{', '.join(info.get('company_name', ['N/A']))}</div>
            <div style="margin-top: 8px; font-size: 0.9rem; color: #64748b;">{', '.join(info.get('stock_code', ['N/A']))}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-card">
            <div class="info-label">時間軸</div>
            <div class="info-value">{info.get('time_info', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("原始財務數據"):
            st.json(info.get('financial_data', {}))
            
        with st.expander("關鍵事件"):
            for event in info.get('events', []):
                st.write(f"• {event}")
                
        with st.expander("新聞來源"):
            st.text(results['text'][:1000] + "...")

else:
    # Empty State
    # Trending News Section
    st.markdown("### 🔥 全球熱門財經新聞")
    
    # Initialize news pool if not present
    if "trending_news_pool" not in st.session_state:
        with st.spinner("正在抓取最新頭條..."):
            # Fetch more items to allow rotation (e.g., 20 items)
            st.session_state["trending_news_pool"] = analyzer.fetch_trending_news(limit=20)
            st.session_state["news_offset"] = 0
            
    news_pool = st.session_state["trending_news_pool"]
    offset = st.session_state["news_offset"]
    batch_size = 3
    
    if news_pool:
        # Get current batch
        current_batch = news_pool[offset : offset + batch_size]
        
        # Display current batch in a Grid
        cols = st.columns(3)
        for i, item in enumerate(current_batch):
            with cols[i]:
                # News Card
                st.markdown(f"""
                <div class="news-card" style="height: 200px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div style="font-weight: 600; font-size: 1rem; margin-bottom: 12px; line-height: 1.4;">
                        <a href="{item['link']}" target="_blank" style="color: #f8fafc; text-decoration: none;">{item['title']}</a>
                    </div>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: auto;">{item['published']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Button
                btn_key = f"trend_btn_{hash(item['title'])}"
                if st.button("⚡ 分析", key=btn_key, use_container_width=True, disabled=not has_api_key):
                    st.session_state['url_input'] = item['link']
                    st.session_state['trigger_analysis'] = True
                    st.rerun()
        
        # Refresh / Next Page Button
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        if st.button("🔄 換一批熱門新聞", type="secondary", use_container_width=True):
            # Increment offset, loop back if end reached
            new_offset = offset + batch_size
            if new_offset >= len(news_pool):
                new_offset = 0
            st.session_state["news_offset"] = new_offset
            st.rerun()
            
    else:
        st.info("暫時無法取得熱門新聞")

