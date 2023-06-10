import scrapy

class NguyenKimSpider(scrapy.Spider):
    name = "nguyenkim"
    start_urls = ["https://www.nguyenkim.com/dien-thoai-di-dong"]
    
    def parse(self, response):
        phone_list = response.css(".product-render")
        for phone in phone_list:
          yield scrapy.Request(phone.css("a::attr(href)").get(), callback=self.parse_new)
        next_page = response.css("a.btn_next.ty-pagination__item.ty-pagination__btn.ty-pagination__next.cm-history::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
      
    def parse_new(self,response):
      infor= response.css('tbody tr')
      img_base ='https://cdn.nguyenkimmall.com'
      yield{
        'link':response.url,
        'img':img_base + response.css("ul.nk-product-bigImg img::attr(src)").get(),
        'name': response.css("h1.product_info_name::text").get(),
        'price': response.css("div.product_info_price_value-final span.nk-price-final::text").get(),
        'color': infor[1].css("td.value::text").get(),
        'ram': infor[7].css("td.value::text").get(),
        'bonho': infor[8].css("td.value::text").get()
      }

    