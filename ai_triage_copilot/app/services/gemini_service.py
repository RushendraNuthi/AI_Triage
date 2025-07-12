import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_analysis(description):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    You are a security analyst assistant. Given the incident description, extract:
    1. Category (Phishing, Bug, Intrusion, Malware, etc.)
    2. Priority (Critical, High, Medium, Low)
    3. Affected Entities (IPs, users, devices)
    4. Suggested Solutions (3–5 steps in markdown)
    Respond in JSON.

    Incident Description:
    {description}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None
