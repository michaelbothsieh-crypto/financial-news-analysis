import streamlit as st
from financial_analyzer import FinancialAnalyzer
import plotly.graph_objects as go
import time

st.set_page_config(page_title="財經新聞智能分析系統", layout="wide", page_icon="📈")

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }
    
    /* Cards/Containers */
    .css-1r6slb0, .stExpander {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        height: 50px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.6);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: rgba(30, 41, 59, 0.5);
        color: white;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 10px 15px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* Metrics/Info Cards */
    .info-card {
        background: rgba(51, 65, 85, 0.5);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 10px;
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
        background: #475569; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b; 
    }
</style>
""", unsafe_allow_html=True)

# Header
col_header_1, col_header_2 = st.columns([1, 5])
with col_header_1:
    st.image("https://cdn-icons-png.flaticon.com/512/2534/2534204.png", width=80)
with col_header_2:
    st.title("財經新聞智能分析系統")
    st.markdown("#### 🚀 AI 驅動的深度市場洞察")
st.markdown("---")

# Initialize Analyzer
@st.cache_resource
def get_analyzer_v3():
    # API Key should be set in environment variables for security
    # In local development, you can set it in .env or export it
    api_key = os.getenv("OPENAI_API_KEY")
    return FinancialAnalyzer(api_key=api_key)

analyzer = get_analyzer_v3()

# Main Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📰 新聞來源")
    url_input = st.text_input("請輸入財經新聞連結 (URL)", placeholder="https://finance.yahoo.com/...")
    
    analyze_btn = st.button("🚀 開始智能分析", type="primary")
    
    if analyze_btn and url_input:
        with st.status("正在處理中...", expanded=True) as status:
            st.write("🌐 正在抓取網頁內容...")
            news_text = analyzer.fetch_news_from_url(url_input)
            
            if news_text.startswith("Error"):
                status.update(label="❌ 抓取失敗", state="error")
                st.error(news_text)
            else:
                st.write("🧠 正在進行情緒分析...")
                sentiment_label, sentiment_score = analyzer.analyze_sentiment(news_text)
                
                st.write("🔍 正在萃取關鍵資訊...")
                info = analyzer.extract_info(news_text)
                
                st.write("💡 正在生成投資建議...")
                advice = analyzer.generate_advice(news_text, sentiment_label)
                
                status.update(label="✅ 分析完成！", state="complete")
                
                # Store results in session state to persist across reruns if needed
                st.session_state['results'] = {
                    'text': news_text,
                    'sentiment': (sentiment_label, sentiment_score),
                    'info': info,
                    'advice': advice
                }

with col2:
    st.subheader("📊 分析儀表板")
    
    if 'results' in st.session_state:
        results = st.session_state['results']
        sentiment_label, sentiment_score = results['sentiment']
        
        # 1. Sentiment Gauge
        st.markdown("#### 情緒傾向")
        
        color = "lightgray"
        if sentiment_label == "positive":
            color = "#2ecc71" # Green
        elif sentiment_label == "negative":
            color = "#e74c3c" # Red
        else:
            color = "#f1c40f" # Yellow
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = sentiment_score * 100,
            title = {'text': sentiment_label.upper(), 'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': "white"},
                'bar': {'color': color},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 100], 'color': "rgba(255, 255, 255, 0.1)"}
                ],
            },
            number = {'font': {'color': 'white'}}
        ))
        fig.update_layout(
            height=250, 
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 2. Key Info
        st.markdown("#### 關鍵資訊")
        info = results['info']
        if "error" in info:
            st.warning(f"資訊萃取受限: {info['error']}")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div class="info-card">
                    <strong>🏢 公司</strong><br>{', '.join(info.get('company_name', []))}
                </div>
                <div class="info-card">
                    <strong>🎫 代號</strong><br>{', '.join(info.get('stock_code', []))}
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="info-card">
                    <strong>📅 時間</strong><br>{info.get('time_info', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander("查看財務數據與事件"):
                st.json(info.get('financial_data', {}))
                st.write("**重大事件**:")
                for event in info.get('events', []):
                    st.write(f"- {event}")

        # 3. Advice
        st.markdown("#### 💡 投資建議")
        st.markdown(results['advice'])
        
        with st.expander("查看原始新聞內容"):
            st.text(results['text'])

    else:
        st.info("👈 請在左側輸入網址並開始分析")
        st.image("https://images.unsplash.com/photo-1611974765270-ca1258634369?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", caption="Financial Analysis")

