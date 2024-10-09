from groq import Groq
import re, json
from models.api_1 import groq_api_key
from models.messages import messages
from Head.NewSpeak import speak
from Functions.image_generator import generate_images
# Initialize Groq client with api key
client = Groq(api_key=groq_api_key)

# Function to interact with AI
def Ai(prompt):
    add_messages("user", prompt)
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192"
    )
    response = chat_completion.choices[0].message.content
    add_messages("assistant", response)

    return response

# Helper function to add messages to the conversation history
def add_messages(role, content):
    messages.append({"role": role, "content": content})

# Main interaction loop
while True:
        user_query = input(">> ")
        res_json = Ai(user_query)

        # Clean up potential problematic characters
        # This might help if there are invalid control characters
        res_json = re.sub(r'[\x00-\x1F]', '', res_json) 

        # Attempt to parse the string into a JSON dictionary
        res = json.loads(res_json)
       
        function_name = res.get("function_name", None)
        print(function_name)
        
        if "Desktop Automation" in function_name:
            code = res.get("code_snippet", {}).get("code", None)
            exec(code)
            AiResponse = res.get("response", None)
            
        elif "Generate Image" in function_name:
            prompt = res.get("action_details").get("user_query")   
            generate_images(prompt)
            AiResponse = res.get("response", None)
            
        else:
            AiResponse = res.get("response", None)
        
        print(f"AI: {AiResponse}")
        speak(AiResponse)