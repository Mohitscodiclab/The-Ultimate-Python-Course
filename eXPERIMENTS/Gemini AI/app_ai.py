import google.generativeai as genai



# API_KEY = "Your_API_KEY"  # Replace with your actual API key
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro-latest")  
chat = model.start_chat()


print("Chat with Gemini-1.5-pro-latest Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chat.send_message(user_input)
    print("Gemini : ", response.text)
