from pypdf import PdfReader
from api import api_key
from groq import Groq, GroqError
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

client = Groq(api_key=api_key)

def extract_text_from_pdf(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(pages)
    final_texts = ""
    for text in texts:
        final_texts += text.page_content
    return final_texts 

def doc_summary(document_content):
    try:
        # Prepare the document for summarization
        messages = [
            {"role": "system", "content": "Summarize the following document."},
            {"role": "user", "content": document_content}
        ]
        # Generate the summary using the Groq client
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        summary = chat_completion.choices[0].message.content
        return summary
    except GroqError as e:
        print("Error:", e)
        return None

def summarize_pdf_file(pdf_file_path):
    document_content = extract_text_from_pdf(pdf_file_path)
    if not document_content:
        print("No document content found in the PDF file.")
        return None
    summary = doc_summary(document_content)
    return summary

