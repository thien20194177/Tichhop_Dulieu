import scrapy

class NguyenKimSpider(scrapy.Spider):
    name = "nguyenkim"
    start_urls = ["https://www.nguyenkim.com/dien-thoai-di-dong"]
    
    def parse(self, response):
        phone_list = response.css(".product-list > li")

        for phone in phone_list:
            phone_name = phone.css(".name a::text").get()
            phone_price = phone.css(".price strong::text").get()

            yield {
                "name": phone_name,
                "price": phone_price
            }

        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)