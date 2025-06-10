import json
import spacy
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import chromadb

# Load JSON data
with open('pib_rss_feed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

press_releases = data['press_releases']  

# Initialize models
ner_nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Initialize ChromaDB with Persistent Storage
persist_directory = "D:\\Ak project\\chroma_data" 
client = chromadb.PersistentClient(path=persist_directory)  
collection = client.create_collection(name="pib_press_collection")

# Process each press release
for idx, release in enumerate(press_releases):
    title = release.get('title', '').strip()
    link = release.get('link', '').strip()

    if not title: 
        continue

   
    doc = ner_nlp(title)
    entities = list(set([ent.text for ent in doc.ents]))  

    entities_str = ", ".join(entities) if entities else ""  

    try:
        summary = summarizer(title, max_length=20, min_length=5, do_sample=False)
        claim = summary[0]['summary_text']
    except Exception as e:
        claim = title 
    # 3. Embedding
    embedding = embedder.encode([claim])[0]

    # 4. Store in ChromaDB
    collection.add(
        ids=[str(idx)],
        documents=[title], 
        metadatas=[{
            "entities": entities_str,  
            "summary": claim,
            "link": link
        }],
        embeddings=[embedding.tolist()]
    )

    print(f"✅ Stored item {idx+1}: {title}")

print(f"🎉 All PIB items processed and stored in ChromaDB at {persist_directory}!")