from flask import Flask, render_template, redirect
from subprocess import Popen
import time

app = Flask(__name__)

# Function to run the Chatbot App on a separate process
def run_chatbot():
    # Start the Chatbot App in a new process on port 5002
    Popen(["python", "chatbot_app.py"])

# Function to run the Voice App on a separate process
def run_voice():
    # Start the Voice App in a new process on port 5001
    Popen(["python", "voice_app.py"])

# Route to serve the main page with the customer service portal
@app.route('/')
def home():
    return render_template('landing.html')

# Route for Chatbot page (this will start the chatbot app and redirect)
@app.route('/chatbot')
def chatbot():
    # Run the chatbot app in a separate process
    run_chatbot()
    time.sleep(10)  # Give the chatbot app a moment to start
    # Redirect to the chatbot page
    while True:
        try:
            return redirect('http://127.0.0.1:5002/')
        except:
            print("Not yet online...")


# Route for Voice Complaint page (this will start the voice app and redirect)
@app.route('/voice')
def voice():
    # Run the voice app in a separate process
    run_voice()
    time.sleep(10)  # Give the voice app a moment to start
    # Redirect to the voice complaint page
    while True:
        try:
            return redirect('http://127.0.0.1:5001/')
        except:
            print("Non yet online")

# Start the main Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5000)
