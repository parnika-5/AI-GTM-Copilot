def build_prompt(company, website, description):
    return f"""
You are an experienced go-to-market strategist and sales engineer.

Your task is to create a practical outbound sales campaign using the
company information provided below.

COMPANY INFORMATION

Company: {company}
Website: {website or "Not provided"}
Description: {description or "Not provided"}

IMPORTANT RULES

1. Use the supplied information as your primary source.
2. Do not claim you visited or researched the website.
   The website is provided as context only.
3. Do not invent funding rounds, employee counts, partnerships,
   revenue figures, technology stacks, or recent company news.
4. Distinguish verified information from hypotheses.
5. Label potential pain points and buying signals as hypotheses
   when they cannot be confirmed from the supplied information.
6. Make the outreach specific, professional, concise, and realistic.
7. Avoid exaggerated claims and generic sales language.
8. Return ONLY a valid JSON object.
9. Do not include markdown code fences or text outside the JSON.

Return exactly these eight fields:

{{
    "research_summary": "A concise 2-4 sentence company summary.",

    "pain_points": [
        "Potential pain point 1",
        "Potential pain point 2",
        "Potential pain point 3"
    ],

    "buying_signals": [
        "Potential buying signal 1",
        "Potential buying signal 2",
        "Potential buying signal 3"
    ],

    "email": "A personalized cold outreach email with a subject line.",

    "linkedin_message": "A concise LinkedIn outreach message.",

    "cold_call_script": "A conversational cold call opening and discovery questions.",

    "follow_up_1": "A short first follow-up email.",

    "follow_up_2": "A short second follow-up email."
}}

OUTPUT REQUIREMENTS

- research_summary must be a string.
- pain_points must be an array of strings.
- buying_signals must be an array of strings.
- All outreach fields must be strings.
- Make the campaign relevant to the company's stated business.
- If information is insufficient, acknowledge the uncertainty.
- Do not present speculative buying signals as confirmed events.
"""
