import streamlit as st
from financial_analyzer import FinancialAnalyzer
import plotly.graph_objects as go
import time
import os

st.set_page_config(page_title="Financial Insights AI", layout="wide", page_icon="⚡")
print("🚀 Starting Financial Insights AI...")
if not os:
    import os

# Custom CSS for Neo-Modern "Independent Designer" Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Background & Main Container */
    .stApp {
        background-color: #020617;
        background-image: 
            radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.15) 0px, transparent 50%),
            linear-gradient(#0f172a 1px, transparent 1px),
            linear-gradient(90deg, #0f172a 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
        color: #f8fafc;
    }

    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(to right, #f8fafc, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Bento Grid Cards */
    .css-1r6slb0, .stExpander, .info-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 24px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .info-card:hover {
        border-color: rgba(139, 92, 246, 0.3);
        transform: translateY(-2px);
    }

    /* Primary Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        font-weight: 600;
        border-radius: 16px;
        height: 56px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.5);
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* Input Fields */
    /* Input Fields - Force High Contrast */
    .stTextInput>div>div>input {
        background-color: #1e293b !important; /* Darker background */
        color: #ffffff !important; /* Pure white text */
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        caret-color: #ffffff !important; /* White cursor */
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.3) !important;
        background-color: #1e293b !important;
    }

    /* Force Sidebar to be Dark */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Sidebar Text */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }

    /* Remove Top Padding & Hide Header Decoration */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        margin-top: -20px !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        z-index: -1;
    }
    
    /* Remove H1 top margin */
    h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Nuclear Option for Status Widget */
    div[data-testid="stStatusWidget"] {
        background-color: #0f172a !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    /* Target ALL children within the status widget */
    div[data-testid="stStatusWidget"] * {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    /* Specifically target details and summary globally as a fallback */
    details {
        background-color: #0f172a !important;
        border-color: rgba(148, 163, 184, 0.1) !important;
    }
    
    summary {
        background-color: #0f172a !important;
        color: #f8fafc !important;
    }
    
    summary:hover {
        background-color: #1e293b !important;
    }
    
    /* Fix SVG Icons in Status */
    div[data-testid="stStatusWidget"] svg {
        fill: #f8fafc !important;
        stroke: #f8fafc !important;
        background-color: transparent !important; /* Icons shouldn't have background */
    }
    
    /* Ensure the spinner is visible */
    div[data-testid="stStatusWidget"] .stSpinner {
        border-color: #8b5cf6 !important;
        border-top-color: transparent !important;
    }
    
    /* Info Card Specifics */
    .info-card {
        padding: 24px;
        margin-bottom: 16px;
        height: 100%;
    }
    
    .info-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .info-value {
        font-size: 1.1rem;
        font-weight: 500;
        color: #f1f5f9;
        line-height: 1.4;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent; 
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.2); 
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(148, 163, 184, 0.4); 
    }
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
    st.markdown("此系統使用 FinBERT 進行情緒分析，並透過 OpenAI 進行深度解讀。")
    
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
    # Priority: User Input > Environment Variable
    api_key = api_key_input or os.getenv("OPENAI_API_KEY")
    return FinancialAnalyzer(api_key=api_key)

analyzer = get_analyzer_v3(user_api_key)

# Main Layout - Centered Search
col_main_1, col_main_2, col_main_3 = st.columns([1, 2, 1])

with col_main_2:
    # Check if we have a URL from history click
    default_url = st.session_state.get('url_input', "")
    # Clear the session state trigger to avoid stuck input
    if 'url_input' in st.session_state:
        del st.session_state['url_input']
        
    url_input = st.text_input("", value=default_url, placeholder="請在此貼上新聞連結...", label_visibility="collapsed")
    analyze_btn = st.button("分析市場情緒", type="primary")

st.markdown("---")

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
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; color: #64748b;">
        <div style="font-size: 4rem; margin-bottom: 20px; opacity: 0.5;">⚡</div>
        <p>等待數據流進行分析...</p>
    </div>
    """, unsafe_allow_html=True)

