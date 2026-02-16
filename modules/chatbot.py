import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

class AgriBot:
    def __init__(self):
        # Configuration (Lightweight)
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GOOGLE_API_KEY")
        self.pc_api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = "agri-knowledge"
        
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = "llama3.2"
        
        # Heavy models (Lazy loaded)
        self.embed_model = None
        self.pc = None
        self.index = None
        self.gemini_model = None
        self.models_loaded = False
        self.Groq = None

    def _load_models(self):
        if self.models_loaded: return
        
        print("⏳ Lazy loading AI models (Lightweight mode)...")
        
        # 1. Load Groq (if not already tried)
        if self.groq_key and not self.Groq:
            try:
                from groq import Groq
                self.Groq = Groq
                print("✅ Groq library imported")
            except ImportError:
                print("⚠️ Groq library not found")

        # 2. Load Gemini
        if self.gemini_key and not self.gemini_model:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini model initialized")
            except Exception as e:
                print(f"⚠️ Gemini init failed: {e}")

        # 3. Load Embedding Model & Pinecone ONLY if absolutely needed and memory allows
        # For Render free tier, we SKIP this by default to prevent crashes
        if os.getenv('RENDER') == 'true':
            print("🚀 Render environment detected: Skipping local embeddings for stability")
        elif self.pc_api_key and not self.index:
            try:
                from sentence_transformers import SentenceTransformer
                from pinecone import Pinecone, ServerlessSpec
                
                print("📦 Loading embeddings (Local Dev Mode Only)...")
                self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.pc = Pinecone(api_key=self.pc_api_key)
                
                existing_indexes = [idx.name for idx in self.pc.list_indexes().indexes]
                if self.index_name not in existing_indexes:
                    self.pc.create_index(
                        name=self.index_name,
                        dimension=384,
                        metric='cosine',
                        spec=ServerlessSpec(cloud='aws', region='us-east-1')
                    )
                self.index = self.pc.Index(self.index_name)
                print("✅ Pinecone initialized")
            except Exception as e:
                print(f"⚠️ RAG initialization failed: {e}")
            
        self.models_loaded = True

    def search_context(self, query):
        """Search Pinecone for relevant context (optional)"""
        if not self.index or not self.embed_model: 
            return ""
        try:
            query_em = self.embed_model.encode(query).tolist()
            results = self.index.query(vector=query_em, top_k=3, include_metadata=True)
            return "\n".join([res['metadata']['text'] for res in results['matches']])
        except: 
            return ""

    def get_answer(self, query, history=[]):
        # Ensure base configs are ready
        self._load_models()
        
        context = self.search_context(query)
        
        # Requesting a more detailed, multi-paragraph explanation
        prompt = f"""
        You are a highly detailed and friendly agricultural expert. 
        Your goal is to provide a comprehensive, multi-paragraph explanation to help the farmer. 
        Don't just give a short answer; explain the 'why' and give specific actionable tips.
        
        Background Information: {context}
        
        User's Question: {query}
        
        Detailed, casual, and encouraging answer:
        """
        
        # Priority 1: Groq (Recommended for Render)
        if self.groq_key and self.Groq:
            try:
                client = self.Groq(api_key=self.groq_key)
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"⚠️ Groq API failed: {e}")

        # Priority 2: Gemini
        if self.gemini_key and self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"⚠️ Gemini API failed: {e}")

        # Priority 3: Local Ollama (Local Dev Only)
        try:
            payload = {"model": self.ollama_model, "prompt": prompt, "stream": False}
            print(f"DEBUG: Trying Local AI ({self.ollama_model})...")
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            if response.status_code == 200: 
                return response.json().get('response')
        except: 
            pass

        # Priority 4: Local Fallbacks (No API keys needed)
        q_lower = query.lower()
        if "rice" in q_lower:
            return "Rice thrives in clayey soil with high water (1000mm+). Use NPK 80:40:40 for best results."
        if "cotton" in q_lower:
            return "Cotton needs deep black soil and drip irrigation. Use NPK 100:50:50 and pheromone traps for pests."
        if "wheat" in q_lower:
            return "Wheat is a Rabi crop needing cool weather and NPK 120:60:40. First irrigation at 21 days is critical."
        
        return "I'm currently in lightweight mode. For detailed AI answers, please ensure your API keys are set correctly in the Render environment!"

# Example knowledge seed
SEED_DATA = [
    "Rice requires high humidity and heavy rainfall, typically above 1000mm. It grows best in clayey loam soil.",
    "Millets are highly drought-resistant and can grow in regions with less than 500mm of annual rainfall.",
    "NPK (Nitrogen, Phosphorus, Potassium) ratio of 20:20:20 is generally recommended for balanced soil health.",
    "Integrated Pest Management (IPM) for Maize involves using biological controls and monitoring pheromone traps.",
    "Drip irrigation saves up to 40% more water compared to furrow irrigation for cotton crops.",
    "Wheat is a Rabi crop usually planted in late October to November in South Asia."
]
