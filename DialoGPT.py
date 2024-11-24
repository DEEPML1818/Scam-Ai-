import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from googletrans import Translator

# Load a faster and smaller conversational model
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Translator for multilingual support
translator = Translator()

# Load scams dataset
with open("scams.json", "r", encoding="utf-8") as f:
    scams_data = json.load(f)

# Scam types for general knowledge
scam_types = {
    "Ponzi scheme": "A Ponzi scheme is a type of investment scam that promises high returns with little risk, using new investors' funds to pay earlier investors.",
    "Fake investment": "Fake investments lure victims by promising high profits in non-existent or fraudulent ventures.",
    # Add more scam types and descriptions as needed
}

def search_scams(query, language):
    """Search for scams related to the query and translate if needed."""
    for scam in scams_data:
        if query.lower() in scam["description"].lower() or query.lower() in scam["company_name"].lower():
            response = (
                f"Company: {scam['company_name']}\n"
                f"Description: {scam['description']}\n"
                f"Status: {scam['scam_status']}\n"
                f"Evidence: {scam['evidence']}"
            )
            # Translate if the language is not English
            if language != "en":
                response = translator.translate(response, src="en", dest=language).text
            return response
    return None  # No scam found

def explain_scam_type(scam_type, language):
    """Explain a scam type and translate if needed."""
    response = scam_types.get(scam_type, "Sorry, I don't have information on this scam type.")
    if language != "en":
        response = translator.translate(response, src="en", dest=language).text
    return response

def fallback_response(user_input, user_language):
    """Generate fallback conversational responses or indicate inability to answer."""
    # Encode input and generate response
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = new_input_ids
    try:
        chat_history = model.generate(bot_input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)
        bot_response = tokenizer.decode(chat_history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    except Exception:
        bot_response = "I'm sorry, I can't answer that right now."

    # Translate response if necessary
    if user_language != "en":
        bot_response = translator.translate(bot_response, src="en", dest=user_language).text
    return bot_response

# Language preference setup
print("Chatbot: Welcome! Before we start, please select your preferred language.")
user_language = input("Preferred language (en, ms, ta, zh): ").strip().lower()

print("Chatbot: Hi! Type 'exit' to end the chat.")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    # Handle scam queries first
    scam_response = search_scams(user_input, user_language)
    if scam_response:
        print(f"Chatbot (Dataset):\n{scam_response}")
        continue

    # Handle scam type explanations
    for scam_type in scam_types.keys():
        if scam_type.lower() in user_input.lower():
            scam_info = explain_scam_type(scam_type, user_language)
            print(f"Chatbot (Scam Info):\n{scam_info}")
            break
    else:
        # Handle fallback responses
        bot_response = fallback_response(user_input, user_language)
        print(f"Chatbot: {bot_response}")
