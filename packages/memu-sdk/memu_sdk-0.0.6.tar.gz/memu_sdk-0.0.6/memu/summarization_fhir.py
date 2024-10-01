import requests

class MedicalSummarizer:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com/"
    
    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def summarize_medical_info_fhir(self, transcript: str, medical_records: list, patient_id: str, language: str = "eng") -> dict:
        """Summarize medical information and generate a FHIR Composition resource."""
        
        url = f"{self.BASE_URL}/summarize_medical_info_fhir"
        payload = {
            "api_key": self.memu_api_key,
            "transcript": transcript,
            "medical_records": medical_records,
            "patient_id": patient_id,
            "language": language
        }

        try:
            # Send a request to the middleware to summarize the medical information and generate the FHIR Composition
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
