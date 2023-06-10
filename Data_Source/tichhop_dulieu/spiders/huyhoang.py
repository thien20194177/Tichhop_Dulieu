import scrapy
from scrapy.http import FormRequest

class HuyHoangSpider(scrapy.Spider):
    name = 'HuyHoang'
    #allowed_domains = ['www.huyhoangmobile.vn']
    start_urls=[]
    def start_requests(self):
      start_urls = ["https://www.huyhoangmobile.vn/san-pham/oppo",
                  "https://www.huyhoangmobile.vn/san-pham/xiaomi",
                  "https://www.huyhoangmobile.vn/san-pham/samsung/trang-1",
                  "https://www.huyhoangmobile.vn/san-pham/samsung/trang-2",
                  "https://www.huyhoangmobile.vn/san-pham/iphone"
                  ]
      for url in start_urls:
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
      #default_url ='https://www.dienmayxanh.com'
      listproduct=response.css('ul.cols.cols-5 > li.cate-pro-short')
      for product in listproduct:
        yield scrapy.Request(product.css("a::attr(href)").get(), callback=self.parse_new)
  

    def parse_new(self, response):
        items = response.css("div.linked a.item.i-25205::attr(href)").extract()
        for item in items:
          yield scrapy.Request(item, callback=self.parse_new2)
          
    def parse_new2(self, response):
      imgs = response.css('div.product-image-gallery.swiper-wrapper img::attr(data-src)').extract()
      colors = response.css('label.opt-label span.opt-name::text').extract()
      prices = response.css('label.opt-label span.opt-price::text').extract()
      temp=len(imgs)
      for i in range(0,temp):
       yield{
          'link': response.url,
          'img': imgs[i],
          'name':response.css("div.topview h1::text").get(),
          'color': colors[i],
          'price': prices[i],
          'ram': '',
          'bonho':response.css("div.linked a.item.i-25205.active span::text").get()
        }