import streamlit as st
import json
from src.database import process_and_store_json
from src.tutor_logic import generate_question, evaluate_answer

st.set_page_config(page_title="Real Estate Tutor 2026", layout="wide")

# --- API Key Setup ---
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")
if not api_key:
    st.info("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# --- Sidebar: Data & Profile ---
st.sidebar.header("🛠️ Admin & Profile")
uploaded_file = st.sidebar.file_uploader("Upload Listings (JSON)", type="json")
if uploaded_file:
    data = json.load(uploaded_file)
    count = process_and_store_json(data, api_key)
    st.sidebar.success(f"Indexed {count} properties.")

experience = st.sidebar.selectbox("Your Experience Level", ["beginner", "intermediate", "advanced"])
pref = st.sidebar.selectbox("Learning Preference", ["detailed", "concise", "example-based"])

# --- Main Tutor Interface ---
st.title("🏡 Real Estate Exam Prep")

if st.button("Get New Question"):
    # Clear old state but keep user profile
    for key in ['q', 'ans', 'objectives', 'ctx', 'submitted', 'feedback']:
        if key in st.session_state: del st.session_state[key]
        
    with st.spinner("Generating comparative question..."):
        # Now returns 4 values: Question, Hidden Answer, Objectives, and Context
        q, ans, obj, ctx = generate_question(api_key)
        st.session_state.q = q
        st.session_state.ans = ans
        st.session_state.objectives = obj
        st.session_state.ctx = ctx

# --- Display Question ---
if "q" in st.session_state:
    st.markdown("---")
    st.markdown("### 📝 Practice Scenario")
    st.markdown(st.session_state.q)
    
    user_choice = st.radio("Choose the best option:", ["A", "B", "C", "D"], key="user_choice", index=None)
    
    if st.button("Submit Answer") and user_choice:
        # Prepare the payload for the advanced JSON evaluation
        assessment_payload = {
            "context": st.session_state.ctx,
            "question": st.session_state.q,
            "user_response": user_choice,
            "learning_objectives": st.session_state.objectives.split(","),
            "user_profile": {
                "experience_level": experience,
                "previous_gaps": st.session_state.get("gaps", []),
                "learning_preferences": pref
            }
        }
        
        with st.spinner("Analyzing your response..."):
            result = evaluate_answer(api_key, assessment_payload)
            st.session_state.feedback = result
            st.session_state.submitted = True

# --- Display Detailed Feedback ---
if st.session_state.get("submitted") and "feedback" in st.session_state:
    feedback = st.session_state.feedback
    
    if "assessment" in feedback:
        st.markdown("---")
        # Visual indicator for correct/incorrect
        if feedback["assessment"]["correct"]:
            st.success(f"### ✅ Correct! Score: {feedback['assessment']['score']}/100")
        else:
            st.error(f"### ❌ Incorrect. Score: {feedback['assessment']['score']}/100")
        
        # Gap Analysis & Correction
        st.write(f"**Gap Analysis:** {feedback['assessment']['gap_analysis']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Educator's Correction:**\n\n{feedback['explanation']['contextual_correction']}")
        with col2:
            st.warning(f"**Industry Insights:**\n\n{feedback['explanation']['industry_insights']}")
            
        # Personalized Next Steps
        st.subheader("🚀 Personalized Follow-up")
        st.write(f"**Suggested Topics:** {', '.join(feedback['personalized_followup']['suggested_topics'])}")
        st.write(f"**Study This Next:** {feedback['personalized_followup']['next_question']}")
        
        # Store gaps for next time
        if not feedback["assessment"]["correct"]:
            if "gaps" not in st.session_state: st.session_state.gaps = []
            st.session_state.gaps.append(feedback['assessment']['gap_analysis'])