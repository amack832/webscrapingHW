from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    mars_data = {}    

    #Initialize the browsers
    browser = init_browser()

    #Scrape the nasa news page
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    #Get the article information: Both Title and Paragraph
    news_title = soup.find('div', class_="content_title")
    news_title1 = news_title.text.strip()
    mars_data["title"] = news_title1

    news_p = soup.find('div', class_="rollover_description")
    news_p1 = news_p.text.strip()
    mars_data["article"] = news_p1

    #Get the Image from the JPL website
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_img ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url_img)

    html = browser.html
    soup_img = BeautifulSoup(html, 'html.parser')

    img = soup_img.find('img', class_= 'thumb')
    img_src = img["src"]

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages' + img_src

    mars_data['JPL_image'] = featured_image_url
    
    
    #Get the latest Tweet information
    mars_w_url = "https://twitter.com/marswxreport?lang=en"
    tweets_info = requests.get(mars_w_url)
    soup_twitter = BeautifulSoup(tweets_info.text, 'html.parser')

    latest_tweet = soup_twitter.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    latest_tweet1 = latest_tweet.text.strip()
    mars_data['tweet'] = latest_tweet1

    #Scrape for the mars facts
    mars_facts_url = "https://space-facts.com/mars/"

    mars_facts_table = pd.read_html(mars_facts_url)

    mars_facts = mars_facts_table[0]
    mars_facts.columns = ["Category","Info"]

    mars_facts_html = mars_facts.to_html()

    mars_data['mars_table'] = mars_facts_html

    #Gather the Mars Hemispheres Images
    astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astro_url)
    astro_html = browser.html
    soup_astro = BeautifulSoup(astro_html, 'html.parser')

    astro_data = soup_astro.find('div', class_='collapsible results')

    astros_places = astro_data.find_all('a')
    hemi_urls = []
    hemi_images =[]

    for astro_place in astros_places:
        if astro_place.h3:
                pic_links = 'https://astrogeology.usgs.gov' + astro_place['href']
                hemi_urls.append(pic_links)
                browser.visit(pic_links)
                time.sleep(3)
                soup = BeautifulSoup(browser.html, 'html.parser')
                hemi_image = soup.find('div', class_='downloads').find('li').a['href']
                app_images = {'link':hemi_image}
                hemi_images.append(app_images)

    cerberus = hemi_images[0]['link']
    schiaparelli = hemi_images[1]['link']
    syrtismajor = hemi_images[2]['link']
    valles_marineris = hemi_images[3]['link']

    mars_data["cerberus"] = cerberus
    mars_data["schiaparelli"] = schiaparelli
    mars_data["syrtismajor"] = syrtismajor
    mars_data['valles_marineris'] = valles_marineris

    browser.quit()


    return mars_data
