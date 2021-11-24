#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

#parse the page to only get the text from the first title
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#parse the page to only get the text from the first title's body
news_b = slide_elem.find('div', class_='article_teaser_body').get_text()
news_b


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[ ]:





# ### Mars Facts

# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


df.to_html()


# In[ ]:





# ### Hemispheres

# In[15]:


# Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[21]:


# Create a list to hold the images and titles.
hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')

items = img_soup.find_all('div', class_='item')
print(items)


# In[55]:


hemisphere_image_urls = []

main_url = "https://marshemispheres.com/"

html = browser.html
img_soup = soup(html, 'html.parser')

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
    
    hemisphere_image_urls.append({'title': title, 'img_download': img_download})


# In[54]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:





# In[18]:


# Quit the browser
browser.quit()

