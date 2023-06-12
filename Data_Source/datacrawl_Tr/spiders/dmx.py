import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "dmxspider"
    start_urls=[]

    def start_requests(self):
    
        start_urls = [
                'https://www.dienmayxanh.com/dien-thoai-samsung',
                   'https://www.dienmayxanh.com/dien-thoai-apple-iphone',
                   'https://www.dienmayxanh.com/dien-thoai-oppo',
                   'https://www.dienmayxanh.com/dien-thoai-xiaomi',
                   'https://www.dienmayxanh.com/dien-thoai-vivo',
                   'https://www.dienmayxanh.com/dien-thoai-realme',
                   'https://www.dienmayxanh.com/dien-thoai-nokia',
                   'https://www.dienmayxanh.com/dien-thoai-masstel',
                   'https://www.dienmayxanh.com/dien-thoai-mobell',
                   'https://www.dienmayxanh.com/dien-thoai-itel'
                  ]
    
        for url in start_urls:
            
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        phones = response.css('.container-productbox .item .main-contain')

        for phone in phones:
            
                relative_url = phone.css('a::attr(href)').get()
                phone_url = 'https://www.dienmayxanh.com' + relative_url 
                yield response.follow (phone_url, callback = self.new_me_parse)     

              
        
    def new_me_parse(self, response): 
        sameproduct1 = response.css('.box_main .box_right .box03')
        k = len (sameproduct1)
        
        if k == 0:
            phone_url = response.xpath("//html/head/link[1]").attrib['href']
            if 'dien-thoai' in phone_url:
                same_phone_url = response.xpath("///html/head/link[1]").attrib['href'] 
                yield response.follow (same_phone_url, callback=self.parse_phone_page)
        
        if k == 1:
            samephone = sameproduct1[0]  
            #divided by memory
            same_phone = samephone.css('a ::attr(href)').extract()
            x = len(same_phone)
            for i in range (0, x):
                same_phone_url = 'https://www.dienmayxanh.com' + same_phone[i]
                yield response.follow (same_phone_url, callback=self.parse_phone_page)

        else:
            samephone = sameproduct1[0]  
            #divided by memory
            same_phone = samephone.css('a ::attr(href)').extract()
            x = len(same_phone)
            for i in range (0, x):
                same_phone_url = 'https://www.dienmayxanh.com' + same_phone[i]
                yield response.follow (same_phone_url, callback=self.new_color_parse)
        
        
    def new_color_parse(self, response): 
        
        sameproduct1 = response.css('.box_main .box_right .box03')
        k = len (sameproduct1)
        
        # if k == 1:
        #     samephone = sameproduct1[0]  
        #     #divided by color (one-option)
        #     same_phone = samephone.css('a ::attr(href)').extract()
        #     x = len(same_phone)
            
        #     for i in range (0, x):
        #         same_phone_url = 'https://www.dienmayxanh.com' + same_phone[i]
        #         yield response.follow (same_phone_url, callback=self.parse_phone_page)
        samephone = sameproduct1[1] #divided by color (two-option)

        same_phone = samephone.css('a ::attr(href)').extract()

        x = len(same_phone)
        for i in range (0, x):
                if 'dienmayxanh' not in same_phone :
                    same_phone_url = 'https://www.dienmayxanh.com' + same_phone[i]
                else:
                    same_phone_url = samephone[i]
                yield response.follow (same_phone_url, callback=self.parse_phone_page)
       
        
    def parse_phone_page(self,response):  

        a = response.xpath("///html/body/section[1]/div[3]/div[2]/div/div/div/p[@class='box-price-present']/text()").get()  
                                       
        b = response.xpath("//section[1]/div[3]/div[2]/div/div[@class='box03 color group desk']/a[@class='box03__item item act']/text()").get()
        if b is None:
            b = response.xpath("///html/body/section[1]/div[3]/div[1]/div[1]/div[2]/div/div[@id='thumb-color-images-gallery-17']/p/text()").get()
        c = (len(response.xpath("/html/body/section[1]/div[3]/div[2]/div[@class='parameter']/ul/li")))
        if c >= 9:
            c = response.xpath("/html/body/section[1]/div[3]/div[2]/div[@class='parameter']/ul/li[7]/div/span/text()").get()
        else: 
            c =response.xpath("/html/body/section[1]/div[3]/div[2]/div[@class='parameter']/ul/li[4]/div/span/text()").get()
        yield{
            'url': response.xpath("///html/head/link[1]").attrib['href'],
            'name = ':response.xpath("//section[1]/h1/text()").get(),
            'img_url =': response.xpath("//section[1]/div[3]/div[1]/div[1]/div[1]/div/div[1]/a/img").attrib['src'],
            'price =': a,
            'memory =': c,
            'color': b, 
           
        }
                

       
