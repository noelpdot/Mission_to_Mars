# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemispheres(browser),
      "last_modified": dt.datetime.now()
   }
    
    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object  and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Using the Try and except for error handling
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):

    # ## JPL Space Images Featured Image
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # use try and except error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url

    return img_url

# ## Mars Facts

def mars_facts():
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      # #Converting the table into a DF 
      df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of DataFrane    
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    #Convert DF into HTML format, and bootstrap
    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    print("hemispheres test")
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    links = browser.links.find_by_partial_text("Hemisphere")
    #pprint(links)
    for i in range(len(links)):
        link = browser.links.find_by_partial_text("Hemisphere")[i] 
        link.click()
        Hemispheres = {}
        sample = browser.links.find_by_text("Sample").first
        Hemispheres["img"] = sample["href"]
        print (sample["href"])
        title=browser.find_by_css("h2.title").text
        Hemispheres["title"]=title
        hemisphere_image_urls.append(Hemispheres)
        browser.back()
    print(hemisphere_image_urls)
    return hemisphere_image_urls
    
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())