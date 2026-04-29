from serpapi import GoogleSearch
from config import SERP_API_KEY

def clean_text(text):
    if not text:
        return None
    return text.strip()


def get_fact_check(query):
    try:
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "num": 5,
            "tbm": "nws",
            "hl": "en"
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        snippets = []

        for res in results.get("news_results", []):
            title = res.get("title", "")
            snippet = res.get("snippet", "")

            combined = f"{title}. {snippet}"
            cleaned = clean_text(combined)

            if cleaned:
                snippets.append(cleaned)

        return " ".join(snippets[:3])  # ✅ return STRING (important)

    except Exception:
        return ""