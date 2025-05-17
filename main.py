import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 🔹 Load environment variables from .env file
load_dotenv()

# 🔹 Set Streamlit Page Config
st.set_page_config(page_title="🍲 AI-Based Recipe Generator", page_icon="🍲", layout="centered")

# 🔹 Secure API Key Handling
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"⚠️ Failed to initialize Gemini AI: {str(e)}")
        gemini_model = None
else:
    st.error("⚠️ Gemini AI API key is missing! Please check your .env file.")
    gemini_model = None

# 🔹 Supported Languages for Translation
languages = {
    "English": "English",
    "Urdu": "اردو",
    "Sindhi": "سنڌي",
    "Punjabi (Shahmukhi)": "پنجابی",
    "Pashto": "پښتو",
    "Balochi": "بلوچی",
    "Gujarati": "ગુજરાતી",
    "Hindko": "ہندکو",
    "Wakhi": "وخی",
}

# 🔹 Function to Translate Text Using Gemini AI
def translate_text(text, target_language):
    if not gemini_model:
        return text
    try:
        prompt = f"Translate the following text to {target_language}:\n\n{text}"
        response = gemini_model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, "text") else text
    except Exception as e:
        st.error(f"⚠️ Translation Error: {str(e)}")
        return text

# 🔹 Main Recipe Generator App
st.title("🍲 AI-Based Recipe Generator")
st.write("Enter the ingredients you have, and I'll suggest a creative recipe for you!")

# Input for Available Ingredients
ingredients = st.text_input("Available Ingredients (separate by commas)", 
                            placeholder="e.g., chicken, tomatoes, basil, garlic")

# Language Selection Dropdown for Recipe Translation
selected_language = st.selectbox("🌍 Select language for recipe translation:", options=list(languages.keys()))

# Generate Recipe Button
if st.button("Generate Recipe"):
    if not ingredients.strip():
        st.error("Please enter some ingredients!")
    elif not gemini_model:
        st.error("Gemini model is not initialized. Please check your API key.")
    else:
        prompt = (f"Using these ingredients: {ingredients}. "
                  "Please suggest a creative and easy-to-make recipe with detailed step-by-step instructions. "
                  "Write the recipe in English.")
        st.info("Generating recipe... Please wait.")
        try:
            response = gemini_model.generate_content(prompt)
            if response and hasattr(response, "text") and response.text.strip():
                recipe = response.text.strip()
                if selected_language != "English":
                    recipe = translate_text(recipe, languages[selected_language])
                st.success("Recipe Generated!")
                st.write(recipe)
            else:
                st.error("⚠️ No response received. Please try again.")
        except Exception as e:
            st.error(f"⚠️ An error occurred while generating the recipe: {str(e)}")

# 🔹 Footer
st.markdown("---")
st.markdown("🚀 **Developed by Muhammad Mudasir** | AI-Powered Recipe Generator")
