from joblib import load 
import json 
import random
from converse import ResponseGeneratorFactory
from flask import Flask, request
from flask_cors import CORS
import nltk
import os

app = Flask(__name__)

CORS(app)

#loads the necessary data 
pipeline = load(os.path.join(os.environ["SHARED"], "model.joblib"))

with open(os.path.join(os.environ["SHARED"], "data.json"), "r") as file:
    intents = json.loads(file.read()) 
    
with open("course info.json", "r") as file:
    course_info = json.loads(file.read())   

["Prerequisites", "Credit Load", "Course Name", "Course Status", "Level Courses", "Semester Courses", "HOD Inquiry", "Information about Lecturer"]
intent_ids = list(zip(intents.keys(), intents.values()))

@app.route("/reply", methods=["POST"])
def main():
    user_input = request.json["message"]    
    print(user_input)    
    intent_id = pipeline.predict([user_input])[0]
    intent = intent_ids[intent_id]
    intent_tag = intent[0]
    
    responseGenerator = ResponseGeneratorFactory.getResponseGenerator(intent_tag)
    res = responseGenerator.response(intents, course_info, intent_tag, user_input)
    
    res = random.choice(res)
    return {"message": res}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)