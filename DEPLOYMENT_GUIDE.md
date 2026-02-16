# AgriPredictor-AI Deployment Guide

## 🚀 Live URL
**https://agripredictor-ai.onrender.com**

## ✅ What's Working
1. **User Authentication** - Register/Login system
2. **Home Page** - Landing page with project overview
3. **About Page** - Team info and sponsor tool integrations
4. **Chatbot** - AI Assistant (may take 5-10 seconds on first question)
5. **Dashboard** - Analytics and visualizations
6. **Review System** - User feedback collection

## ⚠️ Important Notes for Demo

### First-Time Usage
- **Crop Prediction**: The ML model (23MB) loads on first use. If you see "ML Model is currently unavailable", refresh the page and try again.
- **AI Chatbot**: First question may take 5-10 seconds while models initialize. Subsequent questions are instant.

### Test Data for Crop Prediction
Use these values for a quick demo:
- **N**: 90
- **P**: 40
- **K**: 40
- **Temperature**: 25
- **Humidity**: 80
- **pH**: 6.5
- **Rainfall**: 200
- **Soil Type**: Loamy
- **Season**: Kharif
- **Region**: South

## 🛠️ Sponsor Tools Integrated

### 1. **Mocah Voice AI**
- **Location**: AI Chatbot page
- **Feature**: "Listen" button on bot responses
- **How to Demo**: Ask any farming question, then click the speaker icon to hear the response

### 2. **IdeaVo**
- **Location**: About Us page
- **Usage**: Used for initial concept validation and strategic planning

### 3. **Dyad**
- **Location**: About Us page  
- **Usage**: Team collaboration and progress tracking

## 🎯 Hackathon Submission Details

### Project Name
AgriPredictor-AI

### Description
An AI-powered agricultural advisory platform that combines Machine Learning crop predictions with real-time climate risk analysis and an intelligent chatbot assistant. Designed to help farmers make data-driven decisions for optimal yields.

### Key Features
1. **ML-Based Crop Recommendation** - Predicts top 3 suitable crops based on soil and climate data
2. **Climate Risk Intelligence** - Real-time drought and flood risk scoring
3. **AI Agricultural Assistant** - RAG-powered chatbot using Groq Llama 3
4. **Voice Accessibility** - Mocah AI integration for audio responses
5. **Analytics Dashboard** - Visual insights into prediction history and crop comparisons

### Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **ML**: Scikit-learn (Random Forest Classifier)
- **AI**: Groq API (Llama 3.1), Gemini (fallback), Pinecone (RAG)
- **Voice**: Mocah AI (Web Speech API)
- **Database**: SQLite (user data), MongoDB (crop details - optional)
- **Deployment**: Render (Cloud Platform)

### Sponsor Tools
- **Mocah**: Voice AI for accessibility
- **IdeaVo**: Concept validation
- **Dyad**: Team collaboration

## 🔧 Troubleshooting

### If Crop Prediction Shows "Unavailable"
1. Wait 30 seconds
2. Refresh the page
3. Try again - the model should be loaded now

### If Chatbot is Slow
- First question initializes AI models (5-10 seconds)
- Subsequent questions are instant
- If error persists, wait 10 seconds and retry

### If Dashboard is Empty
- You need to make at least one crop prediction first
- Dashboard shows analytics based on your prediction history

## 📊 Demo Flow for Judges

1. **Start**: Visit homepage → Click "Get Started"
2. **Register**: Create account (use any email format)
3. **Predict**: Go to "Crop Prediction" → Enter test data → Submit
4. **View Results**: See top 3 crop recommendations with risk scores
5. **Ask AI**: Go to "AgriChat" → Ask "How to save water in Cotton?"
6. **Listen**: Click the speaker icon to hear Mocah voice response
7. **Analytics**: Go to "Dashboard" → View prediction history charts
8. **About**: Check "About Us" for sponsor tool mentions

## 🎓 Project Context
Built for a hackathon to demonstrate AI's potential in agriculture. Focuses on making advanced technology accessible to farmers through voice interfaces and simple visualizations.

---
**Last Updated**: February 16, 2026
**Deployment**: Render Free Tier
**Status**: Production Ready ✅
