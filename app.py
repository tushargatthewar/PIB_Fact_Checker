import streamlit as st
import spacy
from sentence_transformers import SentenceTransformer
import chromadb
from transformers import pipeline
import google.generativeai as genai
import os

# Configure Gemini API
os.environ["GOOGLE_API_KEY"] = "AIzaSyC8N8FlqCDaDfmRM5mZ_oHuLR3lYDeHyCw" 
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load models
ner_nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Initialize ChromaDB
persist_directory = "D:\\Ak project\\chroma_data"
client = chromadb.PersistentClient(path=persist_directory)
collection = client.get_or_create_collection(name="pib_press_collection")

# Streamlit App UI
st.title("🔍 PIB Fact Checker App (with Gemini Verdict)")
st.write("Enter a news claim to verify against PIB official facts:")

# User input
user_input = st.text_area("Your News Claim or Statement", height=150)

if st.button("Check Facts"):
    if user_input.strip() == "":
        st.warning("Please enter some text to check.")
    else:
     
        doc = ner_nlp(user_input)
        user_entities = list(set([ent.text for ent in doc.ents]))

 
        try:
            summary = summarizer(user_input, max_length=20, min_length=5, do_sample=False)
            extracted_claim = summary[0]['summary_text']
        except Exception as e:
            extracted_claim = user_input


        query_embedding = embedder.encode([extracted_claim])[0]
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=3
        )

        distances = results.get("distances", [[]])[0]  
        threshold = 0.1 

        st.subheader("📝 Extracted Main Claim:")
        st.success(extracted_claim)

        st.subheader("🔍 Named Entities in Your Input:")
        if user_entities:
            for ent in user_entities:
                st.write(f"• {ent}")
        else:
            st.write("No named entities found.")

        st.subheader("📌 Top PIB Facts (Filtered):")
        fact_summaries = []
        found_relevant = False

        if results['documents'] and results['documents'][0]:
            for idx, (doc, distance) in enumerate(zip(results['documents'][0], distances)):
                if distance <= threshold:  
                    metadata = results['metadatas'][0][idx]
                    entities = metadata.get("entities", "")
                    summary = metadata.get("summary", "")
                    link = metadata.get("link", "")
                    
                    st.markdown(f"**Fact {idx+1}:** {doc}")
                    st.write(f"• Summary: {summary}")
                    st.write(f"• Entities: {entities if entities else 'None'}")
                    if link:
                        st.write(f"• Link: [{link}]({link})")
                    st.write("---")
                    fact_summaries.append(f"Fact {idx+1}: {summary} (Link: {link})")
                    found_relevant = True

        if not found_relevant:
            st.warning("No sufficiently relevant PIB facts found for your claim. The statement may not relate to government announcements.")

        # --------------------- Gemini Verdict -------------------------
        if found_relevant and fact_summaries:
            gemini_prompt = f"""
You are a fact-checking AI. Check if the following claim is true based on official PIB facts.

Claim:
\"{extracted_claim}\"

Official PIB Facts:
{chr(10).join(fact_summaries)}

Classify the claim as:
✅ True
❌ False
🤷 Unverifiable

Also provide a brief reasoning.

Respond in this JSON format:
{{
  "verdict": "True/False/Unverifiable",
  "reasoning": "Your brief explanation here"
}}
"""
            model = genai.GenerativeModel("gemini-1.5-flash") 
            response = model.generate_content(gemini_prompt)
            verdict_output = response.text

            st.subheader("🔮 Gemini AI Verdict:")
            st.code(verdict_output, language='json')
        elif not found_relevant:
            st.info("Gemini verdict skipped as no relevant facts were found.")
