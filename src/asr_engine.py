import os
import google.generativeai as genai
from src.utils import setup_logging, get_api_key

logger = setup_logging(__name__)

class ASREngine:
    def __init__(self):
        self.api_key = get_api_key()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            logger.warning("No Google API Key found. ASR will return mock data.")
            self.model = None

    def transcribe(self, audio_path):
        """
        Transcribes the audio file using Gemini API.
        """
        if not self.model:
            return "This is a mock transcript because no API key was provided. The user is pitching a revolutionary AI product that solves a big problem."

        logger.info(f"Uploading {audio_path} to Gemini for transcription...")
        try:
            # Upload the file
            audio_file = genai.upload_file(path=audio_path)
            
            # Prompt for transcription
            response = self.model.generate_content(
                [
                    "Please provide a verbatim transcription of this audio file. Do not add any commentary.",
                    audio_file
                ]
            )
            
            transcript = response.text
            logger.info("Transcription complete.")
            return transcript
            
        except Exception as e:
            logger.error(f"ASR failed: {e}")
            return "Error during transcription."
