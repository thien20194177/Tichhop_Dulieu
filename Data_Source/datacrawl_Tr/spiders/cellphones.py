import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "cellphonespider"
    start_urls=[]

    def start_requests(self):
    
        start_urls = ['https://cellphones.com.vn/mobile/apple.html',
                      'https://cellphones.com.vn/mobile/tecno.html',
                      'https://cellphones.com.vn/mobile/nubia.html',
                      'https://cellphones.com.vn/mobile/vivo.html',
                      'https://cellphones.com.vn/mobile/asus.html',
                      'https://cellphones.com.vn/mobile/oneplus.html',
                      'https://cellphones.com.vn/mobile/nokia.html',
                      'https://cellphones.com.vn/mobile/realme.html',
                      'https://cellphones.com.vn/mobile/oppo.html',
                      'https://cellphones.com.vn/mobile/xiaomi.html',
                      'https://cellphones.com.vn/mobile/samsung.html?version=2',                            
                    ]
    
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        phones = response.css('div.filter-sort__list-product div.block-product-list-filter div.product-info a')

        for phone in phones:
                
                phone_url = phone.css('a::attr(href)').get()
                yield response.follow (phone_url, callback = self.new_me_parse)     
        
    def new_me_parse(self, response): 
        list_phones_url = response.css('div .box-detail-product__box-center .box-linked a ::attr(href)')   
        x = len (list_phones_url)
        phones_url = response.css('div .box-detail-product__box-center .box-linked a ::attr(href)') .extract()
        for i in range (0, x):
                phone_url = phones_url[i]
                yield response.follow (phone_url, callback=self.parse_phone_page)
        
    def parse_phone_page(self,response):  
        a = response.xpath("//section/div[4]/div[2]/div[1]/ul/li[8]/div/text()").get()
        b = response.xpath("//section/div[2]/div[2]/div/div/a[@class='item-linked button__link linked-undefined active']//strong/text()").get()
        if a == b:
            m = a
        else:
             m = a +"(" + b + ")"
        list_color = response.css('div .box-product-variants .box-content .list-variants a strong ::text').extract()
        list_color_price = response.css('div .box-product-variants .box-content .list-variants a span ::text').extract()
        phone_price = response.xpath("//section/div[2]/div[2]/div/div/a[@class='item-linked button__link linked-undefined active']/span/text()").get()
        x = len(response.css('div .box-product-variants .box-content .list-variants a strong ::text'))
      
        for i  in range (0, x):
            c = list_color[i]
            p = phone_price
            if p <= list_color_price [i]:
                 p = list_color_price[i]
       
            yield{
                'url': response.xpath("/html/head/meta[5]").attrib['content'],
                'name = ':response.css('div.box-product-name h1::text').get(),
                'img_url =': response.xpath("///section/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div/img").attrib['src'],
                'price =': p,
                'memory =': m,
                'color': c, 
            }
                

       
