# from models.api_1 import groq_api_key
from groq import Groq
import re, json

# Define API Key for the Groq client
groq_api_key = "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"

# Initialize Groq client
client = Groq(api_key=groq_api_key)

# Initial system message to guide the AI agent
messages = [
    {
        "role": "system",
        "content":  """YOU are a Function Agent that understands user queries and determines if the query is related to opening, closing, searching, and other actions. You should always return your response in JSON format like this:
        DEMO OF USER TELLING TO OPEN WEBSITE:
        {
            "function_name": "Open Website",
            "target_entity": {
                "type": "Website",
                "name": "Specify the website or app name here"
            },
            "action_details": {
                "description": "Provide a modified and clear version of the user's query here",
                "user_query": "Original user query here",
                "is_action_identified": true,
                "action_type": "Open"
            },
            "response": "The action requested by the user has been successfully completed. For example, the website 'Specify the website or app name here' has been opened as per the user's request.",
            "code_snippet": {
                "language": "Python",
                "code": "import webbrowser\nwebbrowser.open('target_link_of_site') *provide\n for new line also try not to create variables.Write code in single line use \n to give enter now!! after importing modules as well*""
            }
        }

        YOU MUST: Provide JSON only, not any other response NOW!!
        """
    }
]

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
        
        # Print the raw JSON response for debugging
        print(f"Raw JSON response: {res_json}")
        
        # Clean up potential problematic characters
        # This might help if there are invalid control characters
        res_json = re.sub(r'[\x00-\x1F]', '', res_json)
        
        # Attempt to parse the string into a JSON dictionary
        res = json.loads(res_json)
        
        # Print the code snippet for verification
        code = res["code_snippet"]["code"]
        if code:   
            # Execute the code snippet
            exec(code)
            

    