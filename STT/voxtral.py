import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "voxtral-mini-latest"
client = Mistral(api_key=api_key)

def transcribe(file_path):
    
    with open(file_path, "rb") as f:
        transcription_response = client.audio.transcriptions.complete(
            model=model,
            file={
                "content": f,
                "file_name": "output.wav",
            },
            language="de"
        )
    return transcription_response.text