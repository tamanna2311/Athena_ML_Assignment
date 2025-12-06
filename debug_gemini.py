import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)
    
    print("\n--- Listing Available Models ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")

    print("\n--- Testing Generation (gemini-1.5-flash) ---")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, are you working?")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error with gemini-1.5-flash: {e}")

    print("\n--- Testing Generation (gemini-1.5-flash-001) ---")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-001')
        response = model.generate_content("Hello, are you working?")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error with gemini-1.5-flash-001: {e}")
