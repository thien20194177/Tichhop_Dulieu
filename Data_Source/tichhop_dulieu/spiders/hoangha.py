import scrapy
from scrapy.http import FormRequest

class HoangHaSpider(scrapy.Spider):
    name = "hoangha"
    start_urls = ["https://hoanghamobile.com/dien-thoai-di-dong?p=9#page_9"]
  
    def parse(self, response):
        phone_list = response.css(".col-content lts-product ")

        for phone in phone_list:
            phone_link = phone.css(".img > a::attr(href)").extract()
            phone_name = phone.css(".infor > a::text").extract()
            phone_price = phone.css("span.price strong::text").extract()

            yield {
                "link": phone_link,
                "name": phone_name,
                "price":phone_price
            }

