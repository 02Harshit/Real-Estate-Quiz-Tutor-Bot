import streamlit as st
import json
from src.database import process_and_store_json
from src.tutor_logic import generate_question, evaluate_answer, get_available_question_types

# --- Page Config ---
st.set_page_config(
    page_title="Real Estate Tutor 2026",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions ---
def create_fallback_question(question_type: str):
    """Creates a reliable fallback question."""
    if question_type == "calculation":
        return (
            "A property is listed at $450,000 with 2,500 square feet. "
            "What is the price per square foot?\n\n"
            "A) $150 per sq ft\n"
            "B) $180 per sq ft\n"
            "C) $200 per sq ft\n"
            "D) $225 per sq ft",
            "B",
            "Price per Square Foot, Basic Calculations",
            {},
            "Solution: $450,000 ÷ 2,500 = $180 per square foot",
            "calculation"
        )
    else:
        return (
            "Property A is zoned commercial, Property B is zoned residential. "
            "Which property can legally operate a retail store?\n\n"
            "A) Property A only\n"
            "B) Property B only\n"
            "C) Both properties\n"
            "D) Neither property",
            "A",
            "Zoning Analysis, Property Use, Commercial Real Estate",
            {},
            "",
            "comparative"
        )

# --- CSS Styling ---
st.markdown("""
<style>
    /* Base Reset */
    .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }
    
    .stApp * {
        color: #e6edf3 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .main .block-container {
        background-color: #0d1117;
        padding: 2rem;
        max-width: 1200px;
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
        min-width: 120px;
    }
    
    .stButton > button:hover {
        background-color: #388bfd !important;
    }
    
    .stButton > button:disabled {
        background-color: #21262d !important;
        border-color: #30363d !important;
        color: #484f58 !important;
    }

    /* Radio Buttons */
    .stRadio > div {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
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

    /* Tags */
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
    .tag-green { color: #3fb950; background-color: rgba(46, 160, 67, 0.1); }
    .tag-purple { color: #bc8cff; background-color: rgba(188, 140, 255, 0.1); }
    
    /* Question type badge */
    .question-type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-left: 12px;
    }
    .type-comparative {
        background-color: rgba(88, 166, 255, 0.1);
        color: #58a6ff;
        border: 1px solid #58a6ff;
    }
    .type-calculation {
        background-color: rgba(63, 185, 80, 0.1);
        color: #3fb950;
        border: 1px solid #3fb950;
    }
    
    /* Solution box */
    .solution-box {
        background-color: #1a2634;
        border-left: 4px solid #3fb950;
        border-radius: 6px;
        padding: 16px;
        margin: 16px 0;
        font-family: monospace;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🔐 Access")
    
    # Get API key from secrets or input
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        api_key = st.text_input(
            "API Key", 
            type="password",
            placeholder="Enter Gemini API Key...",
            label_visibility="collapsed"
        )
    
    if not api_key:
        st.error("Please add your API key to continue")
        st.stop()
    else:
        st.success("✅ Connected")
    
    st.markdown("---")
    st.markdown("### 👤 Profile")
    
    experience = st.selectbox(
        "Experience Level", 
        ["Beginner", "Intermediate", "Advanced"],
        index=1
    )
    
    st.markdown("---")
    st.markdown("### 📁 Data")
    
    uploaded_file = st.file_uploader("Upload Listings (JSON)", type="json")
    if uploaded_file:
        with st.spinner("Processing..."):
            try:
                data = json.load(uploaded_file)
                # This function needs to be implemented in database.py
                st.success(f"✓ File uploaded successfully")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

# --- Main Content ---
# Header
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.title("🏡 Real Estate Tutor")
    st.caption("Master real estate concepts with AI guidance")

with col2:
    st.markdown("### 🎯 Question Type")
    question_types = {
        "Auto (Random)": "auto",
        "Comparative Analysis": "comparative",
        "Calculation Based": "calculation"
    }
    
    # Use a unique key for the selectbox
    selected_type_display = st.selectbox(
        "Select question type",
        options=list(question_types.keys()),
        index=0,
        key="question_type_selector",
        label_visibility="collapsed"
    )
    selected_type = question_types[selected_type_display]

with col3:
    if "gaps" in st.session_state and st.session_state.gaps:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value" style="color: #d29922;">{len(st.session_state.gaps)}</div>
            <div class="metric-label">Focus Areas</div>
        </div>
        """, unsafe_allow_html=True)

# Handle question type switching
if "switch_type" in st.session_state:
    del st.session_state.switch_type
    # Generate new question with opposite type
    current_type = st.session_state.get("question_type", "comparative")
    new_type = "calculation" if current_type == "comparative" else "comparative"
    with st.spinner("Switching question type..."):
        q, ans, obj, ctx, solution, q_type = generate_question(api_key, question_type=new_type)
        st.session_state.q = q
        st.session_state.ans = ans
        st.session_state.objectives = obj
        st.session_state.ctx = ctx
        st.session_state.solution = solution
        st.session_state.question_type = q_type
    st.rerun()

# Generate button
st.markdown("---")
gen_col1, gen_col2, _ = st.columns([1, 2, 3])
with gen_col1:
    if st.button("✨ Generate New Question", key="new_q"):
        # Clear previous state
        for key in ['q', 'ans', 'objectives', 'ctx', 'submitted', 'feedback', 'user_choice', 'solution', 'question_type']:
            if key in st.session_state:
                del st.session_state[key]
        
        with st.spinner("Crafting scenario..."):
            # Generate question
            q, ans, obj, ctx, solution, q_type = generate_question(
                api_key, 
                question_type=None if selected_type == "auto" else selected_type
            )
            
            # Store in session state
            st.session_state.q = q
            st.session_state.ans = ans
            st.session_state.objectives = obj
            st.session_state.ctx = ctx
            st.session_state.solution = solution
            st.session_state.question_type = q_type
        st.rerun()

with gen_col2:
    # Show current question type
    if "question_type" in st.session_state:
        q_type_display = "Comparative Analysis" if st.session_state.question_type == "comparative" else "Calculation"
        badge_class = "type-comparative" if st.session_state.question_type == "comparative" else "type-calculation"
        st.markdown(f"""
        <div style="margin-top: 8px;">
            <span class="question-type-badge {badge_class}">📊 {q_type_display}</span>
        </div>
        """, unsafe_allow_html=True)

# --- Question Display ---
if "q" in st.session_state:
    st.markdown("---")
    
    # Header with objectives
    if "objectives" in st.session_state and st.session_state.objectives:
        objs = [o.strip() for o in st.session_state.objectives.split(",") if o.strip()]
        if objs:
            obj_tags = "".join([f'<span class="tag tag-blue">{o}</span>' for o in objs[:3]])
            st.markdown(f'<div style="margin-bottom: 16px;">{obj_tags}</div>', unsafe_allow_html=True)
    
    # Question text
    st.markdown("### 📝 Practice Scenario")
    st.markdown(st.session_state.q)
    
    # Show solution preview for calculation questions
    if st.session_state.get("question_type") == "calculation" and st.session_state.get("solution"):
        with st.expander("📐 View Formula Reference (Try solving first!)"):
            st.markdown(f'<div class="solution-box">{st.session_state.solution}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Answer Selection
    st.markdown("#### Select your answer:")
    
    user_choice = st.radio(
        "Choose an option",
        ["A", "B", "C", "D"],
        key="user_choice",
        index=None,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Submit Button
    if st.button("Submit Answer", disabled=user_choice is None, key="submit"):
        assessment_payload = {
            "question": st.session_state.q,
            "user_answer": user_choice,
            "correct_answer": st.session_state.ans,
            "question_type": st.session_state.get("question_type", "comparative"),
            "user_profile": {
                "experience_level": experience.lower(),
                "previous_gaps": st.session_state.get("gaps", [])
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
    
    # Get assessment data
    assessment = feedback.get("assessment", {})
    explanation = feedback.get("explanation", {})
    followup = feedback.get("personalized_followup", {})
    
    is_correct = assessment.get("correct", False)
    score = assessment.get("score", 0)
    
    # Result header
    if is_correct:
        st.success(f"### ✅ Correct")
    else:
        st.error(f"### ❌ Incorrect")
    
    # Gap analysis
    if assessment.get("gap_analysis"):
        st.markdown("#### 📊 Analysis")
        st.write(assessment["gap_analysis"])
    
    st.markdown("---")
    
    # Explanation
    st.markdown("#### 📚 Explanation")
    if explanation.get("contextual_correction"):
        st.write(explanation["contextual_correction"])
    
    # Industry insights
    if explanation.get("industry_insights"):
        st.markdown("#### 💼 Industry Insight")
        st.write(explanation["industry_insights"])
    
    # Show solution for calculation questions
    if st.session_state.get("question_type") == "calculation" and st.session_state.get("solution"):
        with st.expander("🔍 View Step-by-Step Solution"):
            st.markdown(f'<div class="solution-box">{st.session_state.solution}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Next Steps
    st.markdown("### 🚀 Next Steps")
    
    if followup.get("suggested_topics"):
        topics = followup["suggested_topics"][:3]
        topics_html = "".join([f'<span class="tag tag-purple">{t}</span>' for t in topics])
        st.markdown(f"**Recommended Topics:** {topics_html}", unsafe_allow_html=True)
    
    if followup.get("next_question"):
        st.info(f"**Suggested Focus:** {followup['next_question']}")
    
    # Store gaps for learning
    if not is_correct:
        if "gaps" not in st.session_state:
            st.session_state.gaps = []
        gap = assessment.get("gap_analysis", "")
        if gap and gap not in st.session_state.gaps:
            st.session_state.gaps.append(gap)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Try Similar"):
            # Clear answer-related state only
            for key in ['submitted', 'feedback', 'user_choice']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        if st.button("🎯 New Question"):
            # Clear all question-related state
            for key in ['q', 'ans', 'objectives', 'ctx', 'submitted', 'feedback', 'user_choice', 'solution']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col3:
        if st.button("🔄 Switch Type"):
            # Set flag to switch type
            st.session_state.switch_type = True
            # Clear question state
            for key in ['q', 'ans', 'objectives', 'ctx', 'submitted', 'feedback', 'user_choice', 'solution']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Select question type from the dropdown and click 'Generate New Question' to start")