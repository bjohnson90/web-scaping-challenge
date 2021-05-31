 # Dependencies
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
    nasa_url = "https://mars.nasa.gov/news/"
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    facts_url = "https://space-facts.com/mars/"
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    nasa_html = requests.get(nasa_url)
    hemispheres_html = requests.get(hemispheres_url)
    # Create a Beautiful Soup object
    nasa_soup = bs(nasa_html.text, 'html.parser')
    hemispheres_soup = bs(hemispheres_html.text, 'html.parser')
    #harvest html_content from nasa url
    nasa_p = nasa_soup.find_all('div', {"class": "rollover_description_inner"})[0].get_text()
    # harvest html_title from nasa url
    nasa_title = nasa_soup.find_all('div', {"class": "content_title"})[0].find('a').get_text()
    # find featured image
    browser = Browser('chrome', headless=False)
    browser.visit(jpl_url)
    browser.find_by_css("button.btn").first.click()
    img_path = browser.find_by_css("img.fancybox-image").first['src']
    # scrape table
    mars_facts_df = pd.read_html(facts_url,attrs={'id': 'tablepress-p-mars'},flavor='html5lib')
    mars_facts_table = mars_facts_df[0].to_html()
    # Scrape Hemisphere images
    hemisphere_image_urls = []
    browser.visit(hemispheres_url)
    for i in range(4):
        temp_dict = {}
        divs = browser.find_by_css("div.item")
        temp_dict['title'] = divs[i].find_by_tag("h3").first.text
        divs[i].find_by_tag("h3").first.click()
        temp_dict['img_url'] = browser.links.find_by_partial_text('Sample').first['href']
        browser.back()
        hemisphere_image_urls.append(temp_dict)
    #bundle items into single dictionary
    scraped_data = {"nasa_news": 
                    {
                        "title": nasa_title,
                        "paragraph": nasa_p
                    },
                    "jpl_mars":
                    {
                        "img": img_path
                    },
                    "mars_facts":
                    {
                        "table": mars_facts_table
                    },
                    "mars_hemispheres": hemisphere_image_urls
                }
    return scraped_data

if __name__ == "__main__":
    print(scrape())

    