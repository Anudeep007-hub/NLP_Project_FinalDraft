from flask import Flask, jsonify, request
from spell_corrector import get_close_matches
from flask_cors import CORS 
import json
from trie import Trie

app = Flask(__name__)


CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

with open("../corpus/data_mid_2.json", 'r') as file:
    data = json.load(file)

def chatbot_response(user_input):
    print(user_input)
    return user_input



# Initialize the Trie
trie = Trie()
with open('../corpus/words.json', 'r') as file:
    words = json.load(file)

for word in words:
    trie.insert(word)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    response = chatbot_response(user_input)
    return jsonify({"response": response})

from flask import make_response

@app.route('/suggest', methods=['GET'])
def suggest():
    prefix = request.args.get('prefix', '')
    suggestions = trie.search_prefix(prefix)
    response = make_response(jsonify(suggestions))
    response.headers.add('Access-Control-Allow-Origin', '*')  
    return response

@app.route('/spellcorrect', methods=['GET'])
def spell_correct():
    word = request.args.get('word', "").strip().lower()
    if not word:
        return jsonify([])

    # Find closest matches based on edit distance 
    corrections = get_close_matches(word, words, n=3, cutoff=0.6)  # Adjust cutoff for tolerance
    response = make_response(jsonify(corrections))
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response

if __name__ == "__main__":
    app.run(debug=True)
