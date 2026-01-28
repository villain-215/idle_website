import streamlit as st
import datetime
import pandas as pd             
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# ⚙️ 頁面配置 (Page Configuration)
# ==========================================
st.set_page_config(
    page_title="i-dle DIMENSION | Romantic Gallery",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌹"
)

# ==========================================
# 🎨 核心風格與 CSS 注入 (The Romantic Gallery Visuals)
# ==========================================

# 定義色票 (Color Palette: Romantic Gallery)
colors = {
    "bg": "#FFF5F5",             # Blush White (畫布底色)
    "accent_primary": "#D92E46", # Velvet Rose (絲絨玫瑰紅)
    "accent_secondary": "#9D7AAE", # Dusty Lilac (煙燻紫丁香)
    "text_main": "#4A2C2C",      # Warm Cocoa (暖可可深褐)
    "text_sub": "#9E9085",       # Warm Greige (暖灰褐)
    "quote_bg": "#FFF0F5",       # Pale Lavender Blush (語錄框底色)
    "white": "#FFFFFF"
}

custom_css = f"""
<style>
    /* 引入字體：
       - Playfair Display: 標題 (優雅襯線)
       - DM Sans: 內文 (現代人文無襯線)
       - Pinyon Script: 手寫副標 (浪漫手寫體)
    */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;500&family=Pinyon+Script&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap');

    /* 全站基礎設定 */
    .stApp {{
        background-color: {colors['bg']};
        color: {colors['text_main']};
        font-family: 'DM Sans', sans-serif;
    }}

    /* 標題字體策略 */
    h1, h2, h3, .serif-font {{
        font-family: 'Playfair Display', serif !important;
        font-weight: 700;
        color: {colors['text_main']};
    }}
    
    /* 手寫字體樣式 */
    .handwriting {{
        font-family: 'Pinyon Script', cursive;
        font-weight: 400;
        font-size: 1.5rem;
        color: {colors['text_sub']};
    }}

    /* 側邊欄客製化 (The Gallery Guide) */
    [data-testid="stSidebar"] {{
        background-color: {colors['bg']};
        border-right: 1px solid rgba(74, 44, 44, 0.1);
    }}
    
    .sidebar-logo {{
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: {colors['accent_primary']};
        font-weight: bold;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }}
    
    .sidebar-sub {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 3px;
        color: {colors['text_sub']};
        text-transform: uppercase;
        margin-bottom: 40px;
    }}

    /* 隱藏預設 Header 與 Footer */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* ------------------------------------
       視覺組件樣式 (Components)
       ------------------------------------ */

    /* 1. 精神宣言大標題 (Hero Text: The Manifesto) */
    .hero-title-box {{
        margin-bottom: 30px;
    }}
    
    .hero-line-1 {{
        font-family: 'Playfair Display', serif;
        font-size: 5.5rem;
        line-height: 0.9;
        font-weight: 700;
        color: {colors['accent_primary']}; /* Velvet Rose */
    }}
    
    .hero-line-2 {{
        font-family: 'Playfair Display', serif;
        font-size: 5.5rem;
        line-height: 0.9;
        font-weight: 700;
        color: {colors['text_main']}; /* Warm Cocoa */
    }}

    /* 2. 語錄框 (Sticky Note -> Elegant Quote) */
    .romantic-quote-box {{
        background-color: {colors['quote_bg']};
        padding: 30px 40px;
        border-radius: 16px;
        position: relative;
        margin-top: 20px;
        /* 左側漸層飾條 */
        border-left: 6px solid {colors['accent_primary']}; 
        border-image: linear-gradient(to bottom, {colors['accent_primary']}, {colors['accent_secondary']}) 1 100%;
        box-shadow: 0 10px 30px -10px rgba(217, 46, 70, 0.1);
    }}
    
    .quote-content {{
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem;
        line-height: 1.6;
        color: {colors['text_main']};
        font-style: italic;
    }}
    
    .quote-meta {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        color: {colors['accent_secondary']};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 15px;
        text-align: right;
    }}

    /* 3. 策展人卡片 (Curator Profile: Sunset Gradient) */
    .curator-card {{
        /* 晚霞漸層：玫瑰紅 -> 蜜桃 -> 煙燻紫 */
        background: linear-gradient(135deg, {colors['accent_primary']} 0%, #FF9A9E 50%, {colors['accent_secondary']} 100%);
        border-radius: 24px;
        padding: 40px;
        color: white;
        box-shadow: 0 20px 50px -15px rgba(217, 46, 70, 0.3);
        position: relative;
        overflow: hidden;
        min-height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    /* 玻璃擬態質感遮罩 */
    .glass-overlay {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    .card-title {{
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }}
    
    .card-subtitle {{
        font-family: 'Pinyon Script', cursive;
        font-size: 1.8rem;
        opacity: 0.9;
    }}

    /* 按鈕客製化 (Magazine Style) */
    .stButton > button {{
        background-color: transparent;
        color: {colors['accent_primary']};
        border: 1px solid {colors['accent_primary']};
        border-radius: 0px; /* 方形按鈕 */
        padding: 8px 24px;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 1px;
        transition: all 0.4s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {colors['accent_primary']};
        color: white;
        border-color: {colors['accent_primary']};
        box-shadow: 0 5px 15px rgba(217, 46, 70, 0.2);
    }}
    
    /* 分隔線 */
    hr {{
        border-color: rgba(74, 44, 44, 0.15);
        margin: 30px 0;
    }}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 🏛️ 側邊導覽列 (The Gallery Guide)
# ==========================================
with st.sidebar:
    # Logo Area
    st.markdown(f"""
    <div class="sidebar-logo">i-dle</div>
    <div class="sidebar-sub">DIMENSION</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Menu (Functional but Styled)
    # 這裡使用 radio 來模擬導覽，但透過 format_func 加上描述
    nav_options = {
        "i-voice": "Artist's Statement",
        "i-archive": "The Collection",
        "i-lab": "Perspectives",
        "i-concierge": "Curator's Guide"
    }
    
    nav_subtitles = {
        "i-voice": "The Manifesto",
        "i-archive": "Discography & Works",
        "i-lab": "Analysis & Insights",
        "i-concierge": "Resources & Links"
    }

    selected_nav = st.radio(
        "Navigation",
        options=list(nav_options.keys()),
        format_func=lambda x: nav_options[x],
        label_visibility="collapsed"
    )

    # 在選單下方顯示對應的手寫副標，增強藝廊感
    st.markdown(f"""
    <div style="margin-top: -10px; margin-bottom: 30px; padding-left: 15px;">
        <span class="handwriting" style="font-size: 1.2rem; color: {colors['accent_secondary']}">{nav_subtitles[selected_nav]}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.7rem; color: {colors['text_sub']}; text-align: center; margin-top: 20px;">
        OPENING HOURS<br>ALWAYS OPEN<br><br>
        ADMISSION<br>FREE FOR NEVERLAND
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 🖼️ 主畫面內容 (Main Gallery Space)
# ==========================================

# 根據側邊欄選擇，顯示不同內容
if selected_nav == "i-voice":
    # ----------------------------------------------------
    # A. i-voice: Artist's Statement (原本的首頁)
    # ----------------------------------------------------
    
    # 頂部裝飾
    st.markdown(f"""
    <div style="display: flex; align-items: baseline; margin-bottom: 20px;">
        <span style="font-family: 'DM Sans'; font-weight: bold; color: {colors['text_sub']}; letter-spacing: 2px; font-size: 0.8rem;">EXHIBITION NO. 05</span>
        <span style="margin-left: auto; font-family: 'Pinyon Script'; color: {colors['accent_primary']}; font-size: 1.5rem;">The Manifesto</span>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_space, col_right = st.columns([1.1, 0.1, 1.2])

    with col_left:
        st.markdown("<br>", unsafe_allow_html=True)
        # 雙色主標題
        st.markdown("""
        <div class="hero-title-box">
            <div class="hero-line-1">I NEVER</div>
            <div class="hero-line-2">DIE</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 內文敘述
        st.markdown(f"""
        <div style="font-size: 1.1rem; line-height: 1.8; color: {colors['text_main']}; text-align: justify; margin-bottom: 20px;">
            歡迎來到 <b>i-dle DIMENSION</b> 的浪漫篇章。在這裡，我們褪去了冰冷的武裝，
            將每一次的破碎與重生，都凝視為藝術。
            <span style="color: {colors['accent_primary']}; font-style: italic;">"玫瑰即使凋零，依然是花中女王。"</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 優雅語錄框
        st.markdown("""
        <div class="romantic-quote-box">
            <div class="quote-content">
                "We frame our scars in gold and velvet,<br>
                turning every battle into a masterpiece."
            </div>
            <div class="quote-meta">— The Curator's Note</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # 策展人卡片邏輯 (保留你原本寫好的)
        muse_options = ["Miyeon", "Minnie", "Soyeon", "Yuqi", "Shuhua"]
        selected_muse = st.selectbox("Select Muse", muse_options, label_visibility="collapsed")
        
        traits = {
            "Soyeon": "The Visionary Architect", "Miyeon": "The Classical Muse",
            "Minnie": "The Dreamy Surrealist", "Yuqi": "The Bold Expressionist",
            "Shuhua": "The Naturalist Icon"
        }

        # 策展人卡片 HTML (加上 muse 變數)
        curator_html = f"""
        <div class="curator-card">
            <div>
                <div class="card-title">{selected_muse}</div>
                <div class="card-subtitle">{traits[selected_muse]}</div>
            </div>
            <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; opacity: 0.2;">
                 <span style="font-size: 8rem; font-family: 'Playfair Display';">i-dle</span>
            </div>
            <div class="glass-overlay">
                <div style="display: flex; justify-content: space-between; align-items: end;">
                    <div>
                        <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Collection Status</div>
                        <div style="font-family: 'Playfair Display'; font-size: 1.5rem;">On Display</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Gallery Zone</div>
                        <div style="font-family: 'Pinyon Script'; font-size: 1.8rem;">Zone 2026</div>
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(curator_html, unsafe_allow_html=True)

elif selected_nav == "i-archive":
    # ----------------------------------------------------
    # B. i-archive: The Collection (典藏作品)
    # ----------------------------------------------------
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 4rem; margin-bottom: 0; color: {colors['accent_primary']}">The Collection</h1>
        <div class="handwriting" style="font-size: 2rem;">Discography & Works</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用 Tabs 區分時期 (Eras)
    tab1, tab2, tab3 = st.tabs(["2 (2024)", "I feel (2023)", "I NEVER DIE (2022)"])
    
    with tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            # 這裡可以使用 st.image 放專輯封面
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
                <div style="aspect-ratio: 1/1; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 8px; margin-bottom: 15px;">
                    <span style="color: #888;">Album Cover Placeholder</span>
                </div>
                <h3 style="margin: 0;">2</h3>
                <p style="color: {colors['text_sub']}; font-size: 0.9rem;">The 2nd Full Album</p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("### Title Track: Super Lady")
            # 模擬播放器樣式
            st.markdown(f"""
            <div style="padding: 20px; background: white; border-radius: 12px; border-left: 4px solid {colors['accent_primary']};">
                <p style="font-family: 'Playfair Display'; font-style: italic; font-size: 1.2rem;">"I am the top, super lady..."</p>
                <div style="margin-top: 10px; height: 4px; background: #eee; border-radius: 2px;">
                    <div style="width: 40%; height: 100%; background: {colors['accent_primary']}; border-radius: 2px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("View Full Tracklist", expanded=True):
                st.markdown("""
                1. **Super Lady**
                2. Revenge
                3. Doll
                4. Vision
                """)

    with tab2:
        st.info("Archive data for [I feel] era is currently being curated.")

elif selected_nav == "i-lab":
    # ----------------------------------------------------
    # C. i-lab: Perspectives (觀點與分析)
    # ----------------------------------------------------
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 4rem; margin-bottom: 0; color: {colors['accent_primary']}">Perspectives</h1>
        <div class="handwriting" style="font-size: 2rem;">Analysis & Insights</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        # 雷達圖邏輯 (Radar Chart)
        st.markdown("### Member Attributes")
        # 假資料
        df = pd.DataFrame(dict(
            r=[90, 85, 80, 95, 88],
            theta=['Vocal', 'Rap', 'Dance', 'Producing', 'Visual']
        ))
        
        # 使用 Plotly 畫圖，並配合你的配色
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself', line_color=colors['accent_primary'])
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, showticklabels=False),
                bgcolor='rgba(0,0,0,0)' # 透明背景
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="DM Sans", color=colors['text_main']),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        # 文字分析
        st.markdown(f"""
        <div style="background-color: white; padding: 30px; border-radius: 16px; height: 100%;">
            <h4 style="font-family: 'Playfair Display'; color: {colors['accent_secondary']};">Curator's Insight</h4>
            <p style="line-height: 1.8; text-align: justify;">
                (G)I-DLE 的獨特之處在於成員們高度的<b>「自製能力 (Self-Producing)」</b>。
                雷達圖顯示，除了傳統偶像的能力值外，她們在創作與概念構建上展現了極高的數值。
            </p>
            <hr>
            <div style="font-size: 3rem; font-family: 'Playfair Display'; color: {colors['accent_primary']};">95%</div>
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Creative Participation</div>
        </div>
        """, unsafe_allow_html=True)

elif selected_nav == "i-concierge":
    # ----------------------------------------------------
    # D. i-concierge: Curator's Guide (策展人指引)
    # ----------------------------------------------------
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h1 style="font-size: 4rem; margin-bottom: 0; color: {colors['accent_primary']}">Curator's Guide</h1>
        <div class="handwriting" style="font-size: 2rem;">Resources & Links</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    # 定義卡片樣式函數
    def resource_card(title, sub, icon):
        return f"""
        <div style="background: white; padding: 30px; border-radius: 16px; text-align: center; border-bottom: 4px solid {colors['accent_secondary']}; transition: transform 0.3s;">
            <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
            <h3 style="margin: 10px 0;">{title}</h3>
            <p style="color: {colors['text_sub']}; font-size: 0.9rem;">{sub}</p>
        </div>
        """
    
    with c1:
        st.markdown(resource_card("Official", "YouTube / X / Instagram", "🌐"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("VISIT OFFICIAL SITE", use_container_width=True)
        
    with c2:
        st.markdown(resource_card("Ticketing", "World Tour [i-DOL]", "🎫"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("VIEW TOUR DATES", use_container_width=True)
        
    with c3:
        st.markdown(resource_card("Fanclub", "NEVERLAND Membership", "💜"), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("JOIN MEMBERSHIP", use_container_width=True)

    # 底部聯絡表單
    st.markdown("---")
    st.markdown("### Guestbook")
    with st.form("guestbook"):
        st.text_area("Leave a message for the gallery:", placeholder="Write something...")
        submitted = st.form_submit_button("SIGN GUESTBOOK")
        if submitted:
            st.success("Your message has been recorded in the gallery archives.")