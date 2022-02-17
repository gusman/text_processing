from nltk.tag import StanfordNERTagger

class NerTool:
    def __init__(self, ner_model, ner_app):
        self.ner_model = ner_model
        self.ner_app = ner_app
        self.ner_tagger = StanfordNERTagger(ner_model, ner_app, encoding='utf-8')
        
    def parse_text(self, text):
        rslt = self.ner_tagger.tag(text)
        return [ w[0] for w in rslt if w[1] == 'Place' ]
    
        