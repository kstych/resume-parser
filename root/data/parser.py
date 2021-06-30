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
                'skills':[],
            }
    
        return 
    
    def extract_emails(self):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", self.rawtext)
        if email:
            for i in list(set(email)):
                self.response['email'].append(i.strip(';'))
    
    # extracting skills
    def extract_skills(self, np):
        skills = [line.strip() for line in open('skills_match.txt', 'r')]
        tokens = [token.text for token in np if not token.is_stop]
        skillset = []
        # check for one-grams
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)
        
        # check for bi-grams and tri-grams
        for token in np.noun_chunks:
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)
        self.response['skills'] = [i.capitalize() for i in set([i.lower() for i in skillset])]
        
       
    
    def extract_ner(self):
        doc = self.nlp(self.rawtext)
        self.extract_skills(doc)
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
        self.extract_ner()
        self.extract_phones()
        self.extract_emails()
        return self.response
