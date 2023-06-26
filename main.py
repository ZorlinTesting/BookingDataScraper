from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# listing_site = 'https://www.booking.com/searchresults.en-us.html?label=gen173nr-1FCAEoggI46AdIM1gEaLQBiAEBmAExuAEXyAEM2AEB6AEB-AECiAIBqAIDuALB_LmhBsACAdICJDQwOTM2ZWYxLTRjMTMtNDBiNi05MTE0LTU4M2M4MWY5Y2I0ONgCBeACAQ&aid=304142&ss=Siargao+Island&ssne=Siargao+Island&ssne_untouched=Siargao+Island&highlighted_hotels=7112030&lang=en-us&sb=1&src_elem=sb&dest_id=5375&dest_type=region&checkin=2023-05-25&checkout=2023-05-31&group_adults=3&no_rooms=1&group_children=0&sb_travel_purpose=leisure&order=price'
# forms_site = 'https://forms.gle/ZUDUjAL1bQQnZMHQ6'


class ListMaker:
    def __init__(self):
        self.location_dic = self.start_crawl()
        self.start_entry(self.location_dic)

    def start_crawl(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(listing_site)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        prices = soup.select(selector='.fbd1d3018c')
        names = soup.select(selector='.a23c043802')
        links = soup.select(selector='.a4225678b2 a')

        prices_list = []
        names_list = []
        links_list = []
        locations_dictionary = []

        for price in prices:
            prices_list.append(int(price.getText()[2:].replace(',', '')))

        for name in names:
            names_list.append(name.getText())

        for link in links:
            links_list.append(link.get('href'))

        for i in range(0, len(names_list)):
            inner_dic = {
                "name": names_list[i],
                "price": prices_list[i],
                "link": links_list[i]
            }
            locations_dictionary.append(inner_dic)
        print('Crawling Phase completed')
        return locations_dictionary

    def start_entry(self, locations_dictionary):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(forms_site)
        print('Encoding Phase beginning')

        for location in locations_dictionary:
            field1 = WebDriverWait(driver=driver, timeout=20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
            field1.send_keys(f"{location['name']}")

            field2 = WebDriverWait(driver=driver, timeout=20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
            field2.send_keys(f"{location['price']}")

            field3 = WebDriverWait(driver=driver, timeout=20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
            field3.send_keys(f"{location['link']}")

            submit_button = driver.find_element(by='css selector', value='.l4V7wb')
            submit_button.click()

            next_button = WebDriverWait(driver=driver, timeout=10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.c2gzEf a')))
            next_button.click()
            print(f'Entry Number: {1 + locations_dictionary.index(location)}')


print(
    "Hi! This is a terminal-based application that automates crawling for search results from Booking.com and "
    "then collates it through Google Forms data entry.")
print("Note: Google Forms data entry link should include three fields - Listing Name, Listing Price, and URL\n")
listing_site = input('Please enter Booking.com search result link: ')
forms_site = input('Please enter Google Forms data entry link: ')
list_maker = ListMaker()
