# Setting Env var for API Key
from groq import Groq
import os
os.environ["GROQ_API_KEY"] = "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"

# Groq client
client = Groq()


def speech2text(filename):
  # Open the audio file
  with open(filename, "rb") as file:
      translation = client.audio.translations.create(
        file=(filename, file.read()),
        model="whisper-large-v3",
        response_format="text",
        temperature=0.0
      )

      return translation
  
if __name__ == "__main__":
   print(speech2text("french1.mp3"))