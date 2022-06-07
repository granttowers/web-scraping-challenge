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


    # Step 1b - JPL Mars Space Images - Featured Image
    # Visit the url for the Featured Space Image page [here](https://spaceimages-mars.com).
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    time.sleep(2)

    # Click the button to view full image
    fullimageclick = browser.find_by_tag("button")[1].click()

    soup = BeautifulSoup(browser.html, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
    featureimage = soup.find('img', class_="fancybox-image").get("src")

    # Make sure to find the image url to the full size `.jpg` image.
    featured_image_url = "https://spaceimages-mars.com/" + featureimage


    # Step 1c - Mars Facts
    # Visit the Mars Facts webpage [here](https://galaxyfacts-mars.com) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    url3 = "https://galaxyfacts-mars.com"
    table = pd.read_html(url3)

    # Find and import the new table from webpage
    mars_df = table[0]
    mars_df

    # Cleanup column names
    cols = list(mars_df.columns)
    cols[0] = "Descriptor"
    cols[1] = "Mars"
    cols[2] = "Earth"

    # Update the Dataframe and move item column to index
    mars_df.columns = cols
    mars_df = mars_df.iloc[1:]
    mars_df.set_index('Descriptor', inplace=True)

    # Convert table to HTML and remove additional lines appear in the HTML
    html_table = mars_df.to_html(classes="table table-striped")
    #html_table = html_table.replace('\n', '')


    # Step 1d - Mars Hemispheres
    # Visit the url for the Featured Space Image page [here](https://spaceimages-mars.com).
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)
    time.sleep(2)

    # Create a master  list to store the overall data 
    hemisphere_image_urls = []

    # Add a new variable for the number of products there are
    hemisphere_count = browser.find_by_css("a.product-item img")

    # Create a loop which occurs the number of times of "hemisphere_count" occurs 
    for count in range(len(hemisphere_count)):
        hemisphere = {}

        # Search for the image, then click the image to get the link to the "Sample" image
        browser.find_by_css("a.product-item img")[count].click()

        # Add dictionary labels to the two variables
        title_dict = browser.find_by_css("h2.title").text
        image_dict = browser.find_by_text("Sample").first

        # Join the two lists together then append to Hemisphere list
        hemisphere["title"] = title_dict
        hemisphere["img_url"] = image_dict["href"]
        hemisphere_image_urls.append(hemisphere)

        # Send the brower back, to repeat the process
        browser.back()


    #Adding all objects into single dictionary
    NASA_Mars_News = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Return Results 
    return NASA_Mars_News

    # Close the browser after scraping
    browser.quit()



