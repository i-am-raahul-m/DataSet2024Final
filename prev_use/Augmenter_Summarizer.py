from transformers import pipeline

matching_texts = "The French Revolution (1789–1799) was a pivotal period in world history that radically transformed France and influenced global politics. It marked the transition from absolute monarchy to a republic, overthrowing feudal privileges and introducing democratic ideals."

# Load the pre-trained summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Assuming 'matching_texts' is the text fetched
text_to_summarize = ''.join(matching_texts)  # Combine all matching texts into one string

# Summarize the retrieved text
summary = summarizer(text_to_summarize, max_length=200, min_length=25, do_sample=False)

# Print the summary
text = summary[0]['summary_text']
print(text)