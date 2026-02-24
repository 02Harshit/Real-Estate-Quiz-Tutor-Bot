import google.generativeai as genai
import json
import random
import re
from typing import Optional, Dict, Any, Tuple

# 2026 Stable Model Alias
CURRENT_MODEL = "gemini-2.5-flash"  

def get_available_question_types() -> Dict[str, Dict[str, Any]]:
    """Returns the available question types and their descriptions."""
    return {
        "comparative": {
            "name": "Comparative Analysis",
            "description": "Compare properties on legal, zoning, or financial nuances",
            "skill_focus": ["Regulatory knowledge", "Analytical thinking", "Property evaluation"],
            "icon": "📊",
            "color": "#58a6ff"
        },
        "calculation": {
            "name": "Calculation Based",
            "description": "Solve real estate mathematics problems",
            "skill_focus": ["Mathematical accuracy", "Formula application", "Financial analysis"],
            "icon": "🧮",
            "color": "#3fb950"
        }
    }

def generate_question(api_key: str, question_type: Optional[str] = None) -> Tuple[str, str, str, Dict, str, str]:
    """
    Fetches context and generates either a comparative or calculation-based question.
    Always returns a valid question (uses fallback if generation fails).
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(CURRENT_MODEL)
        
        # If no type specified, randomly choose
        if question_type is None:
            question_type = random.choice(["comparative", "calculation"])
        
        # Create prompt based on question type
        if question_type == "comparative":
            prompt = """Create a real estate comparative analysis question with 4 options.

The question should compare two properties on legal, zoning, or financial differences.

Format your response EXACTLY like this with these exact headers:

QUESTION:
[Write your question here with clear A, B, C, D options on new lines]

ANSWER:
[Single letter - A, B, C, or D]

OBJECTIVES:
[Learning objectives, comma separated - e.g., Zoning Analysis, Property Rights, Tax Implications]

Make sure each option starts with A) B) C) D) on separate lines."""
            
        else:  # calculation
            prompt = """Create a real estate calculation question with 4 options.

The question should involve price per square foot, LTV ratio, property tax, or commission calculation.

Format your response EXACTLY like this with these exact headers:

QUESTION:
[Write your question here with clear A, B, C, D options showing numbers on new lines]

ANSWER:
[Single letter - A, B, C, or D]

OBJECTIVES:
[Learning objectives, comma separated - e.g., Price per Sq Ft, LTV Ratio, Tax Calculation]

SOLUTION:
[Step-by-step calculation showing how to get the answer]

Make sure each option starts with A) B) C) D) on separate lines."""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            text = response.text
            
            # Extract sections
            question = extract_section(text, "QUESTION:", "ANSWER:")
            answer = extract_section(text, "ANSWER:", "OBJECTIVES:")
            objectives = extract_section(text, "OBJECTIVES:", "SOLUTION:")
            solution = extract_section(text, "SOLUTION:", None)
            
            # Clean up
            question = question.strip() if question else ""
            answer = answer.strip().upper() if answer else "A"
            objectives = objectives.strip() if objectives else "Real Estate Fundamentals"
            solution = solution.strip() if solution else ""
            
            # Validate answer is a single letter
            if answer and len(answer) > 1:
                for letter in ['A', 'B', 'C', 'D']:
                    if letter in answer:
                        answer = letter
                        break
                else:
                    answer = 'A'
            
            # Validate question has options
            if question and all(opt in question for opt in ['A)', 'B)', 'C)', 'D)']):
                return (question, answer, objectives, {}, solution, question_type)
        
        # If we get here, use fallback
        return create_fallback_question(question_type)
        
    except Exception as e:
        print(f"Error generating question: {str(e)}")
        return create_fallback_question(question_type)

def extract_section(text: str, start_marker: str, end_marker: Optional[str]) -> str:
    """Extract a section between markers."""
    try:
        text_lower = text.lower()
        start_lower = start_marker.lower()
        
        if start_lower in text_lower:
            start_idx = text_lower.find(start_lower) + len(start_marker)
            
            if end_marker:
                end_lower = end_marker.lower()
                end_idx = text_lower.find(end_lower, start_idx)
                if end_idx == -1:
                    end_idx = len(text)
            else:
                end_idx = len(text)
            
            section = text[start_idx:end_idx].strip()
            # Remove any remaining headers
            for header in ["QUESTION:", "ANSWER:", "OBJECTIVES:", "SOLUTION:"]:
                section = section.replace(header, "")
            return section.strip()
    except:
        pass
    return ""

def create_fallback_question(question_type: str) -> Tuple[str, str, str, Dict, str, str]:
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

def evaluate_answer(api_key: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs assessment of student's answer.
    Always returns a valid evaluation (uses fallback if AI fails).
    """
    try:
        # Basic correctness check
        user_answer = str(user_data.get('user_answer', '')).strip().upper()
        correct_answer = str(user_data.get('correct_answer', '')).strip().upper()
        is_correct = user_answer == correct_answer
        
        # Try AI evaluation
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(CURRENT_MODEL)
        
        prompt = f"""Evaluate this real estate student's answer and return ONLY a JSON object.

Question: {user_data.get('question', 'N/A')}
Student's answer: {user_answer}
Correct answer: {correct_answer}

Return this exact JSON structure (no other text):
{{
  "assessment": {{
    "correct": {str(is_correct).lower()},
    "score": {100 if is_correct else 0},
    "key_concepts": ["concept1", "concept2"],
    "gap_analysis": "Brief feedback about the answer"
  }},
  "explanation": {{
    "contextual_correction": "Explanation of why the answer is correct or incorrect",
    "industry_insights": "Real-world application of this concept",
    "step_by_step_solution": "",
    "learning_resources": ["Topic to review"]
  }},
  "personalized_followup": {{
    "next_question": "Suggested next topic to practice",
    "suggested_topics": ["topic1"],
    "practice_calculation": ""
  }}
}}"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            # Clean and parse JSON
            json_str = response.text.strip()
            # Remove markdown code blocks
            json_str = re.sub(r'```json\s*|\s*```', '', json_str)
            
            try:
                result = json.loads(json_str)
                # Ensure required structure
                if 'assessment' in result and 'explanation' in result and 'personalized_followup' in result:
                    return result
            except:
                pass
        
        # Fallback to basic evaluation
        return create_basic_evaluation(user_data, is_correct)
        
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        return create_basic_evaluation(user_data, is_correct)

def create_basic_evaluation(user_data: Dict[str, Any], is_correct: bool) -> Dict[str, Any]:
    """Creates a basic evaluation without AI."""
    user_answer = str(user_data.get('user_answer', '')).strip().upper()
    correct_answer = str(user_data.get('correct_answer', '')).strip().upper()
    
    return {
        "assessment": {
            "correct": is_correct,
            "score": 100 if is_correct else 0,
            "key_concepts": ["Real Estate Fundamentals"],
            "gap_analysis": f"You selected {user_answer}. The correct answer is {correct_answer}.",
            "calculation_errors": []
        },
        "explanation": {
            "contextual_correction": f"The correct answer is {correct_answer}. Please review the question carefully.",
            "industry_insights": "This concept is important for real estate professionals.",
            "step_by_step_solution": "",
            "learning_resources": ["Review basic real estate concepts"]
        },
        "personalized_followup": {
            "next_question": "Continue practicing with more questions.",
            "suggested_topics": ["Real Estate Basics"],
            "practice_calculation": ""
        }
    }