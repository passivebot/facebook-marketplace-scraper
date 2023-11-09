# Author: harmindersinghnijjar
# Date: 2023-11-08
# Version: 1.0.1
# Usage: python main.py

# Standard library imports
import logging
import random
import re
import sqlite3
import time
import asyncio

# Related third-party imports
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# Set username.
USER = getpass.getuser()

# Declare global variables.
ELECTRONICS = 'https://www.facebook.com/marketplace/category/electronics?deliveryMethod=local_pick_up&exact=false'
APPLIANCES = 'https://www.facebook.com/marketplace/category/appliances?deliveryMethod=local_pick_up&exact=false'
FURNITURE = 'https://www.facebook.com/marketplace/category/furniture?deliveryMethod=local_pick_up&exact=false'
LOCATIONS = ['pullman', 'colfax', 'moscow']

# Define a Selenium class to automate the browser.
class Selenium():
    # Define a method to initialize the browser.
    def __init__(self):
        # Close the Chrome instance if it is already running.
        os.system("taskkill /f /im chrome.exe")
        # Set the options for the Chrome browser.
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # Add a user data directory as an argument for options.
        chrome_options.add_argument(
            f"--user-data-dir=C:\\Users\\{USER}\\AppData\\Local\\Google\\Chrome\\User Data")
        chrome_options.add_argument("profile-directory=Default")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        # Initialize the Chrome browser using the ChromeDriverManager.
        self.browser = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)

    # Define a method to get the page source using Selenium.
    def get_page_source(self, url):
        # Try to get the page source.
        try:
            # Load the URL.
            self.browser.get(url)
            
            # Wait for the page to load.
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class=' x1gslohp x1e56ztr']")))

            for i in range(1, 5):
                # Scroll down to the bottom of the page to load all items.
                self.browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                # Wait for the page to finish loading.
                sleep(5)
            

            # Get the page source.
            page_source = self.browser.page_source
            
            return page_source

        # Catch any exceptions.
        except TimeoutException:
            print("Timed out waiting for page to load.")
            return None

        except NoSuchElementException:
            print("Element not found.")
            return None

    # Define a method to close the browser.
    def close_browser(self):
        self.browser.quit()

    # Define a method tp scrape the Facebook Marketplace page using Selenium, BeautifulSoup, and SQLite.
    def scrape_facebook_marketplace(self):
        # Initialize the Selenium class.
        # sel = Selenium()
        # Initialize the database connection.
        conn = sqlite3.connect("facebook_marketplace.db")
        c = conn.cursor()

        # Create the tables if they don't exist.
        c.execute('''CREATE TABLE IF NOT EXISTS facebook_marketplace_posts
                  (id INTEGER PRIMARY KEY, title TEXT, image TEXT, price TEXT, location TEXT, category TEXT, url TEXT, date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        # TODO: Remove these two loops and replace them with a single loop that iterates 3 times. However, the code below works for now and trying to fix it is not a priority.
        for location in LOCATIONS:
            for category, url in {'Electronics': ELECTRONICS, 'Appliances': APPLIANCES, 'Furniture': FURNITURE}.items():
                # Keeping the number of iterations below 5 for now to avoid getting blocked by Facebook and also to keep the results from being too far away from Pullman.
                for i in range (1, 5):
                    # Scroll down to the bottom of the page to load all items.
                    self.browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    # Sleep for 5 seconds then scroll again.
                    time.sleep(1)
               
                # Get the page source using Selenium.
                page_source = self.get_page_source(url)

                # Parse the page source using BeautifulSoup.
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Get the items.
                div = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6')
                
                # Iterate through the items.
                for d in div:
                    try:
                        # Get the item image.
                        image = d.find('img', class_='xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
                        # Get the item title from span.
                        title = d.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
                        # Get the item price.
                        price = d.find('span', 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text
                        # Get the item URL.
                        url = d.find('a', class_='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv')['href']
                        # Get the item location.
                        location = d.find('span', 'x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84').text
                        
                        # Print the item information.
                        print(f"Image: {image}")
                        print(f"Price: {price}")
                        print(f"Title: {title}")
                        print(f"Location: {location}")
                        print(f"Category: {category}")
                        url = (f"www.facebook.com{url}")
                        print(f"URL: {url}")
                        print("------------------------")
                        # Add the item to the database including the image.
                        c.execute("INSERT INTO facebook_marketplace_posts (title, image, price, location, category, url) VALUES (?, ?, ?, ?, ?, ?)", (title, image, price, location, category, url))
                        conn.commit()
                    except:
                        pass

            
        # Close the database connection.
        conn.close()
        
        # Close the browser.
        self.close_browser()
        
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the window title and size.
        self.title("Facebook Marketplace Scraper")
        self.geometry("350x200")
        
        # Add a label to the window.
        self.label = tk.Label(self, text="Click the button to start scraping Facebook Marketplace.")
        self.label.pack(pady=10)

        # Add a button to the window.
        self.button = tk.Button(self, text="Scrape Marketplace", command=self.scrape_marketplace)
        self.button.pack(pady=10)
        
        # Add a label to write "Developed by" to the window.
        self.label = tk.Label(self, text="Developed by:")
        self.label.pack(pady=2)
        
        
        # Add Logo to the window.
        self.logo = tk.PhotoImage(file="logo.png")
        self.logo = self.logo.subsample(2, 2)
        self.label = tk.Label(self, image=self.logo)
        self.label.pack(pady=10)

    # Define a method to scrape Facebook Marketplace.
    def scrape_marketplace(self):
        # Initialize the Selenium class.
        sel = Selenium()
        # Call the scrape_facebook_marketplace method.
        sel.scrape_facebook_marketplace()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

                
