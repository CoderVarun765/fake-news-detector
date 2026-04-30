import requests
import os

# 🔑 Get HuggingFace token from environment
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def predict_news(text):
    """
    Lightweight classifier using HuggingFace API
    """

    try:
        payload = {
            "inputs": text[:512]
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # 🔍 Handle response format
        if isinstance(result, list) and len(result) > 0:
            result = result[0]

        label = result.get("label", "").upper()
        score = float(result.get("score", 0.5))

        # 🔥 Map labels properly
        if "CONTRADICTION" in label or "FAKE" in label:
            prediction = "Fake"
            fake_score = score
            real_score = 1 - score

        elif "ENTAILMENT" in label or "SUPPORT" in label or "REAL" in label:
            prediction = "Real"
            real_score = score
            fake_score = 1 - score

        else:
            prediction = "Uncertain"
            fake_score = 0.5
            real_score = 0.5

        confidence = max(fake_score, real_score)

        return {
            "prediction": prediction,
            "confidence": confidence,
            "fake_score": fake_score,
            "real_score": real_score
        }

    except Exception as e:
        print("Classifier API error:", e)

        # 🔥 Safe fallback (never crash app)
        return {
            "prediction": "Uncertain",
            "confidence": 0.5,
            "fake_score": 0.5,
            "real_score": 0.5
        }
