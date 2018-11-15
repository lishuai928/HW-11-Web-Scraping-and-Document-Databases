from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}
    
    # Visit the NASA Mars News Site URL, Scrape the Title and Paragraph Text
    nasa_url = "https://mars.nasa.gov/news"
    browser.visit(nasa_url)
    
    time.sleep(0.3)
    
    html = browser.html
    soup_1 = BeautifulSoup(html, 'html.parser')
    
    news_title = soup_1.find("div", class_="content_title").text
    news_p = soup_1.find("div", class_="article_teaser_body").text
    
    # add the text to mars_data with a key word
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    
    # Visit the JPL Mars Space Images URL
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    
    # Scrape the browser into soup and use soup to find the image url
    html_2 = browser.html
    soup_2 = BeautifulSoup(html_2, 'html.parser')

    image_url_parts = soup_2.find("article", class_="carousel_item")["style"]
    image_url_parts = image_url_parts.split("'")[1]

    featured_image_url = "https://www.jpl.nasa.gov" + image_url_parts
    # add the image url to mars_data with a key word
    mars_data["featured"] = featured_image_url
    
    # Visit the Mars weather twitter URL
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)

    # Scrape the browser into soup and use soup to find the latest Mars weather
    html_3 = browser.html
    soup_3 = BeautifulSoup(html_3, 'html.parser')

    mars_weather = soup_3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
   
    # add the mars weather to mars_data with a key word
    mars_data["mars_weather"] = mars_weather
    
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    mars_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['Property', 'Value']
    df.set_index('Property', inplace=True)
    html_table = df.to_html().replace('\n', '')
    # add the table to mars_data with a key word
    mars_data["html_table"] = html_table
    
    # setup counter
    counter = [0, 1, 2, 3]

    # setup empty list to store data
    hemisphere_image_urls = []

    for x in counter:
        # Visit the following URL
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        
        time.sleep(0.3)

        # Design an XPATH selector to grab the img
        xpath = '//div//a[@class="itemLink product-item"]/img' 

        # Use splinter to Click the each img
        results = browser.find_by_xpath(xpath)
        results[x].click()

        # Scrape page into Soup
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Get the imgage title
        title = soup.find("h2", class_="title").text

        # Get the imgage url
        img_url_parts = soup.find("img", class_="wide-image")["src"]
        img_url = "https://astrogeology.usgs.gov" + img_url_parts

        # Store data in the list as dictionary
        hemisphere_image_urls.append ({
            "title": title,
            "img_url": img_url
        })
       
    # add the table to mars_data with a key word
    mars_data["hemisphere"] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    return mars_data


    