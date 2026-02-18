import json

from PyPDF2 import PdfReader
from openai import OpenAI


class SegregatorAgent:
   def __init__(self, api="sk-pfdDxy1BGJM4edj1TZxHM3thHDbiH"):
       self.api = api
       self.ai_client = OpenAI(api_key=api,
               base_url="https://api.apifree.ai/v1")
       self.extracted_text = ""
       self.classification_category_list = ["claim_forms", "cheque_or_bank_details", "identity_document", "itemized_bill", "discharge_summary", "prescription", "investigation_report", "cash_receipt", "other"]

   def extract_pdf_text(self, file_path):
        pdf_reader = PdfReader(file_path)
        pages = []

        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            pages.append({
                "page_number": i + 1,
                "text": text
            })

        return pages

   def validate_text(self, data_list):
       for data in data_list:
           if data['text'].strip() != "":
               return True
       return False

   def categories_data_using_ai(self, file_path):
       extracted_text = self.extract_pdf_text(file_path)
       if self.validate_text(extracted_text):
           prompt = self.get_prompt(extracted_text)

           response = self.ai_client.chat.completions.create(
               model="claude-sonnet-4.5",
               messages = [
                   {"role": "user",
                    "content": prompt}
               ]
           )

           # response = self.ai_client.responses.create(model="deepseek-chat", input=prompt)
           resp = response.choices[0].message.content
           jsons = resp.split("{")[1].split("}")[0]

           return json.loads("{" + jsons + "}")

   def get_prompt(self, text):
       return f"""{text} is the extracted content of a pdf.
           Identify the pages into categories of {self.classification_category_list} and give response in json format only which should be able to parse with key as category and value as page number list.
           """


