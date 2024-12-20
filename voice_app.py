from flask import Flask, render_template, request, jsonify
import os
from groq import Groq
from database_config import *
from textprocess import get_customer_query
from sentiment_analysis import analyze_query_sentiment

def Voice_App():
    app = Flask(__name__)

    # Set API key
    os.environ["GROQ_API_KEY"] = "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"
    client = Groq()

    def speech2text(filename):
        with open(filename, "rb") as file:
            translation = client.audio.translations.create(
                file=(filename, file.read()),
                model="whisper-large-v3",
                response_format="text",
                temperature=0.0
            )
            return translation

    @app.route("/")
    def index():
        return render_template("voice/index.html")

    @app.route("/submit", methods=["POST"])
    def submit_audio():
        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        audio_file = request.files["audio"]
        temp_filename = "temp_audio.mp3"
        audio_file.save(temp_filename)

        try:
            transcription = speech2text(temp_filename)
            os.remove(temp_filename)

            setup_database()
            sen = analyze_query_sentiment(transcription)
            interaction = (
            generate_interaction_id(),  # interaction_id (UUID)
            "customer_001",             # user_id
            "chat",                     # channel
            get_current_timestamp(),    # timestamp (to be generated)
            f"User: {transcription}\n",  # message_logs
            get_customer_query(transcription, keyword_extraction = True),  # issue_description
            sen[0],
            sen[1],
            )
            insert_interaction(interaction)

            return jsonify({"transcription": transcription})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return app

if __name__ == "__main__":
    Voice_App().run(debug=True, port=5001, use_reloader=False)

