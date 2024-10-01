import requests

class MedicalSummarizer:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com/"
    
    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def summarize_medical_info(self, transcript: str, medical_records: list, language: str = "eng") -> dict:
        """Summarize medical information by calling the middleware."""
        
        url = f"{self.BASE_URL}/summarize_medical_info"
        payload = {
            "api_key": self.memu_api_key,
            "transcript": transcript,
            "medical_records": medical_records,
            "language": language
        }

        try:
            # Send a request to the middleware to summarize the medical information
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
