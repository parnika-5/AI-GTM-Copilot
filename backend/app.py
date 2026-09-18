from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from pathlib import Path
from prompt import build_prompt

import json
import os

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

CORS(app)

# Demo mode is enabled by default.
# Set DEMO_MODE=false to enable real OpenAI generation.
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"


# --------------------------------------------------
# SAMPLE CAMPAIGN GENERATOR
# --------------------------------------------------

def generate_demo_campaign(company, website, description):

    return {
        "research_summary": (
            f"DEMO DATA — SAMPLE CAMPAIGN\n\n"
            f"{company} is the target company for this demonstration. "
            f"Based on the information provided, the company operates in "
            f"the following area: {description or 'Not specified'}. "
            f"The following campaign illustrates how an AI-assisted "
            f"sales workflow could organize prospect information and "
            f"generate personalized outreach. "
            f"No live website research or AI generation was performed."
        ),

        "pain_points": [
            "HYPOTHESIS: The company may be looking for ways to improve operational efficiency.",
            "HYPOTHESIS: Teams may spend significant time on repetitive manual workflows.",
            "HYPOTHESIS: Scaling technical operations could introduce cost or performance challenges."
        ],

        "buying_signals": [
            "HYPOTHESIS: Investment in new technical initiatives could create demand for additional tools.",
            "HYPOTHESIS: Expansion of product capabilities could increase infrastructure requirements.",
            "HYPOTHESIS: A focus on efficiency could motivate evaluation of alternative solutions."
        ],

        "email": (
            f"Subject: Exploring opportunities at {company}\n\n"
            f"Hi [First Name],\n\n"
            f"I came across {company} and was interested in your work "
            f"in {description or 'your industry'}.\n\n"
            f"I'm reaching out to learn how your team is approaching "
            f"its current technical and operational priorities. "
            f"If improving efficiency or scaling existing workflows "
            f"is on your roadmap, I'd welcome the opportunity to "
            f"understand your requirements and explore whether "
            f"there may be a fit.\n\n"
            f"Would you be open to a brief conversation next week?\n\n"
            f"Best,\n"
            f"[Your Name]"
        ),

        "linkedin_message": (
            f"Hi [First Name]! I came across {company} and was "
            f"interested in the work your team is doing. "
            f"I'd love to learn more about your current priorities "
            f"and explore whether there's an opportunity to connect. "
            f"Would you be open to a quick conversation?"
        ),

        "cold_call_script": (
            f"Hi [First Name], this is [Your Name]. "
            f"Did I catch you at an okay time?\n\n"
            f"I'm reaching out because I was interested in "
            f"{company}'s work and wanted to learn more about "
            f"your team's current priorities.\n\n"
            f"Are there any challenges you're currently facing "
            f"around efficiency, scalability, or technical workflows?\n\n"
            f"[Listen and ask follow-up questions.]\n\n"
            f"How is that affecting your team today?\n\n"
            f"If it makes sense, I'd be happy to arrange a "
            f"follow-up conversation to explore your requirements."
        ),

        "follow_up_1": (
            f"Subject: Following up — {company}\n\n"
            f"Hi [First Name],\n\n"
            f"Just following up on my previous message. "
            f"I'd be interested in learning more about your "
            f"team's priorities and whether a conversation "
            f"would be useful.\n\n"
            f"Would you have 15 minutes next week?\n\n"
            f"Best,\n"
            f"[Your Name]"
        ),

        "follow_up_2": (
            f"Subject: Closing the loop\n\n"
            f"Hi [First Name],\n\n"
            f"I wanted to reach out one last time. "
            f"If exploring new solutions isn't a priority "
            f"for {company} right now, I completely understand.\n\n"
            f"Happy to reconnect whenever the timing is better.\n\n"
            f"Best,\n"
            f"[Your Name]"
        )
    }


# --------------------------------------------------
# OPENAI CLIENT
# --------------------------------------------------

def get_openai_client():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing."
        )

    return OpenAI(api_key=api_key)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "ok",
        "message": "AI GTM Copilot backend is running.",
        "demo_mode": DEMO_MODE
    })


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "demo_mode": DEMO_MODE
    })


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please provide a valid JSON request."
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
            "error": "Please enter a website or description."
        }), 400

    # --------------------------------------------------
    # DEMO MODE: NO OPENAI API CALL
    # --------------------------------------------------

    if DEMO_MODE:

        app.logger.info(
            "Generating demo campaign for %s",
            company
        )

        campaign = generate_demo_campaign(
            company,
            website,
            description
        )

        return jsonify(campaign), 200

    # --------------------------------------------------
    # LIVE MODE: OPENAI API
    # --------------------------------------------------

    try:

        client = get_openai_client()

        prompt = build_prompt(
            company,
            website,
            description
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a GTM research assistant. "
                        "Return only valid JSON. "
                        "Do not invent verified company facts."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0.7,
            timeout=60.0
        )

        content = response.choices[0].message.content

        if not content:
            return jsonify({
                "error": "The AI returned an empty response."
            }), 502

        parsed = json.loads(content)

        return jsonify(parsed), 200

    except RuntimeError as error:

        app.logger.error(
            "Configuration error: %s",
            error
        )

        return jsonify({
            "error": "The OpenAI API key is not configured."
        }), 503

    except (OpenAIError, json.JSONDecodeError) as error:

        app.logger.error(
            "AI generation failed: %s",
            error
        )

        return jsonify({
            "error": (
                "AI generation failed. "
                "Check your API key and billing."
            )
        }), 502

    except Exception:

        app.logger.exception(
            "Unexpected error during generation"
        )

        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.getenv("PORT", "5001")
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )