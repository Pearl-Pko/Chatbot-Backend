import re 

course_code_regex = r"\w{3}\d{3}"
course_code_pattern = re.compile(course_code_regex)

department_regex = r"computer science|physics|geology|mathematics|chemistry|statistics|csc|phy|gly|mth|chm|sta"
department_pattern = re.compile(department_regex)

level_regex = r"([1-4]00)"
level_pattern = re.compile(level_regex)

semester_regex = r"(first|second)"
semester_pattern = re.compile(semester_regex)

class ResponseGenerator():
    def response(self, intents, course_info, intent_tag, question):
        raise NotImplementedError
    
class RuleBaseGenerator(ResponseGenerator):
    def response(self, intents, course_info, intent_tag, question):
        return intents[intent_tag]

class NERGenerator(ResponseGenerator):
    def response(self, intents, course_info, intent_tag, question):
        raise NotImplementedError

class PrerequisitesGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        matches = re.findall(course_code_pattern, question)
        if matches and matches[0] in course_info["courses"]:
            prerequisites = course_info["courses"][matches[0]]["prerequisites"]
            if len(prerequisites):
                res = f'The prerequisites for {matches[0]} are {", ".join(course_info["courses"][matches[0]]["prerequisites"])}'
            else:
                res = f'{matches[0]} does not have any prerequisite courses'
        else: 
            res = "Not a valid course code"
        return [res]
    
class CreditLoadGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        matches = re.findall(course_code_pattern, question)
        if matches and matches[0] in course_info["courses"]:
            res = f'The credit load for {matches[0]} is {course_info["courses"][matches[0]]["credits"]} credits'
        else: 
            res = "Not a valid course code"
        return [res]
    
class CourseNameGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        matches = re.findall(course_code_pattern, question)
        if matches and matches[0] in course_info["courses"]:
            res = f'The course name for {matches[0]} is {course_info["courses"][matches[0]]["name"]}'
        else: 
            res = "Not a valid course code"
        return [res]

class CourseStatusGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        matches = re.findall(course_code_pattern, question)
        if matches and matches[0] in course_info["courses"]:
            res = f'{matches[0]} is a {course_info["courses"][matches[0]]["status"]} course'
        else: 
            res = "Not a valid course code"
        return [res]

class LevelCoursesGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        level = re.findall(level_pattern, question)
        
        department = re.findall(department_pattern, question)
        
        if level and department:
            c = "\n"
            res = f'The {level[0]} level courses in {department[0]} are \n{c.join(course_info["department"][department[0]]["courses"][level[0]]["first"] + course_info["department"][department[0]]["courses"][level[0]]["second"])}'
        else: 
            if not level:
                res = "Not a valid level"
            else: 
                res = "Not a valid department"
        return [res]

class SemesterCoursesGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        level = re.findall(level_pattern, question)
        semester = re.findall(semester_pattern, question)
        department = re.findall(department_pattern, question)
        
        if level and department:
            c = "\n"
            res = f'The {level[0]} level courses in {department[0]} are \n{c.join(course_info["department"][department[0]]["courses"][level[0]][semester[0]])}'
        else: 
            if not level:
                res = "Not a valid level"
            else: 
                res = "Not a valid department"
        return [res]

class HODInquiryGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        department = re.findall(department_pattern, question)
        
        if department:
            res = f'The Head of Department of {department[0]} is {course_info["department"][department[0]]["hod"]}'
        else: 
            res = "Not a valid department"
        return [res]

class InformationAboutLecturerGenerator(NERGenerator):
    def response(self, intents, course_info, intent_tag, question):
        question = question.lower()
        lecturers_regex = "|".join(course_info["lecturers"].keys())
        lecturer = re.findall(lecturers_regex, question)
        if lecturer:
            if lecturer[0] in course_info["lecturers"]:
                res = course_info["lecturers"][lecturer[0]]
            else:
                res = f'I do not have any information about this lecturer'
        else: 
            res = f'I do not have any information about this lecturer'
        return [res]

class ResponseGeneratorFactory(): 
    @staticmethod 
    def getResponseGenerator(responseType):
        if responseType == "Prerequisites":
            return PrerequisitesGenerator()
        elif responseType == "Credit Load":
            return CreditLoadGenerator()
        elif responseType == "Course Name":
            return CourseNameGenerator()
        elif responseType == "Course Status":
            return CourseStatusGenerator()
        elif responseType == "Level Courses":
            return LevelCoursesGenerator()
        elif responseType == "Semester Courses":
            return SemesterCoursesGenerator()
        elif responseType == "HOD Inquiry":
            return HODInquiryGenerator()
        elif responseType == "Information about lecturer":
            return InformationAboutLecturerGenerator()
        else: 
            return RuleBaseGenerator()