from transformers import pipeline

# Load summarization pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Input text
text = "The Indian government has announced free electricity to all farmers starting July 2025."

# Generate summary (as proxy for main claim)
summary = summarizer(text, max_length=20, min_length=5, do_sample=False)

print("Extracted Claim (Summary):")
print(summary[0]['summary_text'])
