import spacy



class Engine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    
    def tokeninzer(self, text):
        doc = self.nlp(text)
        return doc.to_json()
