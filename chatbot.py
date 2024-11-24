from flask import Flask, request, jsonify
import json
import spacy
import nltk
from nltk.tokenize import word_tokenize

# Initialize Flask app
app = Flask(__name__)

# Load local scam data
with open("scams.json", "r", encoding="utf-8") as file:
    scam_data = json.load(file)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Function to check for scams
def check_scam(query):
    query_tokens = set(word_tokenize(query.lower()))
    for scam in scam_data:
        company_tokens = set(word_tokenize(scam["company_name"].lower()))
        if query_tokens & company_tokens:  # Overlap between query and company name
            return {
                "company_name": scam["company_name"],
                "scam_status": scam["scam_status"],
                "description": scam["description"],
                "evidence": scam["evidence"]
            }
    return {"scam_status": "Unknown", "message": "No records found for this query."}

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chatbot():
    user_input = request.json.get("query", "")
    if not user_input:
        return jsonify({"error": "No input provided."})

    # Analyze input and check for scams
    result = check_scam(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
