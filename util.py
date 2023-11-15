import openai
import os
from dotenv import load_dotenv
import re
import docx2txt
from pdfminer.high_level import extract_text

load_dotenv()
client = openai
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
    cleaned_text = clean_text(text)
    return cleaned_text

def transform_docx(docx_path):
    # Extract text from DOCX file
    text = docx2txt.process(docx_path)
    if text:
        # Clean the extracted text
        cleaned_text = clean_text(text)
        return cleaned_text
    return None

def style(model, text, job_description):
    seed =123455555
    styled_resume = client.chat.completions.create(
    model=model,
    seed = seed,
    messages=[
        {"role":"user", "content":"You are an expert Recruiter that specializes in improving resume writing. Your task is to re-write a resume provided by the user using the information from the original resume without inventing any skill sets or experience."},
        {"role":"user", "content":"The new resume should follow the specified format:"},
        {"role":"user", "content":"1. Start with the name of the candidate, underneath the candidate's name write the city and state . If the city and state are not in the raw resume, write 'Pending location' in bold."},
        {"role":"user", "content":"2. Include a comprehensive summary of the candidate's profile, highlighting how well the candidate aligns with the job description. this summary is around 100 words long and it is comprehensive"},
        {"role":"user", "content":"3. Create a bulletized list of skills, labeled 'Skills' in bold. this list shopuld not be limited to the skills listed in the resume, but should be obtained from the entire experience, keywords mentioned in the resume that could be valuable to compare against the Job Description."},
        {"role":"user", "content":"4. Include the education section, labeled 'Education' in bold, then underneath it, write the education history in bulletized form. Make sure to bold the school name and degree."},
        {"role":"user", "content":"5. Add the work experience section, labeled 'Experience' in bold. then underneath it, list the experience the candidate has, starting with the company in bold, the dates in bold and followed by the Job Title underneath it, and a comprehensive narrative of the experience, each bullet point in the experience should comprehensively explain the experience, the details are important!!!,- do not invent experience. !!!Attention: Don't remove experience or keywords from this section!!!"},
        {"role":"user", "content":"6. Complete all sections based on the raw resume without asking the user to write or complete any section."},
        {"role":"user", "content":"7. Towards the end of the resume, add a section for training and certifications (in bold) if available. Include any computer skills (in bold) or published work (in bold) if available."},
        {"role":"user", "content":"Please note that you -should remove any comments from your response and only provide the new formatted resume. Also, make sure to remove email, address, and phone numbers from the new version."},
        {"role":"user", "content":"Here is the raw resume:" + str(text)},
        {"role":"system", "content":"Sure, I can help with that, please provide the Job Description"},
        {"role":"user", "content":str(job_description)},
    ],
    temperature=0, #The temperature parameter controls the randomness of the generated output.
    )
    # Extract the summary text from the response
    styledR = styled_resume.choices[0].message.content
    return styledR