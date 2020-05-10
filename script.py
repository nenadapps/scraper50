from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep
import re

base_url = 'https://www.psgpostagestampsgalore.co.uk'

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "lxml")
    except: 
        pass
    
    return html_content

def get_details(url, category, subcategory):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        title = html.select('h1.name')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None     
    
    try:
        price = html.select('.price')[1].get_text().strip()
        price = price.replace('£', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
       
    try:
        raw_text_html = str(html.select('.description')[1])
        raw_text_html = raw_text_html.replace('</p>', ' ')
        raw_text = re.sub(r'<.*?>','',raw_text_html).strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None 
    
    stamp['currency'] = 'GBP'
    
    stamp['category'] = category
    stamp['subcategory'] = subcategory
    
    images = []                    
    try:
        image_items = html.select('.thumb img')
        for image_item in image_items:
            img_src = image_item.get('src').replace('727x0_562x0', '767x0_2560x0')
            img = base_url + img_src
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url 
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('.smallsubtitle a'):
            item_link = base_url + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

def get_subcategories(selected_category_name):
    
    items = {}

    try:
        html = get_html(base_url)
    except:
        return items
    
    try:
        for category_item in html.select('.navContainer ul > li > a'):
            category_name = category_item.get_text().strip()
            if category_name == selected_category_name:
                items_cont = category_item.find_next()
                for item in items_cont.select('a'):
                    item_text = item.get_text().strip()
                    item_link = base_url + item.get('href')
                    if item_link not in items: 
                        items[item_text] = item_link
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = [
"Great Britain",
"Europe",
"British Commonwealth",
"Rest of the World"
    ]
    
for category in categories:
    print(category)   

selection = input('Choose category: ')

subcategories = get_subcategories(selection)
for subcategory in subcategories:
    subcategory_url = subcategories[subcategory]
    page_items = get_page_items(subcategory_url)
    for page_item in page_items:
        stamp = get_details(page_item, selection, subcategory)     
       
