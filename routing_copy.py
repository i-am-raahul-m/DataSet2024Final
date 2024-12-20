import os
from groq import Groq
from database_config import *
from textprocess import get_customer_query

os.environ["GROQ_API_KEY"] = "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"
prompt = """You are a backend customer service bot. 
\nDetermine whether the issue raised by the customer, can be solved by AI assistant or only by a manual agent.
\nRespond only with either: 'AI' or 'manual'. No other extra words. Strictly only one word response."""

with open("routing_capabilities.txt", "r") as f:
    capabilities = f.read()
capabilites = "The capabilities of the AI assistant are:\n" + capabilities

prompt += capabilities


def get_groq_response(request_details: str) -> str:
    # Initialize the Groq client
    client = Groq()

    # Configure the message for the request
    input_text = (
        f"The following is a customer query or request: {request_details}\n\n"
        "Should this request be handled by an AI assistant or a manual agent? Respond with either 'AI assistant' or 'Manual agent'."
    )

    # Send the request to the model
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text},
        ],
        model="llama3-8b-8192",  # Choose the appropriate model
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    # Return the response text from the model
    return chat_completion.choices[0].message.content

# Example usage
def main():
    for customer in get_unique_customer_keys():
        request = retrieve_user_timestamped_messages(customer)
        # print(request)
        summary = get_customer_query(request)
        # print(summary)
        setup_database()
        insert_customer_summary(customer, summary)
        print(get_groq_response(request))
    
