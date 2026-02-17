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
        Your goal is to provide a comprehensive, medium-length explanation (about 3-4 paragraphs) to help the farmer. 
        Don't just give a short answer; explain the 'why' and give specific actionable tips.
        Keep it professional but easy to understand for someone working in the field.
        
        Background Information: {context}
        
        User's Question: {query}
        
        Medium-length, helpful, and encouraging answer:
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
            return (
                "To significantly increase rice production, you should focus on a few key areas:\n\n"
                "1. **Soil & Climate**: Rice thrives in clayey or loamy soil that can retain water. Ensure a consistent water level of at least 5-10cm during the vegetative stage.\n"
                "2. **Nutrient Management**: Use a balanced NPK ratio of 80:40:40. It's often beneficial to apply Nitrogen in split doses (at planting, tillering, and panicle initiation).\n"
                "3. **Improved Varieties**: Use High-Yielding Varieties (HYV) like IR64 or local hybrids suited for your region.\n"
                "4. **Pest Control**: Keep an eye out for Stem Borers and Leaf Folders. Neem oil can be a great natural preventive measure."
            )
        if "cotton" in q_lower:
            return (
                "Boosting cotton yield requires careful moisture and nutrient management:\n\n"
                "1. **Soil Selection**: Cotton performs best in deep black soils (regur) with good drainage. Avoid waterlogged fields as they cause root rot.\n"
                "2. **Fertilization**: A recommended NPK dose is 100:50:50 kg/ha. Adding well-decomposed farmyard manure (FYM) during land preparation significantly improves soil texture.\n"
                "3. **Irrigation**: Use drip irrigation if possible, as it maintains the ideal 'moist but not wet' condition cotton loves.\n"
                "4. **Pest Management**: Use pheromone traps to monitor Pink Bollworm populations early in the season."
            )
        if "wheat" in q_lower:
            return (
                "Wheat production can be optimized by following these Rabi season best practices:\n\n"
                "1. **Sowing Time**: Timely sowing (late Oct to mid-Nov) is critical. Every week's delay after Nov 15th can reduce yield by 10%.\n"
                "2. **Watering Strategy**: Critical stages for irrigation are Crown Root Initiation (CRI) at 21 days after sowing, and the flowering stage.\n"
                "3. **Balanced Nutrition**: Use NPK 120:60:40. Ensure Zinc application if your soil is deficient, as it helps in grain filling.\n"
                "4. **Weed Control**: Early weeding (within 30-35 days) ensures that the wheat crop doesn't compete for nutrients with grass weeds."
            )
        
        return "I'm currently in lightweight mode. For highly personalized AI answers, please ensure your API keys (especially Groq or Gemini) are correctly set in your .env file or environment variables!"

# Example knowledge seed
SEED_DATA = [
    "Rice requires high humidity and heavy rainfall, typically above 1000mm. It grows best in clayey loam soil.",
    "Millets are highly drought-resistant and can grow in regions with less than 500mm of annual rainfall.",
    "NPK (Nitrogen, Phosphorus, Potassium) ratio of 20:20:20 is generally recommended for balanced soil health.",
    "Integrated Pest Management (IPM) for Maize involves using biological controls and monitoring pheromone traps.",
    "Drip irrigation saves up to 40% more water compared to furrow irrigation for cotton crops.",
    "Wheat is a Rabi crop usually planted in late October to November in South Asia."
]
