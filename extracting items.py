import csv
from bs4 import BeautifulSoup
from selenium.webdriver.edge.options import Options

from msedge.selenium_tools import Edge, EdgeOptions

def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
    search_term = search_term.replace(' ', '+')
    
    
    url = template.format(search_term)
    url += '&page={}'
    return url

    

def extractitems(item,page):
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver2 = Edge(options=options)
    atag = item.h2.a
    name = atag.text
    company = ' '
    atag2 = item.div.img
    minim = 'N/A'
    maxim = 'N/A'
    pic = atag2.get('src')    

    URL = 'https://www.amazon.com' + atag.get('href')
    try:
        ranging = item.find('span', {'data-action':'s-show-all-offers-display'})
        pricerangeparent = ranging.a
        pricerange = 'https://www.amazon.com' + pricerangeparent.get('href')
    except AttributeError:
        pricerange = 'None'
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text    
        pricewhole1 = price_parent.find('span','a-price-whole').text
        pricefraction1 = price_parent.find('span','a-price-fraction').text
        tot = pricewhole1 + pricefraction1
    except AttributeError:
        price = 'N/A'
    try:
        #driver.get(url)
        orders = item.find('span',{'class': 'a-size-base'}).text
    except AttributeError:
        orders = ' '
        
        
        
        
        
        

    if pricerange != 'None':
        url = pricerange
        driver2.get(url)
        soup2 = BeautifulSoup(driver2.page_source,'html.parser')
        results2 = soup2.find_all('div', {'id': 'aod-offer'})
  
            
        len(results2)
        #pric = results2[2].find('div', {'id': 'aod-offer-price'})
        #prices = pric.find('div', {'id': 'aod-price-3'})
        #price_parent = prices.find('span','a-price')
        #pricefinal = price_parent.find('span','a-offscreen').text
        priceslist = []

        for i in range(1,len(results2)+1):
            
                template = 'aod-price-Q'
                template = template.replace('Q', str(i))
                pric = results2[i-1].find('div', {'id': 'aod-offer-price'})
                prices = pric.find('div', {'id': template})
                price_parent = prices.find('span','a-price')
                pricefinal = price_parent.find('span','a-offscreen').text
                pricewhole = price_parent.find('span','a-price-whole').text
                pricefraction = price_parent.find('span','a-price-fraction').text
                pricewhole = pricewhole  + pricefraction
                priceslist.append(pricewhole)
                
                
            
    
        priceslist.append(tot)
        if len(priceslist) > 0:            
            priceslist.sort()
            minim = priceslist[0]
            maxim = priceslist[-1]
        else:
            minim = tot
            maxim = tot       

    
    
    result = [name,price,orders,URL,pic,minim,maxim]
    return result
def main(search_term):
    ct=0
    options = EdgeOptions()
    options.use_chromium = True
    driver = Edge(options=options)
    items = []
    records = []
    url = get_url(search_term)
    for page in range (1,2):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for item in results:
            ct+= 1
            record = extractitems(item,page)
            if record:
                records.append(record)
                #print(record[1])
                #print(ct)
                #print('-----')
                result = main2(record[3],record[4],record[5],record[6])
                print("Minimum = ", result[8])
                print("Maximum = ", result[9])
                items.append(result)
                #print(record[3])
                #print('-----')
    driver.close()
    
    with open('results.csv' , 'w' , newline = '',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title','Price','Ratings','Reviews','Availability','URL','Picture','Brand','Minimum Price','Maximum Price'])
        writer.writerows(items)

