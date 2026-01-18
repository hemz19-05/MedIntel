import streamlit as st
from intent import detect_intent
from drug_api import get_drug_label
from ai_agent import generate_response
from analytics import log_query, get_analytics
from db import init_db
from dotenv import load_dotenv
import os


load_dotenv()

# Page config with custom theme
st.set_page_config(
    page_title="💊 MedIntel",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
}

/* ===== App background - Vibrant gradient ===== */
.stApp {
    background: linear-gradient(135deg, #0a2540 0%, #1a4d6d 25%, #0d3b66 50%, #1fb9b3 100%);
}

/* ===== Main content ===== */
.main > div {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    padding: 0;
    border-radius: 0;
    box-shadow: none;
}

/* ===== Text colors ===== */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #ffffff !important;
}

/* ===== Hero Section - SHINY BLACK ===== */
.hero-container {
    background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #0d1117 100%);
    padding: 3rem 3rem;
    border-radius: 0;
    margin: -2rem -2rem 3rem -2rem;
    border-bottom: 3px solid rgba(31, 185, 179, 0.6);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8), 0 0 50px rgba(31, 185, 179, 0.2);
    position: relative;
}

.hero-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, transparent 0%, rgba(31, 185, 179, 0.05) 100%);
    pointer-events: none;
}

.app-logo {
    font-size: 4rem !important;
    font-weight: 900 !important;
    color: #1fb9b3 !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 2px 10px rgba(31, 185, 179, 0.5);
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1.3rem;
    font-weight: 300;
    color: rgba(255, 255, 255, 0.8) !important;
    letter-spacing: 0.5px;
}

.hero-badge {
    display: inline-block;
    background: rgba(255, 152, 0, 0.25);
    color: #ffa726;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 1px solid rgba(255, 152, 0, 0.5);
    margin-bottom: 1.5rem;
    letter-spacing: 1px;
}

/* ===== Input Styling ===== */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: #0d3b66 !important;
    border: 2px solid rgba(255, 152, 0, 0.4) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #ffa726 !important;
    background-color: rgba(255, 255, 255, 1) !important;
    box-shadow: 0 0 0 3px rgba(255, 152, 0, 0.2) !important;
}

.stTextInput > label,
.stTextArea > label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* ===== Button Styling ===== */
button[kind="primary"] {
    background: linear-gradient(135deg, #ffa726 0%, #ff8a00 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.8rem 2.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
    letter-spacing: 0.5px;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(255, 152, 0, 0.6) !important;
    background: linear-gradient(135deg, #ffb74d 0%, #ffa726 100%) !important;
}

/* ===== Result Card - Orange Accent ===== */
.result-card {
    background: linear-gradient(135deg, rgba(255, 152, 0, 0.15) 0%, rgba(31, 185, 179, 0.1) 100%);
    border: 2px solid rgba(255, 152, 0, 0.5);
    border-radius: 16px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 8px 20px rgba(255, 152, 0, 0.2);
    color: #ffffff !important;
}

.result-card h3 {
    color: #ffa726 !important;
    margin-bottom: 1rem !important;
}

.result-card p {
    color: #ffffff !important;
    line-height: 1.8;
    font-size: 1.05rem;
}

/* ===== Section Headers ===== */
.section-header {
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffa726 !important;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.8rem;
    border-bottom: 2px solid rgba(255, 152, 0, 0.4);
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2540 0%, #0d3b66 50%, #1a5f7a 100%);
    border-right: 2px solid rgba(31, 185, 179, 0.3);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stSidebarNav"] {
    display: none;
}

section[data-testid="stSidebar"] button[kind="header"] {
    display: none !important;
}

/* ===== Stats Cards ===== */
.stat-card {
    background: linear-gradient(135deg, rgba(31, 185, 179, 0.15) 0%, rgba(31, 185, 179, 0.05) 100%);
    border: 1px solid rgba(31, 185, 179, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #1fb9b3 !important;
    line-height: 1;
}

.stat-label {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.7) !important;
    margin-top: 0.5rem;
    font-weight: 500;
}

/* ===== Info Badge ===== */
.info-badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 20px;
    background: rgba(31,185,179,0.2);
    border: 1px solid rgba(31,185,179,0.5);
    color: #1fb9b3;
    font-weight: 600;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
}

/* ===== Spinner - Enhanced targeting ===== */
.stSpinner > div {
    border-top-color: #ffffff !important;
    border-right-color: rgba(255, 255, 255, 0.3) !important;
    border-bottom-color: rgba(255, 255, 255, 0.3) !important;
    border-left-color: rgba(255, 255, 255, 0.3) !important;
}

.stSpinner > div > div {
    border-top-color: #1fb9b3 !important;
}

/* Additional spinner targeting */
div[data-testid="stSpinner"] > div {
    border-color: rgba(255, 255, 255, 0.3) !important;
    border-top-color: #ffffff !important;
}

/* Force spinner color */
.stSpinner svg {
    color: #ffffff !important;
}

div[data-testid="stSpinner"] svg {
    color: #ffffff !important;
}
/* ===== Metrics ===== */
[data-testid="stMetricValue"] {
    color: #1fb9b3 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 600 !important;
}

/* ===== Radio buttons in sidebar ===== */
.stRadio > label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
}

