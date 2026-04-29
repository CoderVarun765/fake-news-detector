from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def verify_news(headline, context):
    prompt = f"""
You are an expert fact-checking system.

Your task is to determine whether the USER HEADLINE is factually correct.

========================
HOW TO THINK:
========================
1. FIRST evaluate the headline using real-world knowledge
2. THEN use the context as supporting evidence (if useful)
3. If context is irrelevant or incorrect → IGNORE it

========================
IMPORTANT RULES:
========================
- HEADLINE is PRIMARY (most important)
- CONTEXT is SECONDARY (only for support)
- DO NOT reject a headline just because context is weak
- DO NOT blindly trust context
- If unsure → return UNCERTAIN
- Do NOT hallucinate unknown facts

========================
DECISION:
========================
TRUE:
- If the core event in the headline actually happened

FALSE:
- If the event is incorrect or did not happen

UNCERTAIN:
- If not enough reliable information OR future event

========================
OUTPUT RULES:
========================
- Explanation must:
  • First explain based on headline
  • Then optionally reference context if helpful
- If TRUE → give more details about the event
- If FALSE → give correct real-world information
- If UNCERTAIN → say not enough info

========================
USER HEADLINE:
{headline}

RETRIEVED CONTEXT:
{context if context else "No relevant context"}

========================
OUTPUT FORMAT:
========================
Verdict: TRUE / FALSE / UNCERTAIN
Explanation: Clear reasoning (headline first, then context if useful)
Correct Information: Real fact or "Not enough information"
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text

    except Exception:
        return """Verdict: UNCERTAIN
Explanation: Verification failed
Correct Information: Not enough information"""