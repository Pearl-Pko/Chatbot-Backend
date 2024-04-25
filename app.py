from joblib import load 
import json 
import random
from converse import ResponseGeneratorFactory

#loads the necessary data 
pipeline = load("model.joblib")
with open("data.json", "r") as file:
    intents = json.loads(file.read()) 
    
with open("course info.json", "r") as file:
    course_info = json.loads(file.read())   

["Prerequisites", "Credit Load", "Course Name", "Course Status", "Level Courses", "Semester Courses", "HOD Inquiry", "Information about Lecturer"]

def main():
    intent_ids = list(zip(intents.keys(), intents.values()))
    # print(intent_ids)
    while True: 
        user_input = input("User: ")
        
        intent_id = pipeline.predict([user_input])[0]
        intent = intent_ids[intent_id]
        intent_tag = intent[0]
        print(intent_tag)
        responseGenerator = ResponseGeneratorFactory.getResponseGenerator(intent_tag)
        res = responseGenerator.response(intents, course_info, intent_tag, user_input)
        # intent_res = intent[1]
        
        res = random.choice(res)
        print(f"AI: {res}")

main()