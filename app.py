from flask import Flask, request, jsonify, render_template
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from googletrans import Translator
from fuzzywuzzy import fuzz
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Load local scam data
with open("scams.json", "r", encoding="utf-8") as file:
    scam_data = json.load(file)

# Load conversational model and tokenizer (DialoGPT Large)
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

# Translator for multilingual support
translator = Translator()

# Scam types for general knowledge
scam_types = {
    "Ponzi scheme": "A Ponzi scheme is a type of investment scam that promises high returns with little risk, using new investors' funds to pay earlier investors.",
    "Fake investment": "Fake investments lure victims by promising high profits in non-existent or fraudulent ventures.",
}

# Predefined responses for common greetings and farewells
def get_predefined_response(user_input):
    keywords = {
        "hi": "Hello! How can I assist you today?",
        "hello": "Hi there! How can I help?",
        "bye": "Goodbye! Have a great day!",
        "goodbye": "Take care! See you next time.",
    }
    for key, response in keywords.items():
        if key in user_input:
            return response
    return None

def search_scams(query, language):
    """Search for scams related to the query with fuzzy matching."""
    best_match = None
    highest_score = 0
    for scam in scam_data:
        score = max(
            fuzz.partial_ratio(query.lower(), scam["description"].lower()),
            fuzz.partial_ratio(query.lower(), scam["company_name"].lower())
        )
        if score > 70 and score > highest_score:  # Use a threshold to avoid irrelevant matches
            highest_score = score
            best_match = scam
    
    if best_match:
        response = (
            f"Company: {best_match['company_name']}\n"
            f"Description: {best_match['description']}\n"
            f"Status: {best_match['scam_status']}\n"
            f"Evidence: {best_match['evidence']}"
        )
        if language != "en":
            response = translator.translate(response, src="en", dest=language).text
        return response

    return "No scams found matching your query."

def explain_scam_type(scam_type, language):
    """Explain a scam type and translate if needed."""
    response = scam_types.get(scam_type, "Sorry, I don't have information on this scam type.")
    if language != "en":
        response = translator.translate(response, src="en", dest=language).text
    return response

# Chat history for context (global or session-level storage)
chat_history = []

def fallback_response(user_input, user_language):
    """Generate fallback conversational responses using DialoGPT."""
    global chat_history  # Use chat history to maintain conversation flow

    # Encode the user input and previous context
    inputs = tokenizer.encode(
        f"{' '.join(chat_history)} {user_input}", 
        return_tensors="pt", 
        max_length=1000, 
        truncation=True
    )

    outputs = model.generate(
        inputs, 
        max_length=150,  # Max response length
        num_beams=5, 
        early_stopping=True
    )

    bot_response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Update chat history
    chat_history.append(user_input)
    chat_history.append(bot_response)

    if user_language != "en":
        bot_response = translator.translate(bot_response, src="en", dest=user_language).text
    return bot_response

# Serve the HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        user_input = request.json.get("query", "").strip().lower()
        user_language = request.json.get("language", "en").strip().lower()

        logging.info(f"Received input: {user_input}, Language: {user_language}")

        if not user_input:
            return jsonify({"error": "No input provided."})

        # Predefined responses
        predefined_response = get_predefined_response(user_input)  # Fetch the predefined response based on keywords
        if predefined_response:  # If a response is found
            if user_language != "en":  # Translate only if needed
                predefined_response = translator.translate(predefined_response, src="en", dest=user_language).text
            return jsonify({"response": predefined_response})

        # Scam search
        scam_response = search_scams(user_input, user_language)
        if scam_response:
            return jsonify({"response": scam_response})

        # Scam type explanation 
        for scam_type in scam_types.keys():
            if scam_type.lower() in user_input:
                scam_info = explain_scam_type(scam_type, user_language)
                return jsonify({"response": scam_info})

        # Fallback response
        fallback = fallback_response(user_input, user_language)
        return jsonify({"response": fallback})

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while processing your request."})

if __name__ == "__main__":
    app.run(debug=True)
