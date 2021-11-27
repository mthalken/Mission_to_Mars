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
        "hemisphere_images": hemisphere_images(browser),
        "last_modified": dt.datetime.now()
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

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped")


### Mars Hemisphere Images
def hemisphere_images(browser):
    #visit main url
    main_url = "https://marshemispheres.com/"
    browser.visit(main_url)

    #create lists
    hemisphere_image_urls = []

    #use soup to read 
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #use soup to go to next level
    item = img_soup.find_all('div', class_='item')
    # items = soup(html, 'html.parser')

    for x in item:
        
        hemispheres = {}
        #find title text
        title = x.find('h3').text
        
        #find link to thumb
        link = x.find('a', class_='itemLink product-item')['href']

        #create path to link
        page = main_url + link

        # visit link page
        browser.visit(page)

        #use soup to read page
        html = browser.html
        page_soup = soup(html, 'html.parser')

        #find path 
        large_image = page_soup.find_all('div', class_='downloads')

        #parse the page
        large_image = soup(html, 'html.parser')

        #find the large image
        image_download = large_image.find('img', class_='wide-image')['src']

        #create the url link
        final_image = main_url + image_download

    #     browser.back()

        # add to hemispheres
        hemispheres['final_image'] = final_image
        hemispheres['title'] = title

        #append hemisphere_image_urls
        hemisphere_image_urls.append(hemispheres)

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


