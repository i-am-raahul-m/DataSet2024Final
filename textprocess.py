import os
from groq import Groq

# Set the Groq API key
os.environ["GROQ_API_KEY"] = "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"

def get_customer_query(conversation_text: str, keyword_extraction: bool = False) -> str:
    try:
        # Initialize the Groq client
        client = Groq()
    except:
        raise ValueError("API key is required to interact with the Groq client.")

    # Prepare the input prompt
    if keyword_extraction:
        input_text = (
            f"The following is a conversation between a customer and an agent:\n\n"
            f"{conversation_text}\n\n"
            """Extract keywords that indicate the customer's main problem. 
            \nBe sure to only extract those keywords relevant to the user's problems with the product or service, according to the context.
            \nOnly return a comma-separated Python list of the extracted keywords. Nothing else. Include the square brackets.
            \nIf the context is not a customer indicating their issues, respond with: None."""
        )
    else:
        input_text = (
            f"""The following is formatted message card conatining message logs of a conversation between a customer and an agent,
            \nAs well as keywords relating to the users complaint query:\n\n"""
            f"{conversation_text}\n\n"
            """Please extract and informatively summarize the customer's main query and requests. 
            \nMake the summary length proportional to the user's query length. Make the summary a professional and formal.
            \nIf timestamps are given give a general sense of time in the answer. But, do not over-rely on the timestamps.
            \nOnly return the summary. Not other extra text, wihtout enclosing quotation marks."""
        )

    # Configure the model and generate a response
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text},
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    # Return the generated text
    return chat_completion.choices[0].message.content


if __name__ == '__main__':
    convo = "Voice models are available in Chatgpt and Gemini, You can use only as non distractive device useful for kids replacing google search/query at present."
    print(get_customer_query(convo, keyword_extraction=False))
