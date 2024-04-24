from joblib import load 
import json 
import random
from flask import Flask, request
from flask_cors import CORS
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from joblib.memory import register_store_backend
from joblib._store_backends import StoreBackendBase

class DummyStoreBackend(StoreBackendBase):
    """A dummy store backend that does nothing."""

    def _open_item(self, *args, **kwargs):
        """Open an item on store."""
        "Does nothing"

    def _item_exists(self, location):
        """Check if an item location exists."""
        "Does nothing"

    def _move_item(self, src, dst):
        """Move an item from src to dst in store."""
        "Does nothing"

    def create_location(self, location):
        """Create location on store."""
        "Does nothing"

    def exists(self, obj):
        """Check if an object exists in the store"""
        return False

    def clear_location(self, obj):
        """Clear object on store"""
        "Does nothing"

    def get_items(self):
        """Returns the whole list of items available in cache."""
        return []

    def configure(self, location, *args, **kwargs):
        """Configure the store"""
        "Does nothing"

register_store_backend("local", DummyStoreBackend)

# Custom tokenizer function that tokenizes and stems the text
def tokenize_and_stem(text):
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

app = Flask(__name__)

CORS(app)

stemmer = LancasterStemmer()

#loads the necessary data 
pipeline = load("model.joblib")
with open("data.json", "r") as file:
    intents = json.loads(file.read())   
intent_ids = list(zip(intents.keys(), intents.values()))

@app.route("/reply", methods=["POST"])
def main():
    user_input = request.json["message"]    
    print(user_input)    
    intent_id = pipeline.predict([user_input])[0]
    intent = intent_ids[intent_id]
    intent_tag = intent[0]
    intent_res = intent[1]
    
    res = random.choice(intent_res)
    return {"message": res}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)