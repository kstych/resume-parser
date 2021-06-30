import spacy
import re


class Engine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.initialise_response()
        
        
    def initialise_response(self):
        self.rawtext = ''
        self.response = {
                'email':[],
                'phone':[],
            }
    
        return 
    
    def extract_emails(self):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", self.rawtext)
        if email:
            for i in list(set(email)):
                self.response['email'].append(i.strip(';'))
        
    def extract_ner(self):
        doc = self.nlp(self.rawtext)
        self.response['ner']=doc.to_json()
        
    def extract_phones(self):
        phone = [i[0] for i in re.findall("((\(?)(\+?)(\d{1,3})(\)?)( ?)([-\. \d]{9,11}))", self.rawtext)]
        if phone:
            for i in list(set(phone)):
                if len(i)>10:
                    i = '+'+i
                self.response['phone'].append(i)
        
        
    def tokeninzer(self, text):
        self.initialise_response()
        self.rawtext = text
        print(self.rawtext)
        #self.extract_ner()
        self.extract_phones()
        self.extract_emails()
        return self.response
