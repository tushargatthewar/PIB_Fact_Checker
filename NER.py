import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Input text
text = "The Indian government has announced free electricity to all farmers starting July 2025."

# Process the text
doc = nlp(text)

# Print Named Entities
print("Named Entities, Phrases, and Labels:")
for ent in doc.ents:
    print(f"{ent.text} ({ent.label_})")
