from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from database_config import *
from textprocess import get_customer_query
from sentiment_analysis import analyze_query_sentiment

def Chatbot_App(debug = False):
    # Set up the environment variable for the API key
    os.environ["GROQ_API_KEY"] = "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"

    # Initialize the Groq client
    client = Groq()

    app = Flask(__name__)

    # Route to serve the homepage with the chatbot interface
    @app.route('/')
    def home():
       return render_template('chatbot/index.html')

    # Route to handle the chat request and respond with the chatbot's reply
    @app.route('/chat', methods=['POST'])
    def chat():
        user_input = request.json['message']
        
        # Customize the system instruction based on customer service context
        system_message = """You are a helpful assistive customer service bot. Help customers cordially with their requested queries.
\nReply poiltely and professionally. Reply with concise answers."""
        
        # Send query to Groq's chat model with the customized system instruction
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ],
                model="llama3-8b-8192",  # Use your desired model
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            
            bot_response = chat_completion.choices[0].message.content
        except Exception as e:
            bot_response = f"Error: {e}"

        setup_database()
        sen = analyze_query_sentiment(user_input)
        interaction = (
        generate_interaction_id(),  # interaction_id (UUID)
        "customer_001",             # user_id
        "chat",                     # channel
        get_current_timestamp(),    # timestamp (to be generated)
        f"User: {user_input}\nBot: {bot_response}\n",  # message_logs
        get_customer_query(user_input, keyword_extraction = True),  # issue_description
        sen[0],
        sen[1],
        )
        insert_interaction(interaction)

        return jsonify({'response': bot_response})

    return app

if __name__ == '__main__':
    Chatbot_App().run(debug=True, port=5002, use_reloader=False)
