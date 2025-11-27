import google.generativeai as genai

API_KEY = "AIzaSyDAuBtO4W6gsRHt-4CMnA9nQeZEug75Ba4"   # <-- paste your key here

genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say hello if the Gemini API is working.")
    print("✔ Gemini API Working!")
    print("Response:", response.text)
except Exception as e:
    print("❌ Gemini API Error:")
    print(e)
