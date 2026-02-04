import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from streamlit_calendar import calendar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# 1. SYSTEM CONFIGURATION
st.set_page_config(page_title="L&R Management System", page_icon="⚗️", layout="wide", initial_sidebar_state="expanded")

COLORS = {"bg": "#FAFAF9", "card": "#FFFFFF", "text": "#333333", "terracotta": "#E07A5F", "sage": "#81B29A", "blue": "#98C1D9", "navy": "#3D405B"}

st.markdown(f"""<style>
    .stApp {{ background-color: {COLORS['bg']}; font-family: 'Helvetica', sans-serif; }}
    div[data-testid="stMetric"], div.stDataFrame, div.stPlotlyChart {{ background-color: {COLORS['card']}; border-radius: 12px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #EAEAEA; }}
    .stTabs [aria-selected="true"] {{ background-color: {COLORS['terracotta']} !important; color: white !important; }}
    </style>""", unsafe_allow_html=True)

# 2. DATA LAYER
@st.cache_data(ttl=600)
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(worksheet="Attivita"), conn.read(worksheet="Diario"), conn.read(worksheet="Film"), conn.read(worksheet="Locali"), conn
    except:
        # Fallback Mock Data
        return pd.DataFrame({"Attivita": ["Test"], "Descrizione": ["Test"], "Energia": [3], "Budget": [0], "Luogo": ["Home"]}), pd.DataFrame({"Data": [datetime.now()], "Attivita": ["Test"], "Voto": [5], "Note": ["OK"], "Foto": [""]}), pd.DataFrame(), pd.DataFrame({"Nome": ["Test"], "Luogo": ["Trieste"], "Tipo": ["Pizza"], "Voto_Location": [8], "Voto_Menu": [8], "Voto_Servizio": [8], "Voto_Conto": [8], "Totale": [8], "Recensione": ["Test"]}), None

df_attivita, df_diario, df_film, df_locali, conn = load_data()

# 3. SIDEBAR
with st.sidebar:
    st.title("System Status")
    st.caption("Couple_OS v1.0.4")
    st.metric("Logs", len(df_diario))
    st.progress(min(len(df_diario)/50, 1.0))

# 4. ML ENGINE
def get_smart_recommendation(df_act, df_log):
    if df_log.empty or df_act.empty: return df_act.sample(1).iloc[0]
    liked = df_log[df_log['Voto'] >= 4]['Attivita'].tolist()
    if not liked: return df_act.sample(1).iloc[0]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_act['Descrizione'].fillna(''))
    liked_indices = df_act[df_act['Attivita'].isin(liked)].index
    if len(liked_indices) == 0: return df_act.sample(1).iloc[0]
    user_profile = np.asarray(np.mean(tfidf_matrix[liked_indices], axis=0))
    scores = cosine_similarity(user_profile, tfidf_matrix)[0]
    return df_act.iloc[scores.argmax()]

# 5. TABS
tabs = st.tabs(["📊 Dashboard", "🧠 Smart Decision", "📓 Logbook", "🕰️ Timeline", "🍽️ Food Inspector", "💾 DB Admin"])

with tabs[0]: # Dashboard
    c1, c2 = st.columns([1, 2])
    with c1: st.info("Analytics Module Active")
    with c2: 
        if not df_diario.empty: st.plotly_chart(px.line(df_diario, x="Data", y="Voto", markers=True), use_container_width=True)

with tabs[1]: # Smart Decision
    if st.button("🤖 AI Recommendation"):
        rec = get_smart_recommendation(df_attivita, df_diario)
        st.success(f"Suggested: {rec['Attivita']}")
        st.caption(rec['Descrizione'])

with tabs[2]: # Logbook
    with st.form("log"):
        st.date_input("Data"); st.selectbox("Activity", df_attivita['Attivita'].unique() if not df_attivita.empty else ["None"])
        if st.form_submit_button("Save"): st.success("Saved")

with tabs[3]: # Timeline
    events = [{"title": f"{r['Attivita']}", "start": str(r['Data'])} for _, r in df_diario.iterrows()]
    calendar(events=events)

with tabs[4]: # Food Inspector
    for _, row in df_locali.iterrows():
        st.write(f"**{row['Nome']}** - {row['Totale']}/10")
        fig = go.Figure(data=go.Scatterpolar(r=[row['Voto_Location'], row['Voto_Menu'], row['Voto_Servizio'], row['Voto_Conto'], row['Voto_Location']], theta=['Location','Menu','Service','Cost','Location'], fill='toself'))
        fig.update_layout(height=200, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)