/* ===== Divider ===== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(31, 185, 179, 0.3), transparent);
    margin: 2rem 0;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 3rem !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
    st.markdown('## 🧠 MedIntel')
    st.caption('Medical Information Assistant')
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        ["🔍 Drug Search", "📊 Analytics", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown(
        """
        <div style='background: rgba(31, 185, 179, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(31, 185, 179, 0.3);'>
            <p style='font-weight: 600; margin-bottom: 0.5rem;'>⚕️ Medical Disclaimer</p>
            <p style='font-size: 0.85rem; opacity: 0.9; line-height: 1.5;'>
                MedIntel provides general drug information for educational purposes only. 
                It does not provide medical advice, diagnosis, or treatment. 
                Always consult a qualified healthcare professional.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        """
        <div style='text-align: center; opacity: 0.6; font-size: 0.85rem;'>
            <p>Powered by</p>
            <p style='font-weight: 600; color: #1fb9b3 !important;'>OpenFDA • RxNorm • AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

init_db()

# ---------- HERO SECTION ----------
st.markdown("""
<div class='hero-container'>
    <div class='app-logo'>🧠 MedIntel</div>
    <div class='hero-badge'>💊 DRUG INFORMATION SYSTEM</div>
    <div class='hero-subtitle'>FDA-verified drug data with AI-powered explanations</div>
</div>
""", unsafe_allow_html=True)

# ---------- DRUG SEARCH PAGE ----------
if page == "🔍 Drug Search":
    st.markdown("<div class='section-header'>🔍 Search Drug Information</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        drug_name = st.text_input("💊 Drug Name", placeholder="e.g., Amoxicillin")
        question = st.text_area(
            "❓ Your Question (Optional)",
            placeholder="e.g., Can this be taken during pregnancy?",
            height=120
        )
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        search = st.button("🔍 Search Now", type="primary", use_container_width=True)

    with col2:
        if search and drug_name:
            with st.spinner('🔄 Retrieving information...'):
                try:
                    # Detect intent
                    intent = detect_intent(question or drug_name)
                    
                    # Show intent badge
                    st.markdown(
                        f"""
                        <div class='info-badge'>
                            🎯 Detected intent: {intent.replace('_', ' ').title()}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Get drug data
                    drug_data = get_drug_label(drug_name)

                    # Generate AI response
                    response, variant = generate_response(
                          user_input=question or f"Tell me about {drug_name}",
                          context=drug_data
                    )

                    log_query(drug_name, variant)


                    st.success('✅ Information retrieved successfully')

                    # Display AI Explanation
                    st.markdown("<div class='section-header'>🧠 AI Educational Summary</div>", unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div class='result-card'>
                            {response}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption("⚠️ This information is for educational purposes only. Always consult a healthcare professional.")

                except Exception as e:
                    st.error(f'❌ Error: {e}')
        elif not drug_name and search:
            st.warning("⚠️ Please enter a drug name to search.")

# ---------- ANALYTICS PAGE ----------
elif page == "📊 Analytics":
    st.markdown("<div class='section-header'>📊 Usage Analytics</div>", unsafe_allow_html=True)

    try:
        stats = get_analytics()

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div class='stat-card'>
                    <div class='stat-number'>{stats.get('total_queries', 0)}</div>
                    <div class='stat-label'>Total Searches</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class='stat-card'>
                    <div class='stat-number'>{stats.get('unique_drugs', 0)}</div>
                    <div class='stat-label'>Unique Drugs</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div class='stat-card'>
                    <div class='stat-number'>{stats.get('total_queries', 0)}</div>
                    <div class='stat-label'>AI Responses</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        st.markdown("<div class='section-header'>🔬 Drugs Queried</div>", unsafe_allow_html=True)
        
        drug_list = stats.get('drug_list', [])
        if drug_list:
            for idx, drug in enumerate(drug_list, 1):
                st.markdown(f"**{idx}.** {drug.title()}")
        else:
            st.info("📊 No data yet. Start searching for drugs to see analytics!")

    except Exception as e:
        st.error(f"Unable to load analytics: {e}")

# ---------- ABOUT PAGE ----------
elif page == "ℹ️ About":
    st.markdown("<div class='section-header'>ℹ️ About MedIntel</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='result-card'>
        <h3>🧠 What is MedIntel?</h3>
        <p>
            MedIntel is an <strong>AI-powered drug intelligence assistant</strong> that combines 
            official FDA drug label data with advanced language models to provide clear, 
            educational explanations about medications.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='result-card'>
        <h3>✨ Key Features</h3>
        <p>
            • <strong>FDA Verified Data:</strong> All information sourced from official FDA databases<br>
            • <strong>AI-Powered Analysis:</strong> Advanced natural language processing for clear insights<br>
            • <strong>Intent Detection:</strong> Understands your specific questions about medications<br>
            • <strong>Educational Focus:</strong> Designed to inform, not to replace medical advice
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='result-card' style='border-color: rgba(255, 82, 82, 0.5); background: linear-gradient(135deg, rgba(255, 82, 82, 0.15) 0%, rgba(255, 152, 0, 0.1) 100%);'>
        <h3>⚠️ Important Disclaimer</h3>
        <p>
            MedIntel is <strong>not medical advice</strong>. This tool provides general drug 
            information for educational purposes only. It does not diagnose, treat, or provide 
            medical advice. Always consult a qualified healthcare professional for medical decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

