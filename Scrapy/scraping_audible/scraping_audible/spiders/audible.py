import scrapy
from ..items import ScrapingAudibleItem

class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["www.audible.com"] # only the home page
    # start_urls = ["https://www.audible.com/search/"] # https targt website
    
    request_custom_headers={
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
    }

    def start_requests(self):
        request = scrapy.Request(url="https://www.audible.com/search/", callback=self.parse, 
                                headers=self.request_custom_headers)
        # request.meta['proxy'] = "host:port"
        yield request

    def parse(self, response):
        product_containers = response.xpath('//div[@class="adbl-impression-container "]/div/span/ul/li')
        items = ScrapingAudibleItem()
        for product in product_containers:
            book_title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').get()
            book_length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()

            items['title'] = book_title
            items['author'] = book_author
            items['runtime'] = book_length

            # yield {
            #     'title' : book_title,
            #     'author' : book_author,
            #     'runtime' : book_length,
            #     # 'User-Agent':response.request.headers['User-Agent']
            # }

            yield items

        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a/@href').get()

        if next_page_url: # if next page exists
            yield response.follow(url=next_page_url, callback=self.parse,
                                  headers=self.request_custom_headers)
