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
    
    /* Clean Cards */
    .clean-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1f6feb !important;
        color: #ffffff !important;
        border: 1px solid #388bfd !important;
        border-radius: 6px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
        min-width: 120px;
    }
    
    .stButton > button:hover {
        background-color: #388bfd !important;
        border-color: #58a6ff !important;
    }

    /* Radio Buttons - Clean dark style */
    .stRadio > div {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
    }

    /* Sidebar - Solid dark */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }

    /* HEADER & SIDEBAR TOGGLE FIX */
    /* Make header transparent so it doesn't show a white bar, but keep it functional */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: #e6edf3 !important;
    }

    /* Style the 'Expand' button (the chevron) specifically */
    button[data-testid="stBaseButton-headerNoPadding"] {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        border: 1px solid #30363d !important;
        margin-left: 10px !important;
    }

    /* Hide Streamlit Footer and Menu, but NOT the header */
    #MainMenu, footer {
        visibility: hidden;
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

    /* Tags/Chips */
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
    .tag-blue { color: #58a6ff; background-color: rgba(31, 111, 235, 0.1); }
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