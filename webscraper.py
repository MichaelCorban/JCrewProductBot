import requests
from bs4 import BeautifulSoup
import pandas as pd
import xml.etree.ElementTree as ET
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time
import json
import csv

sitemap = r"https://www.jcrew.com/sitemap-wex/sitemap-index.xml"
# manually defined user agent so requests is not blocked
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

product_list = []

# get the current directory path
current_dir = os.getcwd()

# concatenate the current directory path with the name of the web driver executable
driver_path = os.path.join(current_dir, 'chromedriverundetectable.exe')
ser = Service(driver_path)
op = webdriver.ChromeOptions()

#op.add_argument("start-maximized")
op.add_argument('--disable-blink-features=AutomationControlled')
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('useAutomationExtension', False)
op.add_argument("--headless=new")
driver = webdriver.Chrome(service=ser, options=op)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                     'Chrome/85.0.4183.102 Safari/537.36'})


#op.add_experimental_option("excludeSwitches", ["enable-automation"])
#op.add_experimental_option('useAutomationExtension', False)
#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
#op.add_argument('user-agent={0}'.format(user_agent))
#op.add_argument("--headless=new")

# start the web driver
#driver = webdriver.Chrome(service=ser, options=op)

# get sitemap XML
response = requests.get(sitemap)
xml_data = response.content
# parse the XML data
root = ET.fromstring(xml_data)

# extract all xml files from the elements
text_list = []
for elem in root.iter():
    text = elem.text
    if text is not None:
        text_list.append(text.strip())

pdp_all_list = [x for x in text_list if 'pdp' in x]
pdp_us_list = pdp_all_list[0:5]

# repeat parsing process for every pdp
for xml in pdp_us_list:
    response = requests.get(xml)
    xml_data = response.content
    root = ET.fromstring(xml_data)
    for elem in root.iter():
        text = elem.text
        if text is not None and "http" in text:
            product_list.append(text.strip())

print(len(product_list))

data=[]
count = 0
for url in product_list[0::]:
    count +=1
    print("requesting", url, "number", count)
    try:
        response = requests.get(url, headers = headers, timeout = 5)
    except:
        continue
    #driver = webdriver.Chrome(service=ser, options=op)
    try:
        driver.get(url)
    except:
        time.sleep(10)
        continue
    html_data = response.text
    soup = BeautifulSoup(html_data, 'html.parser')
    #page_source = driver.page_source
    #print(page_source)
    #time.sleep(2)
    # product name
    try:
        #name = soup.find("h1", {"id": "product-name__p"}).text.replace('\n', "")
        name = soup.find("h1", {"data-qaid": "pdpProductName"}).text.replace('\n', "")
        #name = soup.find("h1", {"data-qaid": "pdpProductName"})
    except:
        name = None

    # product regular price
    try:
        priceRegular = driver.find_element("xpath", '//span[@data-qaid="pdpProductName"]').text;
        print(priceRegular)
    except:
        priceRegular = None

    # product regular price
    try:
        priceRegular = driver.find_element("xpath", '//span[@data-qaid="pdpProductPriceRegular"]').text
    except:
        priceRegular = None

    # product sale price
    try:
        priceSale = driver.find_element("xpath", '//span[@data-qaid="pdpProductPriceSale"]').text
    except:
        priceSale = None

    try:
        script_element = driver.find_element("xpath", '(//script[@type="application/ld+json"])[2]')
        script_text = script_element.get_attribute("textContent")
        match = re.search(r'"ratingValue":(\d+)', script_text)
        rating_value = match.group(1)
        ratingAvg = rating_value
    except:
        ratingAvg = None

    try:
        script_element = driver.find_element("xpath", '(//script[@type="application/ld+json"])[2]')
        script_text = script_element.get_attribute("textContent")
        parsed = json.loads(script_text)
        parsedKeywords = parsed["keywords"]
        keywords = parsedKeywords
    except:
        keywords = None

    try:
        script_element = driver.find_element("xpath", '(//script[@type="application/ld+json"])[2]')
        script_text = script_element.get_attribute("textContent")
        rating_value = re.search(r'"ratingCount":"(\d+)"', script_text).group(1)
        ratingCount = rating_value
    except:
        ratingCount = None

    try:
        script_element = driver.find_element("xpath", '(//script[@type="application/ld+json"])[2]')
        script_text = script_element.get_attribute("textContent")
        category_value = re.search(r'"category":"(\w+)"', script_text).group(1)
        category = category_value
    except:
        category = None


    # rating
    #element = driver.find_element("xpath", '//div[@class="class="BVRRNumber BVRRRatingNumber"]')
    # find the script element using XPath and retrieve its text content
    #script_element = driver.find_element("xpath", '(//script[@type="application/ld+json"])[2]')
    #script_text = script_element.get_attribute("textContent")
    #print(script_text)
    #match = re.search(r'"ratingValue":(\d+)', script_text)
    #if match:
        #rating_value = match.group(1)
        #print(rating_value)
    #else:
        #print("ratingValue not found")
    #rating = element.get_attribute('title')
    #print(rating)

    '''
    try:
        sizes = soup.find("h1", {"id": "product-name__p"}).text.replace('\n', "")
    except:
        sizes = None
    try:
        colors = soup.find("h1", {"id": "product-name__p"}).text.replace('\n', "")
    except:
        colors = None
    '''

    #rating = None
    #sizes = None
    #colors = None

    # ideally implement "sizes": sizes, "colors": colors later
    product_data = {"name": name, "priceReg": priceRegular, "priceSale": priceSale, "ratingAvg": ratingAvg, "ratingCnt": ratingCount, "category": category, "keywords": keywords}
    data.append(product_data)
    #driver.close()
    if count % 10 == 0:
        with open('data.csv', mode='w', newline='', encoding="utf-8") as file:

            # Define the fieldnames for the CSV file
            fieldnames = ['name', 'priceReg', 'priceSale', 'ratingAvg', 'ratingCnt', 'category', 'keywords']

            # Create a CSV writer object
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header row to the CSV file
            writer.writeheader()

            # Write the data to the CSV file
            for row in data:
                writer.writerow(row)

print(data)

driver.quit()