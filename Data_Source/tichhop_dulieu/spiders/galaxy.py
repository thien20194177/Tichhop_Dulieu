import scrapy
import time
class GalaxySpider(scrapy.Spider):
    name = "galaxy"
    start_urls = []
    def start_requests(self):
      start_urls = ["https://galaxydidong.vn/category/samsung",
                  "https://galaxydidong.vn/category/xiaomi",
                  "https://galaxydidong.vn/category/iphone"
                  ]
      for url in start_urls:
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        phone_list = response.css(".product-small.box ")
        for phone in phone_list:
          yield scrapy.Request(phone.css("a::attr(href)").get(), callback=self.parse_new)
        next_page = response.css("a.next.page-number::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
      
    def parse_new(self,response):
      time.sleep(10)
      imgs = response.css("div.woocommerce-product-gallery__image.slide a::attr(href)").extract()
      colors = response.css(".price-custom span.name-pv::text").extract()
      prices = response.css(".price-custom span bdi::text").extract()
      bonhos = response.css("div.product-items.active a div.product_linked-storage::text").getall()
      bonho=''
      ram=''
      if len(bonhos)==2:
        ram = bonhos[0]
        bonho=bonhos[1]

      if len(bonhos)==1:
        bonho=bonhos[0]
        ram =''

      for i in range(0, len(colors)):
       yield{
        'link':response.url,
        'img':imgs[i],
        'name': response.css("h1.product-title.product_title.entry-title::text").get(),
        'price': prices[i],
        'color': colors[i],
        'ram': ram,
        'bonho': bonho
        }