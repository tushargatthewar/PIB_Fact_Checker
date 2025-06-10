import json
import spacy
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import chromadb

# Load JSON data
with open('pib_rss_feed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

press_releases = data['press_releases']  # Extract press releases list

# Initialize models
ner_nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Initialize ChromaDB with Persistent Storage
persist_directory = "D:\\Ak project\\chroma_data"  # Specify the folder for storage
client = chromadb.PersistentClient(path=persist_directory)  # Use PersistentClient
collection = client.create_collection(name="pib_press_collection")

# Process each press release
for idx, release in enumerate(press_releases):
    title = release.get('title', '').strip()
    link = release.get('link', '').strip()

    if not title:  # Skip if title is empty
        continue

    # 1. NER Extraction
    doc = ner_nlp(title)
    entities = list(set([ent.text for ent in doc.ents]))  # Unique named entities

    # Convert entities list to a comma-separated string
    entities_str = ", ".join(entities) if entities else ""  # Handle empty entities list

    # 2. Summarization
    try:
        summary = summarizer(title, max_length=20, min_length=5, do_sample=False)
        claim = summary[0]['summary_text']
    except Exception as e:
        claim = title  # Fallback: use title itself if summarizer fails

    # 3. Embedding
    embedding = embedder.encode([claim])[0]

    # 4. Store in ChromaDB
    collection.add(
        ids=[str(idx)],
        documents=[title],  # Original title
        metadatas=[{
            "entities": entities_str,  # Use string instead of list
            "summary": claim,
            "link": link
        }],
        embeddings=[embedding.tolist()]
    )

    print(f"✅ Stored item {idx+1}: {title}")

print(f"🎉 All PIB items processed and stored in ChromaDB at {persist_directory}!")