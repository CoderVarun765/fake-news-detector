from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
)

def predict_news(text):
    result = classifier(text[:512])[0]

    label = result["label"]
    score = result["score"]

    if label == "FAKE":
        return {
            "prediction": "Fake",
            "confidence": score,
            "fake_score": score,
            "real_score": 1 - score
        }
    else:
        return {
            "prediction": "Real",
            "confidence": score,
            "fake_score": 1 - score,
            "real_score": score
        }
