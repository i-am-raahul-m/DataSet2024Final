from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def get_bert_embeddings(text):
    # Tokenize input text and convert to PyTorch tensors
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    # Pass inputs through BERT model
    with torch.no_grad():
        outputs = model(**inputs)
    
    # `outputs.last_hidden_state` contains embeddings for all tokens
    # Use the `[CLS]` token embedding as a sentence representation
    cls_embedding = outputs.last_hidden_state[:, 0, :]
    
    return cls_embedding

# Example text
text = "[local, account, password]"
embedding = get_bert_embeddings(text)

print("BERT Embedding Shape:", embedding.shape)
print(embedding)
