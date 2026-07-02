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

# Change this to False whenever you want to use the real OpenAI API
USE_MOCK = True

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    company = data.get("company", "")
    website = data.get("website", "")
    description = data.get("description", "")

    prompt = build_prompt(company, website, description)

    # ==========================
    # MOCK MODE (No OpenAI API)
    # ==========================
    if USE_MOCK:
        mock_response = {
            "company_summary": f"{company} is positioned as an innovative company serving its target market.",
            "icp": [
                "Marketing Managers",
                "Sales Leaders",
                "Startup Founders"
            ],
            "value_proposition": f"{company} helps businesses streamline workflows and improve productivity.",
            "campaign": {
                "headline": f"Grow Faster with {company}",
                "linkedin_post": f"""🚀 Meet {company}!

Looking for a smarter way to grow your business?

Our solution helps teams save time, increase efficiency, and focus on what matters most.

Learn more today!""",
                "email_subject": f"See how {company} can help your business",
                "email_body": f"""Hi,

I wanted to introduce {company}.

Based on your business needs, we believe our solution can help improve productivity while simplifying day-to-day operations.

Would you be open to a quick conversation next week?

Best,
The {company} Team"""
            }
        }

        return jsonify(mock_response)

    # ==========================
    # REAL OPENAI MODE
    # ==========================
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
    except Exception:
        parsed = {"raw": content}

    return jsonify(parsed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
