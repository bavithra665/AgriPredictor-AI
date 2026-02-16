import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("❌ API Key is MISSING in .env file!")
else:
    genai.configure(api_key=api_key)
    print("\n✅ Listing available models for your key:")
    try:
        models = genai.list_models()
        found_any = False
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
                found_any = True
        if not found_any:
            print("❌ No models found that support content generation!")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
