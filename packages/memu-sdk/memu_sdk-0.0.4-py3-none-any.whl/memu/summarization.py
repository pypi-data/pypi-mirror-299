import json
import logging
import requests
from openai import OpenAI
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class MedicalSummarizer:
    BASE_URL = "https://memu-sdk-backend-85afb0b12f2a.herokuapp.com/"  # Replace with actual backend API URL

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

    def summarize_medical_info(self, transcript: str, medical_records: list, language : str = "eng") -> dict:
        """Generate a structured summary from the transcript and medical records."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info("MeMu is starting summarization with interaction data...")

        # Example format for summarization
        format_example = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "Hypertension",
                    "Type 2 Diabetes",
                    "Hypercholesterolemia",
                    "Asthma"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 bpm",
                    "OxygenSaturation": "Not provided",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "Lisinopril 10 mg daily",
                "Metformin 500 mg twice daily",
                "Simvastatin 20 mg nightly",
                "Ibuprofen 400 mg occasionally",
                "Albuterol Inhaler as needed",
                "Aspirin 81 mg daily",
                "Multivitamin daily"
                ],
                "TreatmentPlan": [
                "Monitor blood pressure due to potential interaction between Ibuprofen and Lisinopril",
                "Continue regular blood sugar checks due to Metformin and Simvastatin combination",
                "Use Albuterol only as needed",
                "Suggested procedures include Blood pressure measurement, Glucose monitoring, ECG monitoring"
                ],
                "Summary": "The patient, Jane Doe, is a 45-year-old female with a history of hypertension, type 2 diabetes, hypercholesterolemia, and asthma. Her vital signs are stable, and she reports no new symptoms. She is currently taking several medications to manage her conditions.",
                "Recommendations": "Continue monitoring blood pressure and blood sugar levels regularly. Be cautious with the use of Ibuprofen due to its potential interaction with Lisinopril. Use Albuterol only when necessary. Follow the suggested procedures for ongoing management of her conditions."
            }
        }

        # Example medical summary in different languages
        English = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "Hypertension",
                    "Type 2 Diabetes",
                    "Hypercholesterolemia",
                    "Asthma"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 bpm",
                    "OxygenSaturation": "Not provided",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "Lisinopril 10 mg daily",
                "Metformin 500 mg twice daily",
                "Simvastatin 20 mg nightly",
                "Ibuprofen 400 mg occasionally",
                "Albuterol Inhaler as needed",
                "Aspirin 81 mg daily",
                "Multivitamin daily"
                ],
                "TreatmentPlan": [
                "Monitor blood pressure due to potential interaction between Ibuprofen and Lisinopril",
                "Continue regular blood sugar checks due to Metformin and Simvastatin combination",
                "Use Albuterol only as needed",
                "Suggested procedures include Blood pressure measurement, Glucose monitoring, ECG monitoring"
                ],
                "Summary": "The patient, Jane Doe, is a 45-year-old female with a history of hypertension, type 2 diabetes, hypercholesterolemia, and asthma. Her vital signs are stable, and she reports no new symptoms. She is currently taking several medications to manage her conditions.",
                "Recommendations": "Continue monitoring blood pressure and blood sugar levels regularly. Be cautious with the use of Ibuprofen due to its potential interaction with Lisinopril. Use Albuterol only when necessary. Follow the suggested procedures for ongoing management of her conditions."
            }
        }
        Chinese = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "高血压",
                    "2型糖尿病",
                    "高胆固醇血症",
                    "哮喘"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 次/分钟",
                    "OxygenSaturation": "未提供",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "每日10毫克赖诺普利",
                "二甲双胍500毫克每天两次",
                "每日晚间20毫克辛伐他汀",
                "布洛芬400毫克偶尔服用",
                "需要时使用沙丁胺醇吸入器",
                "每日81毫克阿司匹林",
                "每日复合维生素"
                ],
                "TreatmentPlan": [
                "监测血压，防止布洛芬和赖诺普利之间的潜在相互作用",
                "继续定期检查血糖，因二甲双胍和辛伐他汀的联合使用",
                "仅在需要时使用沙丁胺醇",
                "建议的程序包括血压测量、血糖监测、心电图监测"
                ],
                "Summary": "患者Jane Doe，45岁女性，有高血压、2型糖尿病、高胆固醇血症和哮喘病史。生命体征稳定，未报告新症状。她目前正在服用多种药物来控制其病情。",
                "Recommendations": "继续定期监测血压和血糖水平。注意使用布洛芬，因为它可能与赖诺普利发生相互作用。仅在必要时使用沙丁胺醇。遵循建议的程序以持续管理她的病情。"
            }
        }
        Uzbek = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "Gipertenziya",
                    "2-tur diabet",
                    "Giperxolesterinemiya",
                    "Astma"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 bpm",
                    "OxygenSaturation": "Mavjud emas",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "Lisinopril 10 mg kuniga",
                "Metformin 500 mg kuniga ikki marta",
                "Simvastatin 20 mg kechasi",
                "Ibuprofen 400 mg ba'zan",
                "Zarur bo'lganda Albuterol Inhaler",
                "Aspirin 81 mg kuniga",
                "Multivitamin kuniga"
                ],
                "TreatmentPlan": [
                "Ibuprofen va Lisinopril o'rtasidagi potentsial o'zaro ta'sir tufayli qon bosimini kuzatish",
                "Metformin va Simvastatin kombinatsiyasi tufayli qon shakarini muntazam tekshirishni davom ettirish",
                "Albuterolni zarur bo'lganda foydalanish",
                "Taklif etilgan protseduralar: Qon bosimini o'lchash, glyukoza monitoringi, EKG monitoringi"
                ],
                "Summary": "Bemor Jane Doe, 45 yoshli ayol, gipertenziya, 2-tur diabet, giperxolesterinemiya va astma tarixi bilan. Uning hayotiy belgilari barqaror va u yangi alomatlarni bildirmaydi. U hozirda o'z holatini boshqarish uchun bir nechta dorilarni qabul qilmoqda.",
                "Recommendations": "Qon bosimi va qon shakarini muntazam kuzatib borishni davom ettiring. Ibuprofenni ehtiyotkorlik bilan ishlating, chunki bu Lisinopril bilan o'zaro ta'sirga kirishishi mumkin. Albuterolni faqat zarur bo'lganda foydalaning. Uning holatini boshqarish uchun taklif qilingan protseduralarga amal qiling."
            }
        }
        Spanish = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "Hipertensión",
                    "Diabetes tipo 2",
                    "Hipercolesterolemia",
                    "Asma"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 latidos/minuto",
                    "OxygenSaturation": "No proporcionado",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "Lisinopril 10 mg diario",
                "Metformina 500 mg dos veces al día",
                "Simvastatina 20 mg por la noche",
                "Ibuprofeno 400 mg ocasionalmente",
                "Inhalador de Albuterol según sea necesario",
                "Aspirina 81 mg diario",
                "Multivitamínico diario"
                ],
                "TreatmentPlan": [
                "Monitorear la presión arterial debido a la posible interacción entre el ibuprofeno y el lisinopril",
                "Continuar con los controles regulares de azúcar en sangre debido a la combinación de metformina y simvastatina",
                "Usar albuterol solo cuando sea necesario",
                "Los procedimientos sugeridos incluyen medición de la presión arterial, monitoreo de glucosa, monitoreo de ECG"
                ],
                "Summary": "La paciente Jane Doe, una mujer de 45 años, tiene antecedentes de hipertensión, diabetes tipo 2, hipercolesterolemia y asma. Sus signos vitales son estables y no reporta nuevos síntomas. Actualmente está tomando varios medicamentos para controlar sus afecciones.",
                "Recommendations": "Continúe monitoreando regularmente los niveles de presión arterial y azúcar en sangre. Sea cauteloso con el uso de ibuprofeno debido a su posible interacción con lisinopril. Use albuterol solo cuando sea necesario. Siga los procedimientos sugeridos para el manejo continuo de sus condiciones."
            }
        }
        Italian = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "Ipertensione",
                    "Diabete di tipo 2",
                    "Ipercolesterolemia",
                    "Asma"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 bpm",
                    "OxygenSaturation": "Non fornito",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "Lisinopril 10 mg al giorno",
                "Metformina 500 mg due volte al giorno",
                "Simvastatina 20 mg ogni sera",
                "Ibuprofene 400 mg occasionalmente",
                "Inalatore di Albuterolo al bisogno",
                "Aspirina 81 mg al giorno",
                "Multivitamina quotidiana"
                ],
                "TreatmentPlan": [
                "Monitorare la pressione sanguigna a causa della possibile interazione tra ibuprofene e lisinopril",
                "Continuare con i controlli regolari del livello di zucchero nel sangue a causa della combinazione di metformina e simvastatina",
                "Utilizzare l'albuterolo solo quando necessario",
                "Procedure suggerite includono la misurazione della pressione sanguigna, il monitoraggio del glucosio e il monitoraggio ECG"
                ],
                "Summary": "La paziente Jane Doe, una donna di 45 anni, ha una storia di ipertensione, diabete di tipo 2, ipercolesterolemia e asma. I suoi segni vitali sono stabili e non segnala nuovi sintomi. Attualmente assume diversi farmaci per gestire le sue condizioni.",
                "Recommendations": "Continui a monitorare regolarmente la pressione sanguigna e i livelli di zucchero nel sangue. Prestare attenzione all'uso dell'ibuprofene a causa della sua possibile interazione con il lisinopril. Usare l'albuterolo solo quando necessario. Seguire le procedure suggerite per la gestione continua delle sue condizioni."
            }
        }
        Russian = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "Гипертония",
                    "Сахарный диабет 2 типа",
                    "Гиперхолестеринемия",
                    "Астма"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 уд/мин",
                    "OxygenSaturation": "Не указано",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "Лизиноприл 10 мг в день",
                "Метформин 500 мг два раза в день",
                "Симвастатин 20 мг на ночь",
                "Ибупрофен 400 мг время от времени",
                "Альбутерол ингалятор по мере необходимости",
                "Аспирин 81 мг в день",
                "Мультивитамины ежедневно"
                ],
                "TreatmentPlan": [
                "Контролировать артериальное давление из-за возможного взаимодействия между ибупрофеном и лизиноприлом",
                "Продолжать регулярные проверки уровня сахара в крови из-за комбинации метформина и симвастатина",
                "Использовать альбутерол только при необходимости",
                "Предлагаемые процедуры включают измерение артериального давления, мониторинг глюкозы и мониторинг ЭКГ"
                ],
                "Summary": "Пациентка Джейн Доу, 45-летняя женщина, имеет историю гипертонии, диабета 2 типа, гиперхолестеринемии и астмы. Жизненные показатели стабильны, новых симптомов нет. Она принимает несколько препаратов для контроля своих заболеваний.",
                "Recommendations": "Продолжайте регулярно контролировать артериальное давление и уровень сахара в крови. Будьте осторожны при использовании ибупрофена из-за возможного взаимодействия с лизиноприлом. Используйте альбутерол только при необходимости. Следуйте предложенным процедурам для постоянного контроля состояния."
            }
        }
        Thai = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "ความดันโลหิตสูง",
                    "เบาหวานประเภท 2",
                    "คอเลสเตอรอลสูง",
                    "โรคหืด"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 ครั้ง/นาที",
                    "OxygenSaturation": "ไม่ได้ระบุ",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "ลิซิโนพริล 10 มก. ต่อวัน",
                "เมทฟอร์มิน 500 มก. วันละ 2 ครั้ง",
                "ซิมวาสทาติน 20 มก. ทุกคืน",
                "ไอบูโพรเฟน 400 มก. บางครั้ง",
                "สูดดมอัลบูเทอรอลตามความจำเป็น",
                "แอสไพริน 81 มก. ต่อวัน",
                "วิตามินรวมทุกวัน"
                ],
                "TreatmentPlan": [
                "ตรวจสอบความดันโลหิตอย่างสม่ำเสมอเนื่องจากอาจเกิดปฏิกิริยาระหว่างไอบูโพรเฟนและลิซิโนพริล",
                "ดำเนินการตรวจระดับน้ำตาลในเลือดอย่างต่อเนื่องเนื่องจากการใช้เมทฟอร์มินและซิมวาสทาตินร่วมกัน",
                "ใช้ยาสูดพ่นอัลบูเทอรอลเฉพาะเมื่อจำเป็น",
                "ขั้นตอนที่แนะนำ ได้แก่ การวัดความดันโลหิต, การตรวจระดับกลูโคส, การตรวจติดตามการทำงานของหัวใจด้วย ECG"
                ],
                "Summary": "ผู้ป่วย Jane Doe หญิงอายุ 45 ปี มีประวัติป่วยเป็นโรคความดันโลหิตสูง, เบาหวานประเภท 2, คอเลสเตอรอลสูง, และโรคหืด สัญญาณชีพของเธอคงที่และไม่มีอาการใหม่ เธอรับประทานยาหลายชนิดเพื่อควบคุมสภาวะสุขภาพของเธอ",
                "Recommendations": "ดำเนินการตรวจสอบความดันโลหิตและระดับน้ำตาลในเลือดอย่างต่อเนื่อง ระวังการใช้ไอบูโพรเฟนเนื่องจากอาจเกิดปฏิกิริยากับลิซิโนพริล ใช้ยาสูดพ่นอัลบูเทอรอลเฉพาะเมื่อจำเป็น ปฏิบัติตามขั้นตอนที่แนะนำเพื่อจัดการสภาวะสุขภาพของเธอต่อไป"
            }
        }
        Arabic = {
            "PatientSummary": {
                "MedicalStatus": {
                "ChronicConditions": [
                    "ارتفاع ضغط الدم",
                    "داء السكري من النوع 2",
                    "فرط كوليسترول الدم",
                    "الربو"
                ],
                "VitalSigns": {
                    "BloodPressure": "120/80",
                    "HeartRate": "72 نبضة في الدقيقة",
                    "OxygenSaturation": "لم تقدم",
                    "Temperature": "98.6°F"
                }
                },
                "Medications": [
                "ليسينوبريل 10 ملغ يومياً",
                "ميتفورمين 500 ملغ مرتين يومياً",
                "سيمفاستاتين 20 ملغ ليلاً",
                "إيبوبروفين 400 ملغ في بعض الأحيان",
                "مستنشقة الألبوتيرول حسب الحاجة",
                "أسبرين 81 ملغ يومياً",
                "الفيتامينات المتعددة يومياً"
                ],
                "TreatmentPlan": [
                "مراقبة ضغط الدم بسبب التفاعل المحتمل بين الإيبوبروفين وليسينوبريل",
                "استمرار فحص مستويات السكر في الدم بانتظام بسبب استخدام ميتفورمين وسيمفاستاتين معًا",
                "استخدام الألبوتيرول عند الحاجة فقط",
                "تشمل الإجراءات المقترحة قياس ضغط الدم ومراقبة الجلوكوز ومراقبة تخطيط القلب الكهربائي"
                ],
                "Summary": "المريضة جين دو، أنثى تبلغ من العمر 45 عامًا، لديها تاريخ مرضي يشمل ارتفاع ضغط الدم، داء السكري من النوع 2، فرط كوليسترول الدم، والربو. علاماتها الحيوية مستقرة ولا توجد أعراض جديدة. تتناول حاليًا عدة أدوية لإدارة حالتها.",
                "Recommendations": "استمر في مراقبة ضغط الدم ومستويات السكر في الدم بانتظام. كن حذرًا في استخدام الإيبوبروفين بسبب التفاعل المحتمل مع ليسينوبريل. استخدم الألبوتيرول عند الضرورة فقط. اتبع الإجراءات المقترحة لإدارة حالتها بشكل مستمر."
            }
        }

        # Combine transcript and medical records
        combined_input = json.dumps({
            "Transcript": transcript,
            "MedicalRecords": medical_records,
            "Language": language  
        }, indent=2)

        try:
            # Call OpenAI model
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": (f"Generate a structured json summary based on this format: {json.dumps(format_example)}."
                                "Make sure the output is on the right lanuage based on the input language."
                                f"Here are the examples for various languages: English: {json.dumps(English, indent=2)}, Chinese: {json.dumps(Chinese, indent=2)}, Uzbek: {json.dumps(Uzbek, indent=2)}, Spanish: {json.dumps(Spanish, indent=2)}, Italian: {json.dumps(Italian, indent=2)}, Russian: {json.dumps(Russian, indent=2)}, Thai: {json.dumps(Thai, indent=2)}, Arabic: {json.dumps(Arabic, indent=2)}"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Here is the medical data: {combined_input}"
                    }
                ],
                temperature=0,
                response_format={"type": "json_object"}  # Ensure the response is JSON
            )

            # Capture and clean the output from the model
            message_content = response.choices[0].message.content.strip().strip('```json').strip()
            total_input_tokens = response.usage.prompt_tokens
            total_output_tokens = response.usage.completion_tokens

            # Parse the output into JSON
            summary_json = json.loads(message_content)
            logger.info(f"Generated Summary: {json.dumps(summary_json, indent=2)}")

            # Log token usage
            self.total_input_tokens += total_input_tokens
            self.total_output_tokens += total_output_tokens
            self.log_usage(self.total_input_tokens, self.total_output_tokens)

            return summary_json

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}

        except Exception as e:
            error_message = f"An error occurred during the summarization process: {str(e)}"
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
