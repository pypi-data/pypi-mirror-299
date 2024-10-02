import os
import requests
from openai import OpenAI
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Audio:
    BACKEND_URL = "https://memu-sdk-backend-85afb0b12f2a.herokuapp.com/"
    MIDDLEWARE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com/"

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key
        self.client_name = self.validate_api_key()
        self.openai_api_key = self.get_openai_api_key()
        self.client = OpenAI(api_key=self.openai_api_key)

    def validate_api_key(self) -> str:
        """Validate MeMu API key by calling the backend."""
        response = self.make_request(self.BACKEND_URL, "GET", "/validate_api_key", params={"api_key": self.memu_api_key})
        return response.get("client_name")

    def get_openai_api_key(self):
        """Fetch the OpenAI API key from the backend."""
        try:
            response = self.make_request(self.BACKEND_URL, "GET", "/openai_api_key", params={"api_key": self.memu_api_key})
            if response and "openai_api_key" in response:
                return response["openai_api_key"]
            else:
                raise ValueError("OpenAI API key not found in the response.")
        except Exception as e:
            logger.error(f"Failed to get OpenAI API key: {e}")
            raise

    def make_request(self, url, method: str, endpoint: str, params=None, json=None) -> dict:
        """Generic method to handle API calls."""
        full_url = f"{url}{endpoint}"
        try:
            response = requests.request(method, full_url, params=params, json=json)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Error in API request to {endpoint}")

    def check_balance(self, minimum_required: float) -> bool:
        """Helper method to check if the client has enough balance."""
        current_balance = self.make_request(self.BACKEND_URL, "GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        if current_balance < minimum_required:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required} is required to proceed. Current balance: ${current_balance}.")
        return True

    def reencode_audio(self, input_path: str, output_path: str, target_format: str = "wav") -> str:
        """Re-encodes the audio file to a specified format."""
        logger.info(f"Re-encoding audio file: {input_path} to {output_path}")
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=target_format, parameters=["-ar", "16000", "-ac", "1"])
        return output_path

    def split_audio(self, audio_file_path: str, chunk_length_ms: int = 600000) -> list:
        """Splits an audio file into smaller chunks and returns file paths."""
        logger.info(f"Splitting audio file: {audio_file_path}")
        audio = AudioSegment.from_file(audio_file_path)
        chunk_file_paths = []
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunk_file_path = f"{audio_file_path}_{i // chunk_length_ms}.wav"
            chunk.export(chunk_file_path, format="wav")
            chunk_file_paths.append(chunk_file_path)
        return chunk_file_paths

    def transcribe_audio_chunk(self, audio_file_path: str, language: str = "en") -> dict:
        """Transcribes a single audio chunk using OpenAI Whisper."""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    temperature=0,
                    response_format="verbose_json",
                    prompt="You are the best medical transcriber in the world. Transcribe the following audio file. Ensure accuracy and correct any errors."
                )
            logger.info(f"Verbose transcription response: {transcription}")
            return transcription
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise e

    def transcribe_audio_file(self, file_path: str, language: str = "en") -> str:
        """Handles re-encoding, splitting, transcribing, and sending transcription for correction."""
        
        # Step 1: Check balance before transcription
        self.check_balance(10.00)

        # Step 2: Re-encode the audio file
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            reencoded_file_path = self.reencode_audio(file_path, f"{temp_audio_file.name}_reencoded.wav")

        # Step 3: Split the audio into chunks and transcribe
        audio_chunks = self.split_audio(reencoded_file_path)
        full_transcription = ""
        total_duration = 0

        for chunk_file_path in audio_chunks:
            transcription_data = self.transcribe_audio_chunk(chunk_file_path, language=language)
            full_transcription += transcription_data.text + "\n"
            total_duration += transcription_data.duration / 60  # Convert to minutes
            os.remove(chunk_file_path)  # Clean up chunk files

        os.remove(reencoded_file_path)

        if full_transcription.strip():
            # Step 4: Send transcription for correction via middleware
            corrected_transcription = self.send_for_correction(full_transcription, total_duration, language)
            return corrected_transcription
        else:
            raise ValueError("Transcription failed: no text was transcribed.")

    def send_for_correction(self, transcription_text: str, total_duration: float, language: str = "en") -> str:
        """Send the transcribed text to the middleware for correction."""
        logger.info("Sending transcription for correction.")
        payload = {
            "transcription_text": transcription_text,
            "duration_minutes": total_duration,
            "language": language,
            "api_key": self.memu_api_key
        }
        try:
            response = self.make_request(self.MIDDLEWARE_URL, "POST", "/correct_transcription", json=payload)
            corrected_transcription = response.get("corrected_transcription")
            return corrected_transcription
        except Exception as e:
            logger.error(f"Failed to correct transcription: {e}")
            raise e
