        
from GoogleNews import GoogleNews
import pandas as pd
def get_news(topic):
    
    gNews = GoogleNews(period='1d')
    gNews.search(topic)

    result = gNews.result()

    data = pd.DataFrame.from_dict(result)
    data = data.drop(columns=['img'])
    data.head()

    for res in result:
        print("Title:", res["title"])
        print("Details:", res["link"]) 

 