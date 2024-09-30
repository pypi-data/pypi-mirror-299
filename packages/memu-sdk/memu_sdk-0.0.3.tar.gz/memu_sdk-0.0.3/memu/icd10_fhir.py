import json
import logging
import requests
import uuid
import datetime
import pytz
from openai import OpenAI

logger = logging.getLogger(__name__)

class ICD10CodeOrchestratorFHIR:
    BASE_URL = "https://memu-sdk-backend-85afb0b12f2a.herokuapp.com/"  # Replace with actual backend API URL
    ICD10_API_URL = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"  # External ICD-10-CM API

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

    def fetch_icd10_codes(self, disease: str) -> list:
        """Fetch ICD-10 codes from the external Clinical Tables API for a given disease or diagnosis."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info(f"Fetching ICD-10 codes for: {disease}")

        params = {
            'terms': disease,
            'sf': 'code,name',
            'df': 'code,name',
            'maxList': 10
        }

        try:
            response = requests.get(self.ICD10_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            codes = data[1]
            descriptions = data[3]
            icd10_codes = [{'code': code, 'description': descriptions[index]} for index, code in enumerate(codes)]
            logger.info(f"Fetched ICD-10 codes for {disease}: {icd10_codes}")
            return icd10_codes

        except Exception as e:
            logger.error(f"Error fetching ICD-10 codes for {disease}: {str(e)}")
            return []

    def suggest_icd10_code(self, disease: str, consultation_summary: str, patient_summary: dict, language : str = "eng") -> dict:
        """Use GPT-4 to suggest the most appropriate ICD-10 code based on the disease, consultation summary, and patient context."""
        logger.info(f"Starting AI-assisted suggestion for ICD-10 code for disease: {disease}")

        # Fetch ICD-10 codes for the given disease
        icd10_codes = self.fetch_icd10_codes(disease)

        if not icd10_codes:
            logger.error(f"No ICD-10 codes found for the disease/diagnosis: {disease}")
            return {"error": f"No ICD-10 codes found for the disease/diagnosis: {disease}"}

        # Prepare context with disease, consultation summary, and patient summary
        context = {
            "disease": disease,
            "consultation_summary": consultation_summary,
            "patient_summary": patient_summary,
            "fetched_codes": icd10_codes,
            "language": language
        }

        # Define the expected output template
        output_template = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "Renovascular hypertension"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "Resistant hypertension"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "Postprocedural hypertension"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "Portal hypertension"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "Neonatal hypertension"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "Benign intracranial hypertension"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "Ocular hypertension, bilateral"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "Essential (primary) hypertension"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "Other secondary hypertension"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "Secondary hypertension, unspecified"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "Essential (primary) hypertension",
                "reason": "The patient has a history of hypertension with no indication of it being secondary, resistant, or related to any specific condition like renovascular or postprocedural hypertension. The blood pressure is stable, suggesting it is well-managed essential hypertension."
            }
        }

        # Examples in various languages
        English = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "Renovascular hypertension"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "Resistant hypertension"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "Postprocedural hypertension"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "Portal hypertension"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "Neonatal hypertension"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "Benign intracranial hypertension"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "Ocular hypertension, bilateral"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "Essential (primary) hypertension"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "Other secondary hypertension"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "Secondary hypertension, unspecified"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "Essential (primary) hypertension",
                "reason": "The patient has a history of hypertension with no indication of it being secondary, resistant, or related to any specific condition like renovascular or postprocedural hypertension. The blood pressure is stable, suggesting it is well-managed essential hypertension."
            }
        }

        Chinese = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "肾血管性高血压"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "难治性高血压"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "术后高血压"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "门静脉高压"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "新生儿高血压"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "良性颅内高压"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "双侧眼压升高"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "原发性高血压"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "其他继发性高血压"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "未特指的继发性高血压"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "原发性高血压",
                "reason": "患者有高血压病史，但没有迹象表明其为继发性、难治性或与特定情况（如肾血管性或术后高血压）相关。血压稳定，表明其为良好控制的原发性高血压。"
            }
        }

        Uzbek = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "Renovaskulyar gipertenziya"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "Qaytarilmas gipertenziya"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "Postoperatsion gipertenziya"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "Portal gipertenziya"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "Neonatal gipertenziya"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "Yaxshi xulqli bosh ichidagi gipertenziya"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "Ikki tomonlama ko‘z gipertenziyasi"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "Asosiy (birlamchi) gipertenziya"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "Boshqa ikkilamchi gipertenziya"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "Aniqlanmagan ikkilamchi gipertenziya"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "Asosiy (birlamchi) gipertenziya",
                "reason": "Bemorning gipertenziya tarixi bor, lekin bu ikkilamchi, qaytarilmas yoki renovaskulyar yoki postoperatsion gipertenziya kabi maxsus sharoit bilan bog‘liq ekanligi ko‘rsatilmagan. Qon bosimi barqaror, bu yaxshi boshqarilgan asosiy gipertenziya ekanligini ko‘rsatadi."
            }
        }

        Spanish = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "Hipertensión renovascular"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "Hipertensión resistente"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "Hipertensión postprocedimiento"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "Hipertensión portal"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "Hipertensión neonatal"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "Hipertensión intracraneal benigna"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "Hipertensión ocular bilateral"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "Hipertensión esencial (primaria)"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "Otra hipertensión secundaria"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "Hipertensión secundaria, no especificada"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "Hipertensión esencial (primaria)",
                "reason": "El paciente tiene un historial de hipertensión sin indicación de que sea secundaria, resistente o relacionada con una condición específica como hipertensión renovascular o postprocedimiento. La presión arterial es estable, lo que sugiere que se trata de hipertensión esencial bien controlada."
            }
        }

        Italian = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "Ipertensione renovascolare"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "Ipertensione resistente"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "Ipertensione postoperatoria"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "Ipertensione portale"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "Ipertensione neonatale"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "Ipertensione intracranica benigna"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "Ipertensione oculare bilaterale"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "Ipertensione essenziale (primaria)"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "Altre ipertensioni secondarie"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "Ipertensione secondaria, non specificata"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "Ipertensione essenziale (primaria)",
                "reason": "Il paziente ha una storia di ipertensione senza indicazioni che sia secondaria, resistente o correlata a una condizione specifica come ipertensione renovascolare o postoperatoria. La pressione sanguigna è stabile, suggerendo che si tratta di ipertensione essenziale ben gestita."
            }
        }

        Russian = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "Реноваскулярная гипертензия"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "Резистентная гипертензия"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "Постпроцедурная гипертензия"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "Портальная гипертензия"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "Неонатальная гипертензия"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "Доброкачественная внутричерепная гипертензия"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "Двусторонняя глазная гипертензия"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "Эссенциальная (первичная) гипертензия"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "Другая вторичная гипертензия"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "Вторичная гипертензия, неуточненная"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "Эссенциальная (первичная) гипертензия",
                "reason": "У пациента есть история гипертензии без признаков того, что она является вторичной, резистентной или связанной с конкретным состоянием, таким как реноваскулярная или постпроцедурная гипертензия. Давление стабильно, что указывает на хорошо управляемую эссенциальную гипертензию."
            }
        }

        Thai = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "ความดันโลหิตสูงจากหลอดเลือดไต"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "ความดันโลหิตสูงที่ดื้อต่อการรักษา"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "ความดันโลหิตสูงหลังจากการทำหัตถการ"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "ความดันโลหิตสูงในตับ"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "ความดันโลหิตสูงในทารกแรกเกิด"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "ความดันโลหิตสูงภายในกะโหลกศีรษะชนิดไม่ร้ายแรง"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "ความดันโลหิตสูงในตาแบบสองข้าง"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "ความดันโลหิตสูงชนิดปฐมภูมิ"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "ความดันโลหิตสูงชนิดทุติยภูมิอื่นๆ"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "ความดันโลหิตสูงชนิดทุติยภูมิไม่ระบุรายละเอียด"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "ความดันโลหิตสูงชนิดปฐมภูมิ",
                "reason": "ผู้ป่วยมีประวัติความดันโลหิตสูงโดยไม่มีการระบุว่าเป็นชนิดทุติยภูมิหรือดื้อยา หรือเกี่ยวข้องกับเงื่อนไขเฉพาะ เช่น ความดันโลหิตสูงจากหลอดเลือดไตหรือหลังการทำหัตถการ ความดันโลหิตคงที่บ่งชี้ว่าเป็นความดันโลหิตสูงชนิดปฐมภูมิที่ควบคุมได้ดี"
            }
        }

        Arabic = {
            "fetched_codes": [
                {
                "code": "I15.0",
                "description": [
                    "I15.0",
                    "ارتفاع ضغط الدم الكلوي الوعائي"
                ]
                },
                {
                "code": "I1A.0",
                "description": [
                    "I1A.0",
                    "ارتفاع ضغط الدم المقاوم للعلاج"
                ]
                },
                {
                "code": "I97.3",
                "description": [
                    "I97.3",
                    "ارتفاع ضغط الدم بعد الإجراء"
                ]
                },
                {
                "code": "K76.6",
                "description": [
                    "K76.6",
                    "ارتفاع ضغط الدم البابي"
                ]
                },
                {
                "code": "P29.2",
                "description": [
                    "P29.2",
                    "ارتفاع ضغط الدم الوليدي"
                ]
                },
                {
                "code": "G93.2",
                "description": [
                    "G93.2",
                    "ارتفاع ضغط الدم داخل الجمجمة الحميد"
                ]
                },
                {
                "code": "H40.053",
                "description": [
                    "H40.053",
                    "ارتفاع ضغط العين الثنائي"
                ]
                },
                {
                "code": "I10",
                "description": [
                    "I10",
                    "ارتفاع ضغط الدم الأساسي (الأولي)"
                ]
                },
                {
                "code": "I15.8",
                "description": [
                    "I15.8",
                    "ارتفاع ضغط الدم الثانوي الآخر"
                ]
                },
                {
                "code": "I15.9",
                "description": [
                    "I15.9",
                    "ارتفاع ضغط الدم الثانوي غير محدد"
                ]
                }
            ],
            "suggested_code": {
                "code": "I10",
                "description": "ارتفاع ضغط الدم الأساسي (الأولي)",
                "reason": "المريض لديه تاريخ من ارتفاع ضغط الدم بدون إشارة إلى كونه ثانويًا، أو مقاومًا، أو مرتبطًا بأي حالة معينة مثل ارتفاع ضغط الدم الكلوي الوعائي أو بعد الإجراء. ضغط الدم مستقر، مما يشير إلى أنه ارتفاع ضغط الدم الأساسي جيد الإدارة."
            }
        }

        # Check if the client has enough balance to proceed
        self.check_balance(10.00)
        
        try:
            # Call OpenAI to suggest the most appropriate ICD-10 code
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert in medical coding. Based on the provided disease, consultation summary, "
                            "and patient summary, suggest the most appropriate ICD-10 code from the fetched list. "
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
            logger.info(f"Suggested ICD-10 Code: {json.dumps(suggested_code, indent=2)}")

            # Log token usage
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens
            self.log_usage(self.total_input_tokens, self.total_output_tokens)

            return {
                "fetched_codes": icd10_codes,
                "suggested_code": suggested_code
            }

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}

        except Exception as e:
            error_message = f"An error occurred during the ICD-10 code suggestion process: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}

    def create_fhir_condition(self, icd10_code: dict, patient_id: str) -> dict:
        """Creates a FHIR Condition resource for the suggested ICD-10 code."""
        # Get current time in ISO 8601 format
        now = datetime.datetime.now(pytz.utc)
        timestamp = now.isoformat()

        # Ensure timezone offset includes colon (e.g., "+00:00")
        if timestamp.endswith('+0000'):
            timestamp = timestamp[:-5] + '+00:00'

        # Create the Condition resource
        condition_resource = {
            "resourceType": "Condition",
            "id": str(uuid.uuid4()),
            "code": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/sid/icd-10-cm",
                        "code": icd10_code["code"],
                        "display": icd10_code["description"]
                    }
                ],
                "text": icd10_code["description"]
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "onsetDateTime": timestamp,
            "clinicalStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        "code": "active",
                        "display": "Active"
                    }
                ]
            },
            "verificationStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                        "code": "confirmed",
                        "display": "Confirmed"
                    }
                ]
            },
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                            "code": "diagnosis",
                            "display": "Diagnosis"
                        }
                    ]
                }
            ],
            "evidence": [
                {
                    "detail": [
                        {
                            "reference": "DocumentReference/consultation-summary",
                            "display": icd10_code["reason"]
                        }
                    ]
                }
            ]
        }

        return condition_resource

    def orchestrate_icd10_fhir(self, disease: str, consultation_summary: str, patient_summary: dict, patient_id: str, language : str = "eng") -> dict:
        """Orchestrates the ICD-10 code suggestion and returns a FHIR Condition resource."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info(f"Starting FHIR-compliant ICD-10 code suggestion for disease: {disease}")

        # Suggest the most appropriate ICD-10 code
        suggestion_result = self.suggest_icd10_code(disease, consultation_summary, patient_summary, language)

        if "error" in suggestion_result:
            return suggestion_result

        suggested_code = suggestion_result["suggested_code"]

        # Create a FHIR Condition resource for the suggested ICD-10 code
        fhir_condition = self.create_fhir_condition(suggested_code, patient_id)

        logger.info(f"Completed FHIR-compliant ICD-10 code suggestion with final FHIR Condition resource.")
        return fhir_condition

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
