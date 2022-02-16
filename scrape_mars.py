from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 

def scrape_info():
    
    mars={}
   # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
  
    soup = bs(response.text, 'html.parser')
    
    print(soup.prettify())
    
    results = soup.find_all('div', class_="content_title")
    results
    
    news_titles = []
    # Loop over div elements
    for result in results:
        if (result.a):
            if (result.a.text):
            # Append
                news_titles.append(result)
    news_titles
    
    clean_news_titles = []
    for x in range(6):
        var=news_titles[x].text
        newvar = var.strip('\n\n')
        clean_news_titles.append(newvar)
    clean_news_titles
    
    news_p = soup.find_all('div', class_="rollover_description_inner")
    news_p  
    
    clean_news_p = []
    for x in range(6):
        var=news_p[x].text
        newvar = var.strip('\n\n')
        clean_news_p.append(newvar)
    clean_news_p
    
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    
    featured_image_element = browser.find_by_css('a.showimg.fancybox-thumbs').first
    featured_image_url = featured_image_element['href']
    
    facts_url = 'https://galaxyfacts-mars.com/'
    response = requests.get(facts_url)
    soup = bs(response.text, 'html.parser')
    
    facts_tables = pd.read_html(facts_url)
    facts_tables[0]
    
    mars_facts_df = facts_tables[0]

    mars_facts_df.columns = ['COMPARISONS', 'MARS', 'EARTH']
    mars_facts_df
    
    clean = pd.Series(mars_facts_df['COMPARISONS'])
    mars_facts_df['COMPARISONS'] = clean.str.strip(':')
    mars_facts_df
    
    mars_facts_df = mars_facts_df.set_index('COMPARISONS')
    mars_facts_df
    
    mars_html_table = mars_facts_df.to_html()
    mars_html_table
    
    mars_facts_df.to_html('mars_facts_table.html')
    
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    
    hemisphere_image_urls = []

    for i in range(4):
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.links.find_by_text('Sample').first
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
        
    hemisphere_image_urls
    
    browser.quit()
    
    return(mars)

if __name__ == "__main__":
    print(scrape_info()) 
    