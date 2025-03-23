
from Googlesit import create_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from api import api_key
from groq import Groq
import re

client = Groq(api_key=api_key)

CLIENT_SECRET_FILE = 'SendEmail.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def send_email(body, subject, to):
    if service:
        emailMsg = body
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = to
        mimeMessage['subject'] = subject
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        try:
            service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
            print('Email sent successfully!')
        except Exception as error:
            print(f'An error occurred while sending the email: {error}')
    else:
        print('Failed to create service instance')

def query_llama3(subject):
    messages = [
        {"role": "system", 
         "content": "Generate an email body based on the following subject. remove any [] and return only the body wuthout any text else"},
        {"role": "user", "content": f"Subject: {subject}"}
    ]

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        response = chat_completion.choices[0].message.content
        return response
    except Exception as error:
        print(f'An error occurred while querying LLAMA3: {error}')
        return ""
    
def parse_email_data(data):
    subject_match = re.search(r"subject:(.*?)(?=(to:|body:|$))", data, re.IGNORECASE)
    to_match = re.search(r"to:(.*?)(?=(subject:|body:|$))", data, re.IGNORECASE)
    body_match = re.search(r"body:(.*?)(?=(subject:|to:|$))", data, re.IGNORECASE)
    
    subject = subject_match.group(1).strip() if subject_match else None
    to = to_match.group(1).strip() if to_match else None
    body = body_match.group(1).strip() if body_match else None
    
    return subject, to, body

def send_email_with_input():
    data = input("""Send all data to your email in the following format: 
    subject:<subject> 
    to:<recipient> 
    body:<optional body (leave empty for automatic generation)>: """)

    subject, to, body = parse_email_data(data)

    if subject and to:
        if not body:  
            body = query_llama3(subject)
        send_email(body, subject, to)
        
    else:
        print("Failed to parse input data. Please ensure the input is in the correct format.")
