import streamlit as st
import json
from src.database import process_and_store_json
from src.tutor_logic import generate_question, evaluate_answer

# --- Page Config ---
st.set_page_config(
    page_title="Real Estate Tutor 2026",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Clean Dark Theme CSS ---
st.markdown("""
<style>
    /* Base Reset */
    .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }
    
    /* Force all text to light */
    .stApp * {
        color: #e6edf3 !important;
    }
    
    /* Specific element overrides for contrast */
    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: #e6edf3 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Main container */
    .main .block-container {
        background-color: #0d1117;
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* Clean Cards - No transparency issues */
    .clean-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    }
    
    .clean-card-blue {
        background-color: #0d1117;
        border: 1px solid #1f6feb;
        border-left: 4px solid #1f6feb;
    }
    
    .clean-card-green {
        background-color: #0d1117;
        border: 1px solid #238636;
        border-left: 4px solid #238636;
    }
    
    .clean-card-red {
        background-color: #0d1117;
        border: 1px solid #da3633;
        border-left: 4px solid #da3633;
    }
    
    .clean-card-amber {
        background-color: #0d1117;
        border: 1px solid #9e6a03;
        border-left: 4px solid #9e6a03;
    }
    
    /* Buttons - Reduced size */
    .stButton > button {
        background-color: #1f6feb !important;
        color: #ffffff !important;
        border: 1px solid #388bfd !important;
        border-radius: 6px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        width: auto !important;
        min-width: 120px;
    }
    
    .stButton > button:hover {
        background-color: #388bfd !important;
        border-color: #58a6ff !important;
    }
    
    .stButton > button:disabled {
        background-color: #21262d !important;
        color: #8b949e !important;
        border-color: #30363d !important;
        cursor: not-allowed !important;
    }
    
    /* Secondary button style */
    .btn-secondary > button {
        background-color: #238636 !important;
        border-color: #2ea043 !important;
    }
    
    .btn-secondary > button:hover {
        background-color: #2ea043 !important;
    }
    
    /* Form Inputs - Dark theme */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stFileUploader > div > button {
        background-color: #21262d !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #1f6feb !important;
        box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.3) !important;
    }
    
    /* Selectbox dropdown */
    .stSelectbox > div > div > div {
        background-color: #21262d !important;
        color: #e6edf3 !important;
    }
    
    /* Radio Buttons - Clean dark style */
    .stRadio > div {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
    }
    
    .stRadio > label {
        color: #8b949e !important;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 12px;
    }
    
    .stRadio > div > div {
        display: flex;
        gap: 12px;
    }
    
    .stRadio > div > div > label {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 10px 20px;
        color: #c9d1d9 !important;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        flex: 1;
        text-align: center;
        font-size: 13px;
    }
    
    .stRadio > div > div > label:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }
    
    /* Selected radio state */
    .stRadio > div > div > label[data-baseweb="radio"] {
        background-color: rgba(31, 111, 235, 0.1);
        border-color: #1f6feb;
        color: #58a6ff !important;
    }
    
    /* Sidebar - Solid dark */
    .css-1d391kg, section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    .css-1d391kg .clean-card {
        background-color: #0d1117;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background-color: #21262d !important;
        border: 2px dashed #30363d !important;
        border-radius: 8px !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #1f6feb !important;
        background-color: #161b22 !important;
    }
    
    /* Success/Error/Info messages - Override Streamlit defaults */
    .stSuccess, .stError, .stInfo, .stWarning {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .stSuccess > div, .stError > div, .stInfo > div, .stWarning > div {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    /* Specific message colors */
    .stSuccess > div {
        border-left: 4px solid #238636 !important;
    }
    
    .stError > div {
        border-left: 4px solid #da3633 !important;
    }
    
    .stInfo > div {
        border-left: 4px solid #1f6feb !important;
    }
    
    .stWarning > div {
        border-left: 4px solid #9e6a03 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        color: #58a6ff !important;
    }
    
    /* Chips/Tags */
    .tag {
        display: inline-block;
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 500;
        color: #8b949e;
        margin: 4px 4px 4px 0;
    }
    
    .tag-blue {
        background-color: rgba(31, 111, 235, 0.1);
        border-color: rgba(31, 111, 235, 0.4);
        color: #58a6ff;
    }
    
    .tag-green {
        background-color: rgba(35, 134, 54, 0.1);
        border-color: rgba(35, 134, 54, 0.4);
        color: #3fb950;
    }
    
    .tag-amber {
        background-color: rgba(158, 106, 3, 0.1);
        border-color: rgba(158, 106, 3, 0.4);
        color: #d29922;
    }
    
    .tag-purple {
        background-color: rgba(139, 92, 246, 0.1);
        border-color: rgba(139, 92, 246, 0.4);
        color: #a78bfa;
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        background-color: #21262d;
        border: 1px solid #30363d;
        color: #8b949e;
    }
    
    .status-badge.active {
        background-color: rgba(35, 134, 54, 0.15);
        border-color: rgba(35, 134, 54, 0.4);
        color: #3fb950;
    }
    
    /* Section headers */
    .section-header {
        font-size: 14px;
        font-weight: 600;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 24px 0 12px 0;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #30363d;
        margin: 24px 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 5px;
        border: 2px solid #0d1117;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Question text formatting */
    .question-text p {
        line-height: 1.6;
        margin: 8px 0;
        color: #c9d1d9;
    }
    
    .question-text strong {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Metric cards */
    .metric-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }
    
    .metric-label {
        font-size: 12px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Fix for HTML escaping issues */
    .stMarkdown code {
        color: #ff7b72 !important;
        background-color: rgba(255, 123, 114, 0.1) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
        font-family: 'SF Mono', Monaco, monospace !important;
    }
    
    /* Remove empty div artifacts */
    .element-container:empty,
    .stMarkdown:empty {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("### 🔐 Access")
    
    api_key = st.secrets.get("GEMINI_API_KEY") or st.text_input(
        "API Key", 
        type="password",
        placeholder="Enter Gemini API Key...",
        label_visibility="collapsed"
    )
    
    if not api_key:
        st.markdown('<span class="status-badge">● Disconnected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge active">● Connected</span>', unsafe_allow_html=True)
    
    if not api_key:
        st.error("Please add your API key to continue")
        st.stop()
    
    st.markdown("---")
    st.markdown("### 👤 Profile")
    
    experience = st.selectbox(
        "Experience Level", 
        ["Beginner", "Intermediate", "Advanced"],
        index=1
    )
    
    pref = st.selectbox(
        "Learning Style",
        ["Detailed", "Concise", "Example-based"]
    )
    
    st.markdown("---")
    st.markdown("### 📁 Data")
    
    uploaded_file = st.file_uploader("Upload Listings (JSON)", type="json")
    if uploaded_file:
        with st.spinner("Processing..."):
            data = json.load(uploaded_file)
            count = process_and_store_json(data, api_key)
            st.success(f"✓ Indexed {count} properties")

# --- Main Content ---
# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏡 Real Estate Tutor")
    st.caption("Master comparative market analysis with AI guidance")

with col2:
    if "gaps" in st.session_state:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color: #d29922;">{len(st.session_state.gaps)}</div>
            <div class="metric-label">Focus Areas</div>
        </div>
        """, unsafe_allow_html=True)

# Generate Button
st.markdown("---")
gen_col, _ = st.columns([1, 4])
with gen_col:
    if st.button("✨ Generate New Question", key="new_q"):
        for key in ['q', 'ans', 'objectives', 'ctx', 'submitted', 'feedback', 'user_choice']:
            if key in st.session_state:
                del st.session_state[key]
        
        with st.spinner("Crafting scenario..."):
            q, ans, obj, ctx = generate_question(api_key)
            st.session_state.q = q
            st.session_state.ans = ans
            st.session_state.objectives = obj
            st.session_state.ctx = ctx
        st.rerun()

# --- Question Display ---
if "q" in st.session_state:
    st.markdown("---")
    
    # Header with objectives
    header_col1, header_col2 = st.columns([1, 2])
    with header_col1:
        st.markdown("### 📝 Practice Scenario")
    
    with header_col2:
        if "objectives" in st.session_state and st.session_state.objectives:
            objs = [o.strip() for o in st.session_state.objectives.split(",") if o.strip()]
            if objs:
                obj_tags = "".join([f'<span class="tag tag-blue">{o}</span>' for o in objs])
                st.markdown(f'<div style="text-align: right;">{obj_tags}</div>', unsafe_allow_html=True)
    
    # Question text - using native Streamlit markdown
    st.markdown(st.session_state.q)
    
    st.markdown("---")
    
    # Answer Selection
    st.markdown("#### Select your answer:")
    
    user_choice = st.radio(
        "",
        ["A", "B", "C", "D"],
        key="user_choice",
        index=None,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Submit Button
    submit_disabled = user_choice is None
    submit_col, _ = st.columns([1, 4])
    with submit_col:
        if st.button("Submit Answer", disabled=submit_disabled, key="submit"):
            assessment_payload = {
                "context": st.session_state.ctx,
                "question": st.session_state.q,
                "user_response": user_choice,
                "learning_objectives": st.session_state.objectives.split(",") if st.session_state.objectives else [],
                "user_profile": {
                    "experience_level": experience.lower(),
                    "previous_gaps": st.session_state.get("gaps", []),
                    "learning_preferences": pref.lower()
                }
            }
            
            with st.spinner("Analyzing response..."):
                result = evaluate_answer(api_key, assessment_payload)
                st.session_state.feedback = result
                st.session_state.submitted = True
            st.rerun()

# --- Feedback Display ---
if st.session_state.get("submitted") and "feedback" in st.session_state:
    feedback = st.session_state.feedback
    
    if "assessment" in feedback:
        is_correct = feedback["assessment"]["correct"]
        
        # Result header
        if is_correct:
            st.success("### ✅ Correct")
        else:
            st.error("### ❌ Incorrect")
        
        # Gap analysis
        if feedback["assessment"].get("gap_analysis"):
            st.write(feedback["assessment"]["gap_analysis"])
        
        st.markdown("---")
        
        # Explanation columns
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            st.markdown("#### 📚 Correction")
            if feedback["explanation"].get("contextual_correction"):
                st.write(feedback["explanation"]["contextual_correction"])
        
        with exp_col2:
            st.markdown("#### 💼 Industry Insight")
            if feedback["explanation"].get("industry_insights"):
                st.write(feedback["explanation"]["industry_insights"])
        
        st.markdown("---")
        
        # Follow-up section
        st.markdown("### 🚀 Next Steps")
        
        followup = feedback.get('personalized_followup', {})
        
        if followup.get('suggested_topics'):
            topics_html = "".join([f'<span class="tag tag-purple">{t}</span>' for t in followup['suggested_topics']])
            st.markdown(topics_html, unsafe_allow_html=True)
        
        if followup.get('next_question'):
            st.info(f"**Recommended Focus:** {followup['next_question']}")
        
        # Store gaps
        if not is_correct:
            if "gaps" not in st.session_state:
                st.session_state.gaps = []
            current_gap = feedback['assessment'].get('gap_analysis', '')
            if current_gap and current_gap not in st.session_state.gaps:
                st.session_state.gaps.append(current_gap)