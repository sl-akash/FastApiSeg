import io

from fastapi import File, UploadFile, Form

from BusinessLogic.ExtractorAgent import ExtractorAgent
from BusinessLogic.SegregatorAgent import SegregatorAgent

class ServicesHandler:
    def get_home(self):
        return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Claim Document Upload</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        font-family: Arial, Helvetica, sans-serif;
                        background: linear-gradient(135deg, #4e73df, #1cc88a);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
            
                    .container {
                        background: #ffffff;
                        padding: 40px;
                        border-radius: 12px;
                        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                        width: 350px;
                        text-align: center;
                    }
            
                    .container h1 {
                        margin-bottom: 25px;
                        color: #333;
                    }
            
                    .form-group {
                        margin-bottom: 20px;
                        text-align: left;
                    }
            
                    label {
                        font-weight: bold;
                        display: block;
                        margin-bottom: 6px;
                        color: #555;
                    }
            
                    input[type="text"],
                    input[type="file"] {
                        width: 100%;
                        padding: 10px;
                        border-radius: 6px;
                        border: 1px solid #ccc;
                        font-size: 14px;
                    }
            
                    input[type="text"]:focus,
                    input[type="file"]:focus {
                        outline: none;
                        border-color: #4e73df;
                        box-shadow: 0 0 5px rgba(78, 115, 223, 0.3);
                    }
            
                    button {
                        width: 100%;
                        padding: 12px;
                        border: none;
                        border-radius: 6px;
                        background-color: #4e73df;
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        cursor: pointer;
                        transition: 0.3s;
                    }
            
                    button:hover {
                        background-color: #2e59d9;
                    }
            
                    .subtitle {
                        font-size: 14px;
                        color: #777;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            
            <body>
                <div class="container">
                    <h1>📄 Claim Report</h1>
                    <div class="subtitle">
                        Upload your claim PDF for processing
                    </div>
            
                    <form method="post" action="/api/process" enctype="multipart/form-data">
                        
                        <div class="form-group">
                            <label for="claim_id">Claim ID</label>
                            <input type="text" name="claim_id" id="claim_id" placeholder="Enter Claim ID" required>
                        </div>
            
                        <div class="form-group">
                            <label for="file">Upload PDF Document</label>
                            <input type="file" name="file" id="file" accept="application/pdf" required>
                        </div>
            
                        <button type="submit">Upload & Process</button>
            
                    </form>
                </div>
            </body>
            </html>
            """

    async def process_pdf(self, file: UploadFile = File(...), claim_id: str = Form(...)):
        try:
            content = await file.read()
            pdf_file = io.BytesIO(content)
            segregator_agent = SegregatorAgent()
            extractor_agent = ExtractorAgent()
            extracted_text = segregator_agent.extract_pdf_text(pdf_file)
            segregation = segregator_agent.categories_data_using_ai(pdf_file)
            identity_document_page = self.filter_page(segregation, extracted_text, "identity_document")
            discharge_summary_page = self.filter_page(segregation, extracted_text, "discharge_summary")
            itemized_bill_page = self.filter_page(segregation, extracted_text, "itemized_bill")
            return {
                "claim_id": claim_id,
                "identity_agent": extractor_agent.idAgent(identity_document_page),
                "discharge_agent": extractor_agent.dischargeSummaryAgent(discharge_summary_page),
                "itemized_bill_agent": extractor_agent.itemizedBillAgent(itemized_bill_page)
            }
        except:
            return {"status", "error"}

    def filter_page(self, segregation, extracted_text, category):
        returnList = []
        for i in segregation[category]:
            returnList.append(extracted_text[i - 1]["text"])
        return returnList
