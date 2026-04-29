from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, render_template
from services.classifier import predict_news
from services.explainability import get_important_words
from services.retrieval import get_fact_check
from services.verifier import verify_news
from utils.text_processing import build_query

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Please enter a valid headline"})

    # Classifier 
    result = predict_news(text)

    # Important words
    words = get_important_words(text)

    # Retrieval 
    query = build_query(text)

    context = get_fact_check(query)

    if isinstance(context, list):
        context = " ".join(context) 

    #  LLM decision
    verification = verify_news(text, context)

    
    if "Verdict: TRUE" in verification:
        final_prediction = "Real"
    elif "Verdict: FALSE" in verification:
        final_prediction = "Fake"
    else:
        final_prediction = "Uncertain"

    return jsonify({
        "prediction": final_prediction,
        "confidence": result["confidence"],
        "important_words": words,
        "verification": verification
    })


if __name__ == "__main__":
    app.run(debug=True)