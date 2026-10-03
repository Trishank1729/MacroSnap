# 🥗 MacroSnap

MacroSnap is an AI-powered nutrition assistant that helps users understand their meals using **Google Gemini** and **Streamlit**.

Users can chat with the AI about food, upload meal images, get estimated calories and macronutrients, and receive a personalized nutrition summary directly through Gmail.

## ✨ Features

- 💬 **AI Nutrition Chat**  
  Chat with MacroSnap about meals, food, nutrition, and fitness.

- 📷 **Meal Image Analysis**  
  Upload a photo of your meal and let Gemini analyze what the meal contains.

- 🔥 **Calorie Estimation**  
  Get an estimated calorie count for the meal.

- 💪 **Macronutrient Estimation**  
  Get estimated values for:
  - Protein
  - Carbohydrates
  - Fat

- 📊 **Personalized Nutrition Summary**  
  Generate a summary based on your conversation and meal information.

- 📧 **Gmail Summary**  
  Send your personalized nutrition summary directly to your Gmail account.

- 💾 **Conversation Memory**  
  The application maintains the conversation during the current session so the AI can use previous meal information when creating the summary.

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Web application interface
- **Google Gemini API** – AI conversation and meal image analysis
- **Gmail SMTP** – Sending nutrition summaries through email

## 📁 Project Structure

```text
MacroSnap/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml.example