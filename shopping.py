from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_jumia(product_name):
    search_url = f"https://www.jumia.com.eg/catalog/?q={product_name.replace(' ', '+')}"
    
    options = Options()
    options.headless = True  
    options.add_argument('--log-level=3')  # Suppresses most of the console output

    service = Service(ChromeDriverManager().install())
    service.log_path = "NUL"  # On Windows, use "NUL" to suppress the log file creation
    service.service_args = ['--log-path=NUL']


    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(search_url)
    time.sleep(5)  # Wait for the page to load

    items = driver.find_elements(By.CSS_SELECTOR, 'article.prd._fb.col.c-prd')

    if not items:
        driver.quit()
        return {'products': None, 'search_page': search_url}

    product_list = []

    for item in items[:5]:  
        try:
            price_tag = item.find_element(By.CSS_SELECTOR, 'div.prc')
            name_tag = item.find_element(By.CSS_SELECTOR, 'a.core')
            
            if name_tag and price_tag:
                price_text = price_tag.text.strip().replace(',', '').replace('EGP', '').strip()
                try:
                    price = float(price_text)
                    href = name_tag.get_attribute('href')
                    if not href.startswith('https://www.jumia.com.eg'):
                        link = 'https://www.jumia.com.eg' + href
                    else:
                        link = href
                    
                    product_list.append({
                        'price': f"EGP {price:.2f}",
                        'link': link
                    })
                except ValueError:
                    continue
        except Exception as e:
            print(f"Error processing item: {e}")

    driver.quit()
    
    return {
        'products': product_list if product_list else None,
        'search_page': search_url
    }
    
def response():
    product_name = input("Enter product name: ")
    results = search_jumia(product_name)
    if results['products']:
        for i, product in enumerate(results['products']):
            print (f"{i+1}: Price: {product['price']}")
            print(f" Link: {product['link']}")
        print(f"Search Page: {results['search_page']}")
    else:
        print("No results found.")
        print(f"Search Page: {results['search_page']}")

