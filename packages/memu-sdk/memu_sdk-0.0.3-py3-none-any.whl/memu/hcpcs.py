import json
import logging
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)

class HCPCSCodeOrchestrator:
    BASE_URL = "https://memu-sdk-backend-85afb0b12f2a.herokuapp.com/"  # Replace with actual backend API URL
    CLINICAL_TABLES_URL = "https://clinicaltables.nlm.nih.gov/api/hcpcs/v3/search"  # External HCPCS codes API

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key
        self.client_name = self.validate_api_key()
        self.openai_api_key = self.get_openai_api_key()
        self.client = OpenAI(api_key=self.openai_api_key)
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def validate_api_key(self) -> str:
        """Validate MeMu API key by calling the backend."""
        response = self.make_request("GET", "/validate_api_key", params={"api_key": self.memu_api_key})
        return response.get("client_name")

    def get_openai_api_key(self):
        """Fetch the OpenAI API key from the backend."""
        try:
            response = self.make_request("GET", "/openai_api_key", params={"api_key": self.memu_api_key})
            if response and "openai_api_key" in response:
                return response["openai_api_key"]
            else:
                raise ValueError("OpenAI API key not found in the response.")
        except Exception as e:
            logger.error(f"Failed to get OpenAI API key: {e}")
            raise

    def make_request(self, method: str, endpoint: str, params=None, json=None) -> dict:
        """Generic method to handle API calls to the backend."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=json)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Error in API request to {endpoint}")

    def check_balance(self, minimum_required: float) -> bool:
        """Helper method to check if the client has enough balance."""
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        if current_balance < minimum_required:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required} is required to proceed. Current balance: ${current_balance}.")
        return True

    def deduct_client_balance(self, total_cost: float):
        """Deduct the total cost from the client's balance by calling the backend API."""
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")

        # Check if there is enough balance to cover the cost
        if current_balance < total_cost:
            logger.error(f"Insufficient balance to cover the cost. Current balance: ${current_balance}, total cost: ${total_cost}")
            raise ValueError(f"Insufficient balance to cover transcription cost. Total cost: ${total_cost}, current balance: ${current_balance}")

        # Proceed with deduction if balance is sufficient
        new_balance = current_balance - total_cost
        self.make_request("POST", "/balance/update", params={"api_key": self.memu_api_key}, json={"balance": new_balance})
        logger.info(f"Deducted ${total_cost} from {self.client_name}. New balance: ${new_balance}.")

    def fetch_hcpcs_codes(self, procedure: str) -> list:
        """Fetch HCPCS codes from the external Clinical Tables API for a given procedure."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info(f"Fetching HCPCS codes for: {procedure}")

        params = {
            'terms': procedure,
            'sf': 'code,short_desc,long_desc',
            'df': 'code,display',
            'maxList': 100
        }

        try:
            response = requests.get(self.CLINICAL_TABLES_URL, params=params)
            response.raise_for_status()
            data = response.json()

            codes = data[1]
            descriptions = data[3]
            hcpcs_codes = [{'code': code, 'description': descriptions[index][1]} for index, code in enumerate(codes)]
            logger.info(f"Fetched HCPCS codes for {procedure}: {hcpcs_codes}")
            return hcpcs_codes

        except Exception as e:
            logger.error(f"Error fetching HCPCS codes for {procedure}: {str(e)}")
            return []

    def suggest_hcpcs_code(self, procedure: str, consultation_summary: str, patient_summary: dict, language: str = "eng") -> dict:
        """Use GPT-4 to suggest the most appropriate HCPCS code based on the procedure, consultation summary, and patient context."""
        logger.info(f"Starting AI-assisted suggestion for HCPCS code for procedure: {procedure}")

        # Fetch HCPCS codes for the given procedure
        hcpcs_codes = self.fetch_hcpcs_codes(procedure)

        if not hcpcs_codes:
            logger.error(f"No HCPCS codes found for the procedure: {procedure}")
            return {"error": f"No HCPCS codes found for the procedure: {procedure}"}

        # Prepare context with procedure, consultation summary, and patient summary
        context = {
            "procedure": procedure,
            "consultation_summary": consultation_summary,
            "patient_summary": patient_summary,
            "fetched_codes": hcpcs_codes,
            "language": language
        }

        # Define the expected output template
        output_template = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "Intens cardiac rehab w/exerc"
                },
                {
                "code": "G0423",
                "description": "Intens cardiac rehab no exer"
                },
                {
                "code": "C8930",
                "description": "Tte w or w/o contr, cont ecg"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte w or w/o contr, cont ecg",
                "reason": "The procedure involves ECG monitoring, and the code C8930 specifically includes continuous ECG monitoring, which aligns with the procedure described."
            }
        }
    
        # Examples in various languages

        English = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "Intens cardiac rehab w/exerc"
                },
                {
                "code": "G0423",
                "description": "Intens cardiac rehab no exer"
                },
                {
                "code": "C8930",
                "description": "Tte w or w/o contr, cont ecg"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte w or w/o contr, cont ecg",
                "reason": "The procedure involves ECG monitoring, and the code C8930 specifically includes continuous ECG monitoring, which aligns with the procedure described."
            }
        }

        Chinese = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "强化心脏康复伴运动"
                },
                {
                "code": "G0423",
                "description": "强化心脏康复无运动"
                },
                {
                "code": "C8930",
                "description": "超声心动图（有或无对比剂），连续心电图监测"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "超声心动图（有或无对比剂），连续心电图监测",
                "reason": "该手术涉及心电图监测，代码C8930特别包括连续心电图监测，符合描述的手术内容。"
            }
        }

        Uzbek = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "Qalb terishni kuchaytirish bilan intensiv terishma"
                },
                {
                "code": "G0423",
                "description": "Qalb terishmasiz intensiv terishma"
                },
                {
                "code": "C8930",
                "description": "Tte bilan yoki bo'sh contr, davom etuvchi ecg"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte bilan yoki bo'sh contr, davom etuvchi ecg",
                "reason": "Operatsiya ECG monitoringni o'z ichiga olganligi uchun, C8930 kodi xususiyat bilan davomiy ECG monitoringni o'z ichiga oladi, bu operatsiyani tasvirlangan bilan mos keladi."
            }
        }

        Spanish = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "Rehabilitación cardíaca intensiva con ejercicio"
                },
                {
                "code": "G0423",
                "description": "Rehabilitación cardíaca intensiva sin ejercicio"
                },
                {
                "code": "C8930",
                "description": "Tte con o sin contr, ecg continuo"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte con o sin contr, ecg continuo",
                "reason": "El procedimiento implica la monitorización del ECG, y el código C8930 incluye específicamente la monitorización continua del ECG, que se alinea con el procedimiento descrito."
            }
        }

        Italian = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "Riabilitazione cardiaca intensiva con esercizio"
                },
                {
                "code": "G0423",
                "description": "Riabilitazione cardiaca intensiva senza esercizio"
                },
                {
                "code": "C8930",
                "description": "Tte con o senza contr, ecg continuo"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte con o senza contr, ecg continuo",
                "reason": "La procedura coinvolge il monitoraggio ECG, e il codice C8930 include specificamente il monitoraggio ECG continuo, che si allinea alla procedura descritta."
            }
        }

        Russian = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "Интенсивная кардиореабилитация с упражнениями"
                },
                {
                "code": "G0423",
                "description": "Интенсивная кардиореабилитация без упражнений"
                },
                {
                "code": "C8930",
                "description": "Тте с или без контраста, непрерывное ЭКГ"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Тте с или без контраста, непрерывное ЭКГ",
                "reason": "Процедура включает мониторинг ЭКГ, а код C8930 специально включает непрерывный мониторинг ЭКГ, что соответствует описанной процедуре."
            }
        }

        Thai = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "การฟื้นฟูหัวใจอย่างหนักพร้อมการออกกำลังกาย"
                },
                {
                "code": "G0423",
                "description": "การฟื้นฟูหัวใจอย่างหนักโดยไม่มีการออกกำลังกาย"
                },
                {
                "code": "C8930",
                "description": "Tte พร้อมหรือไม่พร้อม contr, ecg ต่อเนื่อง"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte พร้อมหรือไม่พร้อม contr, ecg ต่อเนื่อง",
                "reason": "ขั้นตอนนี้เกี่ยวข้องกับการตรวจสอบ ECG และรหัส C8930 รวมถึงการตรวจสอบ ECG ต่อเนื่องโดยเฉพาะที่สอดคล้องกับขั้นตอนที่อธิบาย"
            }
        }

        Arabic = {
            "fetched_codes": [
                {
                "code": "G0422",
                "description": "إعادة تأهيل القلب المكثفة مع التمارين"
                },
                {
                "code": "G0423",
                "description": "إعادة تأهيل القلب المكثفة بدون تمارين"
                },
                {
                "code": "C8930",
                "description": "Tte مع أو بدون contr، ecg مستمر"
                }
            ],
            "suggested_code": {
                "code": "C8930",
                "description": "Tte مع أو بدون contr، ecg مستمر",
                "reason": "الإجراء يشمل مراقبة ECG، والرمز C8930 يتضمن بشكل خاص مراقبة ECG المستمرة، والتي تتماشى مع الإجراء الموصوف."
            }
        }
        
        # Check if the client has enough balance to proceed
        self.check_balance(10.00)

        try:
            # Call OpenAI to suggest the most appropriate HCPCS code
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert in medical coding. Based on the provided procedure, consultation summary, "
                            "and patient summary, suggest the most appropriate HCPCS code from the fetched list. "
                            "Return your answer in the following JSON format:\n"
                            f"{json.dumps(output_template, indent=2)}"
                            "Make sure the output is on the right lanuage based on the input language."
                            f"Here are the examples for various languages: English: {json.dumps(English, indent=2)}, Chinese: {json.dumps(Chinese, indent=2)}, Uzbek: {json.dumps(Uzbek, indent=2)}, Spanish: {json.dumps(Spanish, indent=2)}, Italian: {json.dumps(Italian, indent=2)}, Russian: {json.dumps(Russian, indent=2)}, Thai: {json.dumps(Thai, indent=2)}, Arabic: {json.dumps(Arabic, indent=2)}"
                        )
                    },
                    {
                        "role": "user",
                        "content": json.dumps(context)
                    }
                ],
                temperature=0,
                response_format={"type": "json_object"}  # Ensure the response is JSON
            )

            suggested_code = json.loads(response.choices[0].message.content)
            logger.info(f"Suggested HCPCS Code: {json.dumps(suggested_code, indent=2)}")

            # Log token usage
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens
            self.log_usage(self.total_input_tokens, self.total_output_tokens)

            return {
                "fetched_codes": hcpcs_codes,
                "suggested_code": suggested_code
            }

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}

        except Exception as e:
            error_message = f"An error occurred during the HCPCS code suggestion process: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}

    def log_usage(self, total_input_tokens, total_output_tokens):
        """Log the usage of tokens for billing purposes."""
        log_payload = {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "duration_minutes": 0  # Since interaction checks don't involve audio
        }

        logger.info(f"Logging interaction usage with payload: {log_payload}")

        try:
            self.make_request("POST", "/log_transcription_usage", params={"api_key": self.memu_api_key}, json=log_payload)
            logger.info("Successfully logged usage for drug interaction checking.")
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
        
        total_cost = self.make_request("POST", "/calculate_cost", json={
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "duration_minutes": 0
            }).get("total_cost")

            # Step 6: Deduct the cost from the client's balance
        self.deduct_client_balance(total_cost)
        logger.info(f"Deducted cost: ${total_cost}.")
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance after operation: ${current_balance}")
