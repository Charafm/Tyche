import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

if __name__ == "__main__":
    sample = "Apple acquired Beats for $3B in 2014."
    print(extract_entities(sample))
