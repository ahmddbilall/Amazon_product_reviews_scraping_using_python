import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"

    custom_settings = {
        'FEEDS': {
            'data/%(name)s_%(time)s.csv': {
                'format': 'csv',
                'overwrite': True,  
            }
        },
        'LOG_LEVEL': 'ERROR',  
    }

    def start_requests(self):
        asin_list = ['B0CX3NVXV9']
        for asin in asin_list:
            amazon_reviews_url = f'https://www.amazon.com/product-reviews/{asin}/'
            yield scrapy.Request(url=amazon_reviews_url, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': 0})

    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        next_page_relative_url = response.css(".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com/', next_page_relative_url)
            print(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': retry_count})

        elif retry_count < 3:
            retry_count += 1
            yield scrapy.Request(url=response.url, callback=self.parse_reviews, dont_filter=True, meta={'asin': asin, 'retry_count': retry_count})

        review_elements = response.css("#cm_cr-review_list div.review")
        for review_element in review_elements:
            yield {
                "asin": asin,
                "text": "".join(review_element.css("span[data-hook=review-body] ::text").getall()).strip(),
                "title": review_element.css("*[data-hook=review-title]>span::text").get(),
                "location_and_date": review_element.css("span[data-hook=review-date] ::text").get(),
                "verified": bool(review_element.css("span[data-hook=avp-badge] ::text").get()),
                "rating": review_element.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0],
            }

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AmazonReviewsSpider)
    process.start()  