import spacy
import re
import os
from spacy.matcher import Matcher
from .grex.gen import KB_Extractor, BASE_PATH

# Engine Class
class Engine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.initialise_response()
        

    def initialise_response(self):
        self.rawtext = ''
        self.response = {
                'email':[],
                'phone':[],
                'skills':[],
                'education':[],
                'names':[],
                'nationality':[],
                'designation':[],
                'gender':[],
            }
    
        return 
    
    # extract emails
    def extract_emails(self):
        email = re.findall("((\S)+@[\w]+\.[\w]+)", self.rawtext)
        if email:
            for i in list(set([i[0] for i in email])):
                self.response['email'].append(i.strip(';').strip())
    
    # extract name
    def extract_name(self):
        NAME_PATTERN = [
            [
                {'POS': 'PROPN'}, 
                {'POS': 'PROPN'}, 
                {'POS': 'PROPN'},
            ]
        ]
        matcher = Matcher(self.nlp.vocab)
        matcher.add('NAME',NAME_PATTERN)
        matches = matcher(self.doc)
        output = []
        # noice reducer
        for match_id, start, end in matches:
            span = self.doc[start:end]
            for i in span.ents:
                if i.label_=='PERSON':
                    output.append(i.text)
        
        # noice reduction
        self.response['names'] = output
        
    
    # extracting skills
    def extract_skills(self):
        skills = [line.strip().lower() for line in open(os.path.join(BASE_PATH, 'KB/Skills.txt'), 'r')]
        regex = '|'.join(['(?!\W){}(?=\W)'.format(re.escape(i)) for i in skills])
        cregex = re.compile(regex, re.I)
        result = cregex.findall(self.rawtext)
        self.response['skills'] = list(set([i.capitalize() for i in result if i]))
        
    # extract education
    def extract_education_course(self):
        pattern = '|'.join(['((?!\W){}(?=\W))'.format(re.escape(line.strip('\n'))) for line in open(os.path.join(BASE_PATH, 'KB/Education.txt'), 'r')])
        regex = re.compile(pattern, re.I)
        course = [''.join(i).strip() for i in regex.findall(self.rawtext)]
        self.response['education'] = [i.upper() for i in set([i.lower() for i in course]) if i]
         
    
    def extract_ner(self):
        self.doc = self.nlp(self.rawtext)
        
        
    
    # extract phones
    def extract_phones(self):
        phone = [i[0] for i in re.findall("((\(?)(\+?)(\d{1,3})(\)?)( ?)([-\. \d]{9,11}))", self.rawtext)]
        if phone:
            for i in list(set(phone)):
                if len(i)>10:
                    if '+' not in i:
                        i = '+'+i
                self.response['phone'].append(i)
    
    # extract nationality
    def extract_nationality(self):
        nationality = [line.strip().lower() for line in open(os.path.join(BASE_PATH, 'KB/Nationality.txt'), 'r')]
        regex = '|'.join(['(?!\W){}(?=\W)'.format(re.escape(i)) for i in nationality])
        cregex = re.compile(regex, re.I)
        result = cregex.findall(self.rawtext)
        self.response['nationality'] = list(set([i.capitalize() for i in result if i]))
        return 

    # extract designation
    def extract_designation(self):
        designation = [line.strip().lower() for line in open(os.path.join(BASE_PATH, 'KB/Designation.txt'), 'r')]
        regex = '|'.join(['(?!\W){}(?=\W)'.format(re.escape(i)) for i in designation])
        cregex = re.compile(regex, re.I)
        result = cregex.findall(self.rawtext)
        self.response['designation'] = list(set([i.capitalize() for i in result if i]))
        return 
    
    # extract gender
    def extract_gender(self):
        gender = [line.strip().lower() for line in open(os.path.join(BASE_PATH, 'KB/Gender.txt'), 'r')]
        regex = '|'.join(['(?!\W){}(?=\W)'.format(re.escape(i)) for i in gender])
        cregex = re.compile(regex, re.I)
        result = cregex.findall(self.rawtext)
        self.response['gender'] = list(set([i.capitalize() for i in result if i]))
        return 




    def include_ntlk_data(self):
        self.response['Suggestions'] = KB_Extractor(self.rawtext)
        return 

    def tokeninzer(self, text):
        self.initialise_response()
        self.rawtext = text
        self.doc = None
        self.extract_ner()

        self.extract_skills()
        self.extract_phones()
        self.extract_emails()
        self.extract_education_course()
        self.extract_name()
        self.extract_nationality()
        self.extract_designation()
        self.extract_gender()

        self.include_ntlk_data()
        return self.response
