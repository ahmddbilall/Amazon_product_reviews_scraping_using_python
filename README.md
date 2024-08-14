# Amazon Reviews Scraping: A Python Library Comparison

This project explores different Python libraries for scraping Amazon reviews. It includes implementations using Selenium, Scrapy, and BeautifulSoup to understand their strengths and limitations.

## Findings

### Selenium
Selenium successfully opens the Amazon page and displays it. However, it sometimes redirects to the login page, which can be manually handled due to the browser being open. Despite setting time delays for page loading, it fetches only a few reviews and encounters errors for the rest.

### Scrapy
Scrapy encounters issues with redirection to the login and captcha pages after fetching the first page of reviews. Solving or bypassing the captcha remains a challenge as Scrapy lacks a web driver interface like Selenium.

### BeautifulSoup
BeautifulSoup works efficiently in this context. By providing the ASIN and specifying the number of pages, it generates a CSV file with the review data.

## How to Use

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ahmddbilall/Amazon_product_reviews_scraping_using_python.git
   ```

2. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```
