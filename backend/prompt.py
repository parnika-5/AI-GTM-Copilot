def build_prompt(company, website, description):
    return f"""
You are an elite GTM strategist and sales engineer.

Given the company info below, generate a full outbound campaign.

Company: {company}
Website: {website}
Description: {description}

Return STRICT JSON with:

- research_summary (2-4 lines)
- pain_points (bullet list)
- buying_signals (bullet list)
- email (cold outreach email)
- linkedin_message
- cold_call_script
- follow_up_1
- follow_up_2

Make it specific, realistic, and enterprise-focused.
Keep tone professional but direct.
"""