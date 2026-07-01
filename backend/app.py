from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv
from prompt import build_prompt
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    company = data.get("company")
    website = data.get("website")
    description = data.get("description")

    prompt = build_prompt(company, website, description)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You output ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
    except:
        parsed = {"raw": content}

    return jsonify(parsed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)