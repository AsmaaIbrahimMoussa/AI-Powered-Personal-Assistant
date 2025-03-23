from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract

# Define the path to your Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load BLIP model and processor
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

def describe_image(image_path):
    image = Image.open(image_path).convert("RGBA")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50)  
    caption = processor.decode(out[0], skip_special_tokens=True)
    
    return caption

def extract_text_from_image(image_path):
    image = Image.open(image_path).convert("RGBA")  
    text = pytesseract.image_to_string(image)
    return text

# Function to combine image captioning with text extraction
def analyze_image(image_path):
    # Generate image description using BLIP
    description = describe_image(image_path)
    
    # Extract text from the image using Tesseract OCR
    extracted_text = extract_text_from_image(image_path)
    
    return description, extracted_text

analyze_image(r"C:\Users\Asmaa\Downloads\large-language-model-7563532-final-9e350e9fa02d4685887aa061af7a2de2.png")
