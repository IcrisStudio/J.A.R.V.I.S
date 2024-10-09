from models.api_1 import groq_api_key
from groq import Groq
import re

client = Groq(api_key=groq_api_key)

messages = [
    {
        "role": "system",
        "content":  f"You are jarvis from iron man movie. To Open Any website:```python\nimport webbrowser\nwebbrowser.open(website)```"
    },
   

]


def Ai(prompt):
    add_messages("user", prompt)
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192"
    )

    response = chat_completion.choices[0].message.content

    add_messages("assistant", response)

    return response


def add_messages(role, content):
    messages.append({"role": role, "content": content})



