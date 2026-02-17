# 🌾 AgriPredictor-AI: Intelligent Agricultural Advisory Platform

> **"Transforming Soil and Climate Data into Actionable Farming Intelligence"**

---

## 🌟 1. Project Overview
**AgriPredictor-AI** is a comprehensive digital solution designed to assist farmers in maximizing their crop yields while minimizing environmental risks. By integrating Machine Learning (ML), Generative AI (LLMs), and Retrieval-Augmented Generation (RAG), the platform provides personalized crop recommendations, real-time climate risk assessments, and an intelligent 24/7 agricultural consultant.

---

## 🛑 2. Problem Statement
Farmers worldwide face three critical challenges:
1. **Uncertainty**: Choosing the wrong crop for the soil type leads to financial loss.
2. **Climate Risk**: Unexpected droughts or floods can destroy seasons.
3. **Information Gap**: Lack of immediate access to expert agronomic advice for pest control and plant diseases.

**AgriPredictor-AI** solves this by bridging the gap between flat data and actionable wisdom.

---

## ✨ 3. Key Features

### 🧠 A. AI-Powered Crop Recommendation
- **ML Model**: Uses a Random Forest Classifier trained on soil parameters (N, P, K, pH) and climate data (Temperature, Humidity, Rainfall).
- **Hybrid Logic**: Includes a fail-safe rule-based predictor for environments with low computing resources.
- **Top 3 Recommendations**: Provides weighted choices instead of a single result to give farmers flexibility.

### ⚡ B. Climate Risk Intelligence
- **Scoring Engine**: Real-time calculation of **Drought** and **Flood** risks based on environmental inputs.
- **Risk-Adjusted Confidence**: Modifies ML predictions to account for impending weather threats.

### 🤖 C. AgriChat Assistant (RAG)
- **Groq & Llama 3.1**: Ultra-fast AI responses for farming queries.
- **Knowledge Base**: Integrated via **Pinecone Vector DB** to provide specific context-aware advice on irrigation, pests, and fertilizers.
- **Voice Accessibility**: Integrated with **Mocah Voice AI** to convert text advice into audible speech for better accessibility.

### 📊 D. Interactive Analytics Dashboard
- Visualizes prediction history using **Chart.js**.
- Tracks soil health trends and crop distribution to help in long-term farm planning.

---

## 🛠️ 4. Technical Architecture

### Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Bootstrap 5
- **Machine Learning**: Scikit-learn, Joblib (Memory-Mapped loading)
- **AI/LLM**: Groq (Llama 3.1), Google Gemini (Fallback)
- **Vector DB**: Pinecone (RAG implementation)
- **Database**: SQLite (Users/History), MongoDB (Crop Metadata)
- **Voice AI**: Mocah (Web Speech API)

### Cloud Optimization (Render Free Tier)
- **Lazy Loading**: Drastically reduced startup memory usage by delaying heavy library and model imports.
- **mmap_mode**: Implemented Memory-Mapping for the ML model to run on low-RAM environments (Render Free Tier).
- **Lightweight Fallbacks**: Automatic logic switching to ensure 100% uptime even if cloud AI services are throttled.

---

## 🔗 5. Sponsor Tools & Integrations

1. **Mocah Voice AI**: Powers the "Listen" feature in the chatbot, enabling an inclusive experience for all farmers.
2. **IdeaVo**: Used for project brainstorming, strategic roadmap creation, and feature validation.
3. **Dyad**: Employed as the core collaboration and task management tool during the development sprint.

---

## 🚀 6. Installation & Deployment

### Local Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env` (GROQ_API_KEY, GOOGLE_API_KEY, etc.).
5. Run the app: `python app.py`

### Cloud Deployment (Render)
1. Hosted at: `https://agripredictor-ai.onrender.com`
2. **Health Check**: Implemented `/health` route for 100% uptime monitoring.
3. **Procfile**: Optimized Gunicorn configuration with `--no-preload` and `--timeout 0` for stable startup.

---

## 🔮 7. Future Roadmap
- **Satellite Integration**: Incorporating real-time satellite imagery for crop health monitoring.
- **IoT Sensors**: Direct integration with soil moisture and pH sensors for automated data entry.
- **Multi-lingual Support**: Expanding the Mocah Voice AI to support local regional languages.

---

## 👨‍💻 8. The Team
*Created with passion for Sustainable Agriculture and AI Innovation.*

---
© 2026 AgriPredictor-AI Project Documentation
