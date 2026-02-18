import google.generativeai as genai
import json
from .database import query_listings

# 2026 Stable Model Alias
CURRENT_MODEL = "gemini-2.5-flash"  

def generate_question(api_key):
    """
    Fetches context and generates a comparative question with hidden metadata.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(CURRENT_MODEL)
    
    # Fetch 3 listings to ensure comparative analysis
    context = query_listings("diverse property listings", api_key, num_results=3)
    if not context:
        return None, None, None, None

    prompt = f"""
    ROLE: Senior Real Estate Licensing Instructor.
    DATASET: {context}
    
    TASK: Generate ONE 'Comparative Analysis' MCQ.
    
    REQUIREMENTS:
1. Compare AT LEAST TWO properties.
2. Focus on legal, zoning, disclosure, financing, HOA, tax, or regulatory differences.
3. The comparison must require analytical reasoning — NOT surface-level facts.
4. Ensure the correct answer depends on interpreting regulatory or financial nuance.
5. All distractors (A–D) must be plausible and technically defensible but incorrect.
6. Avoid obvious giveaway wording.
7. Mimic real estate licensing exam tone (e.g., scenario-based advisory question).

QUESTION STYLE:
- Present as a client advisory scenario.
- The licensee must determine a compliance, disclosure, or due diligence implication.
    
    INSTRUCTIONS:
    - Compare at least TWO properties on legal/zoning/financial nuances.
    - Provide 4 options (A, B, C, D).
    
    OUTPUT FORMAT (STRICT):
    [Question & Options]
    |||
    [Correct Letter]
    |||
    [Learning Objectives list, comma separated]
    """
    
    response = model.generate_content(prompt)
    parts = response.text.split("|||")
    
    if len(parts) >= 3:
        return parts[0].strip(), parts[1].strip(), parts[2].strip(), context
    return "Error generating question", "N/A", "N/A", context

def evaluate_answer(api_key, user_data):
    """
    Performs a deep assessment using the provided JSON schema.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(CURRENT_MODEL)
    
    # Constructing the sophisticated prompt based on your schema
    prompt = f"""
    You are an expert real estate educator. Evaluate this student's response:
    
    INPUT DATA:
    {json.dumps(user_data, indent=2)}
    
    INSTRUCTIONS:
    1. Analyze the response against industry standards.
    2. If incorrect, provide deep contextual explanations linking to specific property features and regulations.
    3. Tailor the tone to the user's experience level ({user_data['user_profile']['experience_level']}).
    
    RESPONSE FORMAT (STRICT JSON):
    {{
      "assessment": {{
        "correct": boolean,
        "score": number,
        "key_concepts": ["concept1", "concept2"],
        "gap_analysis": "string"
      }},
      "explanation": {{
        "contextual_correction": "string",
        "industry_insights": "string",
        "learning_resources": ["link_or_topic1", "link_or_topic2"]
      }},
      "personalized_followup": {{
        "next_question": "string",
        "suggested_topics": ["topic1", "topic2"]
      }}
    }}
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Clean potential markdown backticks from AI response
        cleaned_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_json)
    except Exception as e:
        return {"error": f"JSON Parse Error: {str(e)}", "raw": response.text}