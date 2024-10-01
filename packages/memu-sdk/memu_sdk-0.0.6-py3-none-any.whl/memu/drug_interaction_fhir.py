import requests

class DrugInteractionCheckerFHIR:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com/"  # Replace with your middleware URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def orchestrate_interaction_check_fhir(self, medication_list: list, patient_id: str, language: str = "en") -> dict:
        """Orchestrates the FHIR-compliant interaction check by calling the middleware."""
        
        url = f"{self.BASE_URL}/drug_interaction_check_fhir"
        payload = {
            "api_key": self.memu_api_key,
            "medications": medication_list,
            "patient_id": patient_id,
            "language": language
        }

        try:
            # Send a request to the middleware to perform the drug interaction check
            response = requests.post(url, json=payload)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as errh:
            raise ValueError(f"HTTP Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise ValueError(f"Request Error: {err}")
