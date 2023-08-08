# <img src="static/rs2.png" width="100" height="100" style="vertical-align: middle;"> Resume Styler <i><span style="font-size: 0.8em;">for Recruiters</span></i>

## Overview
The BEPC Resume Styler is a Streamlit application designed to enhance the formatting of resumes. It accepts both PDF and DOCX files, and applies a unique and professional styling to the content. The application uses artificial intelligence to process and reformat the content of the resume.

## Installation

This app requires Python 3.10 or later. You will also need to install the necessary Python libraries, which are listed in the requirements.txt file. You can install these dependencies with pip:

Copy code
```pip install -r requirements.txt```
Usage
To run the app, navigate to the application's directory and execute the following command:

Copy code
```streamlit run resume_styler_app.py```

The application will then be accessible in your web browser at http://localhost:8501.

## Usage:
Enter the job description in the provided text area.
Upload the resume using the file uploader.
Click the 'Save Job Description' button to save your job description.
Click the 'Style Resume' button to transform your resume. The application will display the new styled resume.

## Features
Accepts PDF and DOCX file formats.
Uses AI to reformat and enhance the styling of resumes.
Provides a simple and intuitive user interface with a professional look.

## Note

The app will delete the uploaded audio file after it is processed to prevent storage of unnecessary files.

## Author

- [Marco Saenz]((https://github.com/Mythmarco))

## License

This project is [MIT licensed](./LICENSE).
