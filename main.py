from joblib import load 
from tokenizer import tokenize_and_stem
import json 
import random

#loads the necessary data 
pipeline = load("model.joblib")
with open("data.json", "r") as file:
    intents = json.loads(file.read())   

def main():
    intent_ids = list(zip(intents.keys(), intents.values()))
    # print(intent_ids)
    while True: 
        user_input = input("User: ")
        
        intent_id = pipeline.predict([user_input])[0]
        intent = intent_ids[intent_id]
        intent_tag = intent[0]
        intent_res = intent[1]
        
        res = random.choice(intent_res)
        print(f"AI: {res}")

main()