# 🏠 Real Estate AI Tutor (RAG-Driven)

![AI](https://img.shields.io/badge/AI-RAG%20System-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-000000?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![RAG](https://img.shields.io/badge/Architecture-Retrieval%20Augmented%20Generation-success?style=for-the-badge)

---

## 📌 What is Real Estate AI Tutor?

The **Real Estate AI Tutor** is an **AI-powered educational system** designed to simulate **real-world, high-stakes real estate assesments**.

Unlike traditional MCQ platforms or static question banks, this system dynamically **generates intelligent exam questions** by analyzing **multiple real property listings simultaneously**, forcing users to reason like licensed professionals.

It leverages **Retrieval-Augmented Generation (RAG)** to combine:
- Semantic document retrieval
- Comparative legal and financial reasoning
- Personalized pedagogical feedback

---

## 🧠 Why This Project is Different

### ❌ Traditional Learning Platforms
- Static questions
- Keyword-based search
- No reasoning or adaptive learning

### ✅ Real Estate AI Tutor
- AI-generated scenario-based questions
- Comparative risk assessment
- Adaptive explanations based on user expertise
- Real-world property data reasoning

---

## ✨ Key Innovations

### 🔍 Comparative RAG Engine
Retrieves **up to 3 diverse property listings** (Residential, Commercial, Industrial) and synthesizes **a single exam question** that requires cross-comparison of:
- Legal risks
- Zoning conflicts
- Environmental liabilities
- Financial implications

### 🎯 Adaptive Feedback Loop
The system tracks:
- User experience level (Beginner → Advanced)
- Repeated mistake patterns
- Knowledge gaps

And adjusts:
- Question difficulty
- Explanation depth
- Legal terminology usage

### 🧬 Semantic Search (ChromaDB)
Powered by **vector embeddings**, the system understands **intent**, not just keywords—allowing it to retrieve relevant case studies even when exact terms don’t match.

---

## 🏗️ System Architecture (Low-Level Design)

The project follows a clean **Controller–Service–Repository** pattern for scalability and testability.




## 🚀 Setup & Tech Stack

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-000000?style=flat)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=flat)

### Tech Stack
- **Frontend:** Streamlit  
- **LLM:** Google Gemini 2.5 Flash  
- **Vector Database:** ChromaDB  
- **Embeddings:** `models/gemini-embedding-001`  
- **Language:** Python  

### Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/real-estate-ai-tutor.git
cd real-estate-ai-tutor

# Install dependencies
pip install -r requirements.txt

# Create Streamlit secrets file
mkdir .streamlit
echo 'GEMINI_API_KEY = "your_google_ai_studio_api_key"' > .streamlit/secrets.toml

# Run the application
python -m venv venv
venv\Scripts\activate
streamlit run app.py

# App will be available at:
# http://localhost:8501

###Live Working Demo
https://real-estate-quiz-tutor-bot-xyz.streamlit.app/

