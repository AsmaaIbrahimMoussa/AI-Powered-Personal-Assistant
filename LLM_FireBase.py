from api import api_key
from groq import Groq, GroqError
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin import credentials, firestore, initialize_app
from WeatherUpdats import get_weather
from Wikipedia import search_wikipedia
from youtubesummary import get_transcript
from GenerateImage import Generate_Image
from Google_sendEmail import send_email_with_input
from shopping import search_jumia

client = Groq(api_key=api_key)

# Initialize Firebase
cred = credentials.Certificate('ai-assistant-33cbf-firebase-adminsdk-s366o-fcb1014435.json')
initialize_app(cred)
db = firestore.client()

# Function to query the Llama3 model
def query_llama3(messages):
    try:     
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        response = chat_completion.choices[0].message.content
    except GroqError as e:
        response = "Error: " + str(e)
    return response

# Function to store question and response
def store_interaction(user_id, question, response):
    user_ref = db.collection('users').document(user_id)
    interaction = {'question': question, 'response': response}
    doc = user_ref.get()
    if doc.exists:
        user_ref.update({
            'interactions': firestore.ArrayUnion([interaction])
        })
    else:
        user_ref.set({
            'interactions': [interaction]
        })

# Function to retrieve stored interactions
def get_stored_interactions(user_id):
    user_ref = db.collection('users').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        data = doc.to_dict()
        interactions = data.get('interactions', [])
        return interactions
    else:
        return []

# Function to handle user questions with context
def handle_user_question(user_id, question):

    # Retrieve stored interactions
    interactions = get_stored_interactions(user_id)
    messages = [
        {"role": "system", 
         "content": "You are a friendly human assistant, you have to remember anything the user tells you and answer all the questions"}
    ]
    # Generate the context from previous interactions
    for interaction in interactions:
        if isinstance(interaction, dict):  
            messages.append({"role": "user", "content": interaction['question']})
            messages.append({"role": "assistant", "content": interaction['response']})
    messages.append({"role": "user", "content": question})
    response = query_llama3(messages)
    store_interaction(user_id, question, response)
    return response

def store_user_input(user_id, user_input):
    # Reference to the user's document in Firestore
    user_doc_ref = db.collection('users').document(user_id)
    
    # Try to get the document
    user_doc = user_doc_ref.get()
    
    if user_doc.exists:
        # Document exists, append the new interaction to the existing interactions
        user_data = user_doc.to_dict()
        interactions = user_data.get('interactions', [])
        interactions.append(user_input)
        user_doc_ref.update({'interactions': interactions})
    else:
        # Document does not exist, create it with the new interaction
        user_doc_ref.set({'interactions': [user_input]})


def store_user_data(user_id, question, response):
    # Reference to the user's document in Firestore
    user_ref = db.collection('users').document(user_id)
    interaction = {'question': question, 'response': response}
    user_ref.set({
            'interactions': [interaction]
        })
    
def answer_question (user_id, question):
    if "what is the weather ?" in question.lower() or "weather ?" in question.lower():
        response = get_weather()
        store_interaction(user_id,question,None)   
        
    elif "wikipedia" in question.lower():
        topic = question.replace("wikipedia", "").strip() 
        response = search_wikipedia(topic)
        store_interaction(user_id,question,None)   
    
    elif "summarize video" in question.lower():
        video_url = question.replace("summarize video", "").strip()  
        transcript = get_transcript(video_url)
        response = query_llama3(transcript + " Summarize this script in short.")
        store_interaction(user_id,question,None) 
            
    elif "send email" in question.lower():
        response = send_email_with_input() 
        store_interaction(user_id,question,None) 
            
    elif "search jumia" in question.lower():
        product_name = question.replace("search jumia", "").strip()   
        response = search_jumia(product_name)  
        store_interaction(user_id,question,None) 
            
    elif "generate image" in question.lower():
        image_prompt = question.replace("generate image", "").strip()  
        image_path = Generate_Image(image_prompt)
        response = f"Image generated and saved to: {image_path}"
        store_interaction(user_id,question,None) 
        return image_path 
    
    else:
        questions = [question] 
        for question in questions:
            response = handle_user_question(user_id, question)
            print(f"Q: {question}\nA: {response}\n")
while True:    
    user_id = "asmaa211"
    user_input= input("Enter your question : ")
    answer_question(user_id, user_input)   