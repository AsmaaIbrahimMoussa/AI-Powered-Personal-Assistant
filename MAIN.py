
from LLM_FireBase import handle_user_question,store_interaction, query_llama3
from PlayYouTube import play_song
from PlayYouTube import play_song
from Wikipedia import search_wikipedia 
from GenerateImage import Generate_Image
from youtubesummary import get_transcript
from shopping import response
from LastNews import get_news
from GooGle import SearchGoogle
from WeatherUpdats import get_weather
from DOCsummary import summarize_pdf_file
from Image_recognition import analyze_image
user_id= 'userloly'

while True:
    #text= take_command().lower()
    user_input = input("Enter your question : ")
    if 'do you remember' in user_input:
        questions = [user_input] 
        for question in questions:
            response = handle_user_question(user_id, question)
            print(f"Q: {question}\nA: {response}\n")  
            
            
    elif 'play' in user_input :
        play_song(user_input)
        store_interaction(user_id,user_input,None)   


    elif 'wikipedia' in user_input: 
        topic = input("sure, what is the topic: ")
        search_result = search_wikipedia(topic)
        print(search_result)
        store_interaction(user_id,user_input,None)    
            
    elif 'generate image' in user_input:
        Generate_Image(user_input)    
        store_interaction(user_id,user_input,None)

    elif 'summarize' in user_input and 'video' in user_input:
        video_url = input("sure, but enter the video URL: ")
        transcript = get_transcript(video_url)
        response = query_llama3(transcript+"* expalin this script in short. *")
        print(response)
        store_interaction(user_id,user_input,response)
    
    elif 'product' in user_input:
        response(user_input)
        store_interaction(user_id,user_input,None)
        
    elif 'news' in user_input:
        topic = input("Enter the topic: ")
        news_texts = get_news(topic)
        for text in news_texts:
            print (text) 
            store_interaction(user_id,text,text)                        
    
    elif 'google' in user_input:
        Query = user_input.replace("google", "").strip()
        search_result= SearchGoogle(Query) 
        store_interaction(user_id,text,search_result)  
    
    elif 'weather' in user_input:
        results = get_weather()
        print (results)

    elif 'summarize' in user_input and 'document' in user_input:
        file= 'ch1.pdf'
        summary = summarize_pdf_file(file)
        print(summary)
        store_interaction(user_id,text,summary)
         
    elif 'expalin image' in user_input:
        image_path = r"C:\Users\Asmaa\Downloads\large-language-model-7563532-final-9e350e9fa02d4685887aa061af7a2de2.png"
        description, extracted_text = analyze_image(image_path)
        out=query_llama3(f"describe the image which contains '{description, extracted_text}'")
        print (out)
                                       
    else: 
        questions = [user_input] 
        for question in questions:
            response = handle_user_question(user_id, question)
            print(f"Q: {question}\nA: {response}\n")

if __name__ == "__main__":
    main()