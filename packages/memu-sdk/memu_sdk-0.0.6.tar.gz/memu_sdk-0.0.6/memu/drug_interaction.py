import requests

class DrugInteractionChecker:
    BASE_URL = "https://memu-v1-2d38d2b70341.herokuapp.com/"  # Replace with your middleware URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key

    def orchestrate_interaction_check(self, medication_list: list, language: str = "en") -> dict:
        """Orchestrates the whole process by calling the middleware for drug interactions."""
        
        url = f"{self.BASE_URL}/drug_interaction_check"
        payload = {
            "api_key": self.memu_api_key,
            "medications": medication_list,
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
