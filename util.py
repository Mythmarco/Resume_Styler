import openai
import os
from dotenv import load_dotenv
import re
import docx2txt
from pdfminer.high_level import extract_text

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def clean_text(txt):
    # Remove symbols and punctuations
    txt = re.sub(r'[^\w\s@.\']', ' ', txt)
    # Remove extra spaces and line breaks
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

def transform_pdf(file_path):
    # Extract text from PDF file
    text = extract_text(file_path)
    # Clean the extracted text
    return clean_text(text)

def transform_docx(docx_path):
    # Extract text from DOCX file
    text = docx2txt.process(docx_path)
    if text:
        # Clean the extracted text
        return clean_text(text)
    return None

def style(model, text, job_description):

    styled_resume = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role":"system", "content":"Hello, Im a resume Styler app, that uses AI to transform your resume how can I help?"},
        {"role":"user", "content":"I need you to help me re-write a resume using using the information from the resume, dont invent any skillsets, or experience, the new resume needs to improve the wording in the raw resume without inventing anything. The new resume should not invent anything"},
        {"role":"system", "content":"Ok, I will get to work on that, what format should I return the resume in?"},
        {"role":"user", "content":"It needs to start with the name of the candidate, and the city and state underneath the candidate's name (If city and state are not in the raw resume, write 'Pending location' in bold), followed by a summary of the candidate's profile, highlighting how well the candidate aligns with the Job description, then a bulletized list of skills ('Skills' in bold), followed by the Education ('Education' in bold), and then the work experience ('Experiecne' in bold and also each experience title in bold), complete all sections based on the raw resume, dont ask me to wirte or complete any section, towards the end of the Resume add, training and certifications (in bold) if available, and any computer skills(in bold) if available or published work(in bold) if available,"},
        {"role":"system", "content":"Sure, I can help with that, please provide the raw resume"},
        {"role":"user", "content":"Please dont add any comments to your response, I only need the new formatted Resume, remove email, address and phone numbers from the new version, here is the raw resume:" + str(text)},
        {"role":"system", "content":"Sure, I can help with that, please provide the Job Description"},
        {"role":"user", "content":str(job_description)},
    ],
    temperature=0, #The temperature parameter controls the randomness of the generated output.
    )
    # Extract the summary text from the response
    styled_resume = styled_resume['choices'][0]['message']['content']
    return styled_resume