import os
import requests
import logging
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend and middleware URLs
BACKEND_URL = "https://memu-sdk-backend-85afb0b12f2a.herokuapp.com/"
MIDDLEWARE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com/"

class AudioFHIR:
    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key
        self.client_name = self.validate_api_key()

    def validate_api_key(self) -> str:
        """Validate MeMu API key by calling the backend."""
        response = requests.get(f"{BACKEND_URL}/validate_api_key", params={"api_key": self.memu_api_key})
        response.raise_for_status()
        return response.json().get("client_name")

    def check_balance(self, minimum_required: float) -> bool:
        """Check if the client has enough balance."""
        current_balance = requests.get(f"{BACKEND_URL}/balance", params={"api_key": self.memu_api_key}).json().get("balance")
        if current_balance < minimum_required:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required} is required to proceed.")
        return True

    def deduct_client_balance(self, total_cost: float):
        """Deduct the total cost from the client's balance by calling the backend."""
        current_balance = requests.get(f"{BACKEND_URL}/balance", params={"api_key": self.memu_api_key}).json().get("balance")
        if current_balance < total_cost:
            raise ValueError(f"Insufficient balance to cover transcription cost. Current balance: ${current_balance}, total cost: ${total_cost}")

        # Deduct balance if sufficient
        new_balance = current_balance - total_cost
        requests.post(f"{BACKEND_URL}/balance/update", params={"api_key": self.memu_api_key}, json={"balance": new_balance})
        logger.info(f"Deducted ${total_cost} from client. New balance: ${new_balance}.")

    def reencode_audio(self, input_path: str, output_path: str, target_format: str = "wav") -> str:
        """Re-encodes the audio file to a specified format."""
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=target_format, parameters=["-ar", "16000", "-ac", "1"])
        return output_path

    def split_audio(self, audio_file_path: str, chunk_length_ms: int = 600000) -> list:
        """Splits an audio file into smaller chunks and returns file paths."""
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
            # Using Whisper for transcription
            with open(audio_file_path, 'rb') as audio_file:
                transcription = requests.post(
                    f"{BACKEND_URL}/transcribe_chunk",
                    files={"file": audio_file},
                    data={"language": language, "api_key": self.memu_api_key}
                ).json()
            return transcription
        except Exception as e:
            logger.error(f"Error transcribing audio chunk: {e}")
            raise

    def transcribe_audio_file(self, file_path: str, language: str = "en") -> str:
        """Handles the flow of re-encoding, splitting, transcribing, and sending for correction."""
        minimum_required_balance = 10.00
        self.check_balance(minimum_required_balance)

        # Re-encode the audio file
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            reencoded_file_path = self.reencode_audio(file_path, f"{temp_audio_file.name}_reencoded.wav")

        # Split the audio and transcribe
        audio_chunks = self.split_audio(reencoded_file_path)
        full_transcription = ""
        total_duration = 0

        for chunk_file_path in audio_chunks:
            transcription_data = self.transcribe_audio_chunk(chunk_file_path, language)
            full_transcription += transcription_data['text'] + "\n"
            total_duration += transcription_data['duration'] / 60
            os.remove(chunk_file_path)

        os.remove(reencoded_file_path)

        if full_transcription.strip():
            # Send transcription to the middleware for correction
            return self.send_to_middleware_for_correction(full_transcription, language, total_duration)
        else:
            raise ValueError("Transcription failed: no text was transcribed.")

    def send_to_middleware_for_correction(self, transcription_text: str, language: str, total_duration: float, patient_id: str) -> str:
        """Send the transcribed text to the middleware for correction."""
        try:
            response = requests.post(
                f"{MIDDLEWARE_URL}/correct_transcription",
                json={
                    "transcription_text": transcription_text,
                    "language": language,
                    "api_key": self.memu_api_key,
                    "duration_minutes": total_duration,
                    "patient_id": patient_id
                }
            )
            response.raise_for_status()
            fhir_document = response.json().get("fhir_document")
            logger.info(f"Received FHIR document from middleware.")
            return json.dumps(fhir_document, indent=4)  # Returning FHIR document in JSON format
        except Exception as e:
            logger.error(f"Error correcting transcription via middleware: {e}")
            raise

