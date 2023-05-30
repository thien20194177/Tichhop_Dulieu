import scrapy
from scrapy.http import FormRequest

class CellPhoneSpider(scrapy.Spider):
    name = "CellPhone"
    start_urls = ["https://viettelstore.vn/dien-thoai"]
    base_url = "https://viettelstore.vn"

    def parse(self, response):
        phone_list = response.css(".product-list > li")

        for phone in phone_list:
            phone_name = phone.css(".name a::text").get()
            phone_price = phone.css(".price strong::text").get()

            yield {
                "name": phone_name,
                "price": phone_price
            }

        next_page_url = response.css(".loadmore .viewmore::attr(href)").get()
        if next_page_url:
            yield FormRequest(
                url=self.base_url + next_page_url,
                method="GET",
                callback=self.parse
            )