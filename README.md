# PIB_Fact_Checker
project

# 📢 PIB Fact Checker using AI, ChromaDB & Streamlit

## project Demo Link
https://www.youtube.com/watch?v=ovT2XzT3Vec

This project is an AI-powered Fact Checking system designed to verify user-entered claims against authenticated news facts from the **Press Information Bureau (PIB), Government of India**.

---

## 🚀 **Project Overview**

The project performs:

1. **Web Scraping**: Extracting the latest official news content from the PIB website.
2. **Embedding Generation**: Processing and embedding the PIB facts using **Sentence Transformers**.
3. **Real-time User Verification**: Comparing user claims against stored facts using **ChromaDB** for similarity search.
4. **Final AI Verdict**: Using **Gemini AI** to generate a final decision based on retrieved facts.

---

## 🏗️ **Project Structure**

```
├── app.py                # Main Streamlit UI & Pipeline (User Input, Fact Check, Gemini Verdict)
├── json_storage.py       # Scrapes PIB website, parses content & stores as JSON
├── embedding_storage.py  # Processes JSON data, generates embeddings & stores into ChromaDB
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)
```

---

## ⚙️ **Setup Instructions**

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pib-fact-checker.git
cd pib-fact-checker
```

---

### 2. Install Required Python Packages

```bash
pip install -r requirements.txt
```

---

### 3. File-wise Usage Instructions

---

#### 🔹 **1. `json_storage.py`**  

**Purpose**:  
Scrapes the PIB RSS feed, extracts data (title, summary, entities), and stores them in a JSON file.

**To Run**:
```bash
python json_storage.py
```

---

#### 🔹 **2. `embedding_storage.py`**  

**Purpose**:  
Reads the generated JSON file, computes sentence embeddings of each PIB fact, and stores them into **ChromaDB** for future similarity searches.

**To Run**:
```bash
python embedding_storage.py
```

---

#### 🔹 **3. `app.py`**  

**Purpose**:  
- Streamlit web app for users to enter any claim.  
- Performs NER, summarization, embedding on the user query.  
- Searches ChromaDB for the top 3 closest PIB facts.  
- Sends these to **Gemini AI** to generate the final fact-checking verdict.

**To Run**:
```bash
streamlit run app.py
```

---

## 🧩 **Technology Stack**

| Area                  | Tools/Frameworks                     |
|-----------------------|--------------------------------------|
| Web Scraping          | `feedparser`, `requests`              |
| Natural Language Processing | `spaCy`, `transformers`, `sentence-transformers` |
| Vector Database       | `ChromaDB (PersistentClient)`        |
| Frontend             | `Streamlit`                          |
| AI Verdict            | `Google Gemini AI (Generative LLM)`  |

---

## 💡 **Pipeline Summary**

1. **Data Collection** (via `json_storage.py`)
    - Parse PIB RSS feed and save data as JSON.
2. **Embedding Generation** (via `embedding_storage.py`)
    - Generate semantic embeddings for facts and store in ChromaDB.
3. **Real-Time Verification** (via `app.py`)
    - User enters a claim.
    - Extract entities & summary.
    - Generate embedding & search ChromaDB for closest facts.
    - **Gemini AI** generates the final verdict.

---

## 📌 **Example Usage (in App)**

> **User Claim**:  
> *"The government is providing free electricity to farmers from July 2025."*

✔️ The system extracts the claim, matches similar PIB facts, and gives a final **True/False/Unverifiable verdict** based on real government releases.

---

## 📂 **Persistent Storage**

All PIB facts embeddings are stored in **ChromaDB** under the `chroma_data` directory for efficient, persistent vector search.

---


## 🤝 **Contributors**

- **Your Name** — Tushar gatthewar


