# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import pymongo


def scrape_info():

    # Add splinter functions
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Step 1a -  Visit Page and add wait time to ensure page loads correctly
    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)
    time.sleep(1)

    # Convert the browser HTML to a soup object
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Drill down into the html tags you want to scrape
    results = soup.find('div', class_="list_text").text

    # scrape the article header 
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text


    NASA_Mars_News = {
        "news_title": news_title,
        "news_p": news_p
    }

    # Return Results
    return NASA_Mars_News
    
# def scrape_info():
#     # Add splinter functions
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=True)

#     # Step 1b - JPL Mars Space Images - Featured Image
#     # Visit the url for the Featured Space Image page [here](https://spaceimages-mars.com).
#     url2 = 'https://spaceimages-mars.com/'
#     browser.visit(url2)
#     time.sleep(2)

#     # Click the button to view full image
#     fullimageclick = browser.find_by_tag("button")[1].click()

#     soup = BeautifulSoup(browser.html, 'html.parser')

#     # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
#     featureimage = soup.find('img', class_="fancybox-image").get("src")

#     # Make sure to find the image url to the full size `.jpg` image.
#     featured_image_url = "https://spaceimages-mars.com/" + featureimage

#     # Print result - Make sure to save a complete url string for this image.
#     print(featured_image_url)

#     # Return Results
#     return featured_image_url




    # Close the browser after scraping
    browser.quit()