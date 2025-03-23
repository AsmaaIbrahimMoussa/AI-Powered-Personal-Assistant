import wikipedia
def search_wikipedia(topic): 
    try:
        result = wikipedia.summary(topic, sentences=5)
        print(result)
    except wikipedia.exceptions.DisambiguationError as e:
        print("It seems there are multiple options. Please be more specific.")
    except wikipedia.exceptions.PageError as e:
        print("Sorry, I could not find any information on that topic.")
    except Exception as e:
        print("An error occurred:", str(e))   