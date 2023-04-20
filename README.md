# facebook-marketplace-scraper

<p align="center">
<img src="https://i.imgur.com/Mizo3N9.png">
</p>
<h3 align="center">An open-source Python program to scrape Facebook Marketplace using Selenium, BeautifulSoup, and SQLite.</h3>
<h3 align="center">

```diff
You use the software provided at your own risk. I cannot be held responsible for any potential consequences, including potential bans from Meta.
```
### Overview
This open-source program uses a combination of Python and SQLite  to scrape data from Facebook Marketplace. The program uses the Selenium webdriver to navigate the Facebook Marketplace website and BeautifulSoup to parse the HTML and extract relevant data. It then stores the data in an SQLite database. The program also has a GUI made with PyQt5 that allows the user to start the scraping process.

### Customization
This program can be customized to your personal/organizational needs. For more information please contact me via [LinkedIn](https://www.linkedin.com/in/harmindersinghnijjar/) or email at harmindernijjar1996@gmail.com
  
### Frameworks:
- PyQt5 
- Selenium 
- BeautifulSoup 
- SQLite 
  
### Language: 
- [Python](https://www.python.org/)
  
### Flow diagrams:

### Requirements:
- Python 3.x
- Selenium
- PyQt5 
- BeautifulSoup 
- SQLite
  
 ### Modules:
- Selenium: The Selenium module is used to automate the browser. It is used to navigate to the Facebook Marketplace website and get the page source.
- BeautifulSoup: BeautifulSoup is used to parse the HTML and extract the relevant data.
- SQLite: SQLite is used to store the scraped data in a database.
- PyQt5: PyQt5 is used to create a GUI so the user can start the scraping process.
  
 ### API:
  
 ### Classes:
- Selenium 
- MainWindow
  
### Functions:
- `__init__`: Initializes the Selenium browser. 
- `get_page_source`: Gets the HTML source code of the current page. 
- `close_browser`: Closes the Selenium browser. 
- `scrape_facebook_marketplace`: Scrapes the Facebook Marketplace page using Selenium, BeautifulSoup, and SQLite. 
- `scrape_marketplace`: Starts the scraping process.
 
### Procedure:
1. The user launches the program.
2. The GUI window is displayed.
3. The user clicks the "Scrape Marketplace" button.
4. The program initializes the Selenium browser and navigates to the Facebook Marketplace page.
5. The program extracts relevant data from the page and stores it in an SQLite database.
6. The program closes the browser. 
