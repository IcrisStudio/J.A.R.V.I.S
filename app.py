from flask import Flask, render_template, request, jsonify
from Head.RealasticSpeak import speak
from models.ai import Ai

app = Flask(__name__)

import re
def find_code(text):
    pattern = r'```python(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        code = matches[0].strip()
        return code
    else:
        print('no code found')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/speech-to-text", methods=["POST"])
def speechToText():
    data = request.get_json().get("response", "")
    print(data)
    speak(data)
    
    return "success"


@app.route("/get-ai-response", methods=["POST"])
def GetAiRes():
    Query = request.get_json().get("query", "")
    Response = Ai(Query)
    print(Response)
    
    return jsonify({"Query": Query, "Response": Response})
    
if __name__ == "__main__":
    app.run(debug=True)