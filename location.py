import requests
def get_location():
    try:
        ipAdd = requests.get('https://api.ipify.org').text
        url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
        response = requests.get(url)
        data = response.json()
        city = data['city']
        return city
    except Exception as e:
        print("something went wrong", e)    
        
    