import streamlit as st
import util
import os
from werkzeug.utils import secure_filename
import requests

st.set_page_config(page_title="BEPC-Resume_Styler", page_icon="static/logo.png", layout='wide')
import base64
# Function to read binary data and convert to base64
def get_image_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Convert your images to base64
sr2new = get_image_base64('static/rs2.png')

# Include the base64 images in your HTML
st.markdown(
    f"""
    <div class="container">
        <h2 class="text-center mt-4">
            <img src="data:image/png;base64,{sr2new}" width="75" height="75" class="d-inline-block align-top" alt="">
            Resume Styler <span style="font-style: italic; font-size: 17px;">for recruiting V1.1</span>
        </h2>
    </div>
    """,
    unsafe_allow_html=True,
)

resumes = os.path.join(os.getcwd(), 'resumes')

job_id = st.text_input('1.- Enter the Job ID')
#job_description = st.text_area('1.- Enter the Job Description', height=200)

uploaded_file = st.file_uploader('2.- Choose a Resume file')
if uploaded_file is not None:
    # Use the secure_filename function to make sure the filename is safe
    filename = secure_filename(uploaded_file.name)
    resume_file_path = os.path.join(resumes, filename) 

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(resume_file_path), exist_ok=True)

    # Save the uploaded file
    with open(resume_file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    st.success('Resume uploaded successfully!')

    if st.button('Style Resume'):
        with st.spinner('Styling Resume...'):
            # Transform the Resume file
            if filename.endswith('.pdf'):
                transformed_resume = util.transform_pdf(resume_file_path)
            elif filename.endswith('.docx'):
                transformed_resume = util.transform_docx(resume_file_path)
            #Send Request to the PHP API
            url = 'https://bepc.backnetwork.net/JobSiftBeta/assets/php/equalizer.php'
            data = {
                "job": job_id,
                "get_description": "1",
            }

            response = requests.post(url, data=data)
            response_text = response.text 
            # Generate a summary of the transcript
            summary = util.style("gpt-4-1106-preview", transformed_resume, response_text)

        st.markdown("**Stylized Resume**", unsafe_allow_html=True)
        st.markdown(summary, unsafe_allow_html=True)

        # Delete the Text file after transcribing and generating the summary and call score
        try:
            os.remove(resume_file_path)
        except Exception as e:
            st.write(f"Error deleting file: {e}")

        st.success("Resume processing completed! To transform another file, please refresh the page (press F5).")

st.markdown("""
<footer class="footer mt-auto py-3">
    <div class="container text-center">
        <p class="text-muted">
            Copyright © 2023 | BEPC Incorporated | All Rights Reserved |
            <a href="https://52840b2d-10d4-472e-8343-b77dcb77c887.filesusr.com/ugd/17c3bf_3ac57d22aa71435a8e092faeab264e45.pdf">Privacy Policy</a> |
            <a href="https://52840b2d-10d4-472e-8343-b77dcb77c887.filesusr.com/ugd/17c3bf_01578308cc1f4718b62978df425c17c3.pdf">Cybersecurity</a> |
            <a href="https://52840b2d-10d4-472e-8343-b77dcb77c887.filesusr.com/ugd/17c3bf_9ba7da42b5104bc5b8060b236b55276f.pdf">HIPAA</a>
            |  MSMMXXIII
        </p>
    </div>
</footer>
""", unsafe_allow_html=True)