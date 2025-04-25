# 💬 Chat with Google Gemini using Python

This simple Python project allows you to chat with **Google's Gemini 1.5 Pro model** using the `google-generativeai` library. With just a few lines of code, you'll be able to create an interactive AI chatbot in your terminal!

## 🚀 Features
- Chat with **Gemini-1.5-Pro-Latest** using your terminal
- Lightweight and easy to set up
- Ideal for beginners learning about Generative AI

---

## 🛠️ Setup Instructions

### 1. Clone this repository (or create a new Python file):
You can either:
- Clone this repo:  
  ```bash
  git clone https://github.com/yourusername/your-repo-name.git
  cd your-repo-name
  ```

- Or simply copy and paste the code below into your own `.py` file.

### 2. Install the required package
Make sure Python is installed, then run:

```bash
pip install google-generativeai
```

### 3. Create an API Key
Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) and:
- Sign in with your Google account
- Generate a new API key
- Copy your API key

### 4. Update the script

Replace `API_KEY` with your actual key in the code below:

```python
import google.generativeai as genai

API_KEY = "Your_API_KEY"  # Replace with your actual API key

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro-latest")  
chat = model.start_chat()

print("Chat with Gemini-1.5-pro-latest. Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chat.send_message(user_input)
    print("Gemini:", response.text)
```

---

## 🧠 Example
```
You: Hello!
Gemini: Hello! How can I assist you today?
```

---

## 📌 Notes
- This script runs completely in your terminal.
- It uses the latest **Gemini 1.5 Pro model**.
- Make sure you **don’t share your API key** publicly.

---

## 📄 License
This project is licensed under the MIT License. Feel free to use and modify!

---

## ✨ Credits
Created with ❤️ using Python and Google's Generative AI SDK.
```

---

Would you like me to generate a `README.md` file for direct download or help you upload it to your GitHub repo?
