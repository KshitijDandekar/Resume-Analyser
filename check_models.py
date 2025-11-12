import google.generativeai as genai
import os

# # --- IMPORTANT ---
# Set your API key as an environment variable in your terminal
# On Windows: set GOOGLE_API_KEY=YOUR_API_KEY
# On macOS/Linux: export GOOGLE_API_KEY=YOUR_API_KEY

# OR, just paste your key directly here for a quick test:
os.environ["GOOGLE_API_KEY"] = "AIzaSyDSwjS02Ta38ZLlNpnvGOBo_fCVnJ3oQxk"

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it or paste your key directly into the script.")
    exit()
except Exception as e:
    print(f"Error configuring API: {e}")
    exit()

print("Listing available models...\n")

try:
    for model in genai.list_models():
        # We only care about models that can 'generateContent'
        if 'generateContent' in model.supported_generation_methods:
            print(f"Model Name: {model.name}")
            print(f"  Supported Methods: {model.supported_generation_methods}\n")
            
except Exception as e:
    print(f"An error occurred while listing models: {e}")