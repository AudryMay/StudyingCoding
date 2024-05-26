import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import xmltojson

if __name__ == "__main__":
    
    option = webdriver.ChromeOptions()
    # I use the following options as my machine is a window subsystem linux. 
    # I recommend to use the headless option at least, out of the 3
    #option.add_argument('--headless') # using headless gives me a 403 error
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-sh-usage')
    option.add_argument('--disable-extensions')
    # Replace YOUR-PATH-TO-CHROMEDRIVER with your chromedriver location
    driver = webdriver.Chrome(options=option)
    
    driver.get('https://www.imdb.com/chart/top/') # Getting page HTML through request
    soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
    # with open("output.txt", "w", encoding="utf-8") as f: # need to output to utf-8 
    #     f.write(soup.prettify())
    #print(soup.prettify()) # print everything
    totalScrapedInfo = [] # In this list we will save all the information we scrape

    movie_containers = soup.find_all('div', class_ = 'ipc-metadata-list-summary-item__c')

    # links = soup.select("div") # Selecting all of the anchors with titles
    # print(links)
    # first10 = links[:10] # Keep only the first 10 anchors
    # for anchor in first10:
    movie_containers = movie_containers[:5] # Keep only the first 5 movies
    for container in movie_containers:
        if container.find('a', class_ = 'ipc-title-link-wrapper') is not None:
            # print(container.a)
            # <a class="ipc-title-link-wrapper" href="/title/tt1954470/?ref_=chttp_t_250" tabindex="0"><h3 class="ipc-title__text">250. Gangs of Wasseypur</h3></a>
            # print(container.a['href'])
            # /title/tt1954470/?ref_=chttp_t_250
            driver.get('https://www.imdb.com/' + container.a['href']) # Access the movie’s page
            # with open("output_page.txt", "w", encoding="utf-8") as f: # need to output to utf-8 
            #     f.write(soup.prettify())
            #     break

            ## The find elements -> need to change something to find it 
            infolist = driver.find_element(By.ID, '__NEXT_DATA__') # Find the first element with class ‘ipc-inline-list’
            print("infolist: ", infolist.get_attribute('innerHTML'))
            jsonInfoList = json.loads( infolist.get_attribute('innerHTML'))
            # informations = infolist.find_elements(By.CSS_SELECTOR, "[role='presentation']") # Find all elements with role=’presentation’ from the first element with class ‘ipc-inline-list’
            
            # Getting the data from soup parser
            soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
            url = soup.find_all('meta' ,property="og:url")[0]['content']
            scrapedInfo = {
                "title": container.a.text,
                "url": url,
                "year": jsonInfoList['props']['pageProps']['aboveTheFoldData']['releaseYear']['year'],
                "duration":jsonInfoList['props']['pageProps']['aboveTheFoldData']['runtime']['displayableProperty']['value']["plainText"],
            } # Save all the scraped information in a dictionary
            print(scrapedInfo)
            totalScrapedInfo.append(scrapedInfo) # Append the dictionary to the totalScrapedInformation list
            break

    print("Printing scraped Info:")
    print(totalScrapedInfo) # Display the list with all the information we scraped
    """
    Using requests + soup
    """
    # headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    # page = requests.get('https://www.imdb.com/chart/top/', headers=headers) # Getting page HTML through request
    # soup = BeautifulSoup(page.content, 'html.parser') # Parsing content using beautifulsoup
    # print(soup.prettify())
    # links = soup.select("table tbody tr td.titleColumn a") # Selecting all of the anchors with titles
    # first10 = links[:10] # Keep only the first 10 anchors
    # for anchor in first10:
    #     print(anchor.text) # Display the innerText of each anchor