from joblib import load 
from tokenizer import tokenize_and_stem
import json 
import random
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

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