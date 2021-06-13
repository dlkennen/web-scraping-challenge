#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():

    #Setting up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Mars url to be scraped
    url = 'https://redplanetscience.com'
    browser.visit(url)

    html = browser.html
    mars_soup = bs(html, "html.parser")


# In[5]:


#Storing article title and description
    news_title = mars_soup.find('div', class_='content_title').text
    news_p = mars_soup.find('div', class_='article_teaser_body').text
    
    #Quit browser
    browser.quit()


# In[6]:


    #Printing stored title and description
    print(news_title)
    print(news_p)


# In[7]:


    #Setting up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Storing url for featured image site
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    image_soup = bs(html, "html.parser")

    #Scraping all images
    images = image_soup.findAll('img')


# In[8]:


    #Storing the second available image
    featured_image = images[1]

    #Creating a dictionary based upon the image attributes
    image_attr_dict = featured_image.attrs

    #Creating a url for the featured image
    featured_image_url = image_url + image_attr_dict['src']
    print(featured_image_url)

    #Quit browser
    browser.quit()

# In[9]:


    #Scraping Mars Facts Table
    table_url = 'https://galaxyfacts-mars.com/'
    mars_tables = pd.read_html(table_url)

    #Storing second table as a dataframe
    mars_info_df = mars_tables[1]
    mars_info_df


# In[10]:


    #Converting dataframe to an HTML table string
    mars_info_html_table = mars_info_df.to_html()
    mars_info_html_table


# In[11]:


    #Stripping newlines
    mars_info_html_table = mars_info_html_table.replace('\n', '')
    mars_info_html_table

    #Quit browser
    browser.quit()

# In[12]:


    #Setting up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Storing url for featured image site
    mars_hemi_url = 'https://marshemispheres.com/'
    browser.visit(mars_hemi_url)

    html = browser.html
    hemi_soup = bs(html, "html.parser")

    #Scraping all hemisphere pages
    hemi_pages = []
    for url in hemi_soup.findAll('a'):
        if url.get('href') != "#":
            if url.get('href') not in hemi_pages:
                if url.get('href') != 'https://astrogeology.usgs.gov/search':
                    hemi_pages.append(url.get('href'))
    hemi_pages

#Scraping the full image from each hemisphere

    #Setting up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Creating empty list
    hemisphere_image_urls=[]

    #For loop to visit each hemisphere page and scraping the full image url
    for url in hemi_pages:
        search_url = mars_hemi_url + url
    
        browser.visit(search_url)
        html = browser.html
        search_soup = bs(html, "html.parser")
        full_image = search_soup.find('img', class_="wide-image")
    
    #Creating a dictionary based upon the image attributes
        image_attr_dict = full_image.attrs
        image_url = mars_hemi_url + image_attr_dict['src']
    
        hemi_title = search_soup.find('h2', class_="title").get_text()
        title = hemi_title.replace('Enhanced', '')
    
        hemi_dict = {"title" : title, "img_url": image_url}
        hemisphere_image_urls.append(hemi_dict)  

    #Completed list of hemisphere dictionaries
    hemisphere_image_urls

    #Compiling composite dictionary
    final_dict =  {"news_title" : news_title,
                    "news_para" :news_p,
                    "featured_image" :featured_image_url,
                    "mars_table" : mars_info_html_table,
                    "hemi_images" : hemisphere_image_urls}
    
    #Quit browser
    browser.quit()
    
    return final_dict
                             
    






