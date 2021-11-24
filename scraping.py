#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#set up splinter
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_images": hemisphere_images(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data










### Mars News Site

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        #parse the page to only get the text from the first title
        news_title = slide_elem.find('div', class_='content_title').get_text()

        #parse the page to only get the text from the first title's body
        news_b = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None 

    return news_title, news_b


### Featured Images

def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


### Mars Facts

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html(classes="table table-striped")


### Mars Hemisphere Images
def hemisphere_images(browser):
    
    hemisphere_image_urls = []

    main_url = "https://marshemispheres.com/"
    try:
        html = browser.html
        img_soup = soup(html, 'html.parser')

        items = img_soup.find_all('div', class_='item')

        # Write code to retrieve the image urls and titles for each hemisphere.
        for x in items:
            results = {}
            
            #find the title
            title = x.find('h3').text
            
            #get the link to the specific image
            link = x.find('a', class_='itemLink product-item')['href']
            
            #create a link for the large image
            browser.visit(main_url + link)
            
            #go to image page
            image_html = browser.html
            soup_spec = soup(image_html, 'html.parser')
            img_download = soup_spec.find('img', class_='wide-image')['src']
            
            hemisphere_image_urls.append({'title': title, 'img_download': main_url + img_download})

        return hemisphere_image_urls

    except BaseException:
        return None


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


