from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from pathlib import Path
from prompt import build_prompt

import json
import os

# Load .env from the backend directory, regardless of where Flask is started.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

# Configure CORS for local development and the deployed frontend.
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_url = os.getenv("FRONTEND_URL", "").strip().rstrip("/")

if frontend_url:
    allowed_origins.append(frontend_url)

CORS(app, resources={
    r"/generate": {"origins": allowed_origins}
})

# Initialize the client only when a request needs it.
# This allows Flask to start even if the API key has not been configured.
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to backend/.env "
            "or configure it in your hosting environment."
        )

    return OpenAI(api_key=api_key)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "AI GTM Copilot backend is running."
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a valid JSON request."
        }), 400

    company = str(data.get("company") or "").strip()
    website = str(data.get("website") or "").strip()
    description = str(data.get("description") or "").strip()

    if not company:
        return jsonify({
            "error": "Please enter a company name."
        }), 400

    if not website and not description:
        return jsonify({
            "error": "Please provide a website or company description."
        }), 400

    prompt = build_prompt(company, website, description)

    try:
        client = get_openai_client()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a GTM research assistant. "
                        "Return only valid JSON. "
                        "Do not invent verified facts about companies."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            timeout=60.0
        )

        content = response.choices[0].message.content

        if not content:
            return jsonify({
                "error": "The AI returned an empty response. Please try again."
            }), 502

        parsed = json.loads(content)

        if not isinstance(parsed, dict):
            return jsonify({
                "error": "The AI returned an unexpected response format."
            }), 502

        return jsonify(parsed), 200

    except RuntimeError as error:
        app.logger.error("Configuration error: %s", error)

        return jsonify({
            "error": "The server's OpenAI API key is not configured."
        }), 503

    except (OpenAIError, json.JSONDecodeError) as error:
        app.logger.error("AI generation failed: %s", error)

        return jsonify({
            "error": (
                "AI generation failed. Check your API key, "
                "API billing, and server logs."
            )
        }), 502

    except Exception:
        app.logger.exception("Unexpected error during generation")

        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
