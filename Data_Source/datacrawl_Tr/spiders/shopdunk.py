import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "shopdunkspider"
   
    #allowed_domains = [ 'shopdunk']
    

    start_urls=[]
    def start_requests(self):
      start_urls = ['https://shopdunk.com/iphone']
      for url in start_urls:
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):

        phones = response.css('div .item-box .product-item')

        for phone in phones:
        
            relative_url = phone.css('h2 a ::attr(href)').get()
            phone_url = 'https://shopdunk.com' + relative_url        
            yield response.follow (phone_url, callback=self.newparse)         
        
        
    def newparse(self, response): 
    
        x = len(response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li"))
        y = len(response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li"))

        if x < y:
            k = y
        else: 
            k = x
        
        a = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[1]/a").get()
        
        if a is None:
            yield response.follow (response.xpath("/html/head/link[3]").attrib['href'], callback=self.parse_phone_page)
        
        else:

            if len(response.xpath("//div[@class='attributes']/dl/dd")) > 3:
                m = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li[1]").get()
                if m is not None:
                    a = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li[1]/a").attrib['href']
                    if k >=2 :                     
                        b = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li[2]/a").attrib['href']
                    if k>= 3:
                        c = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li[3]/a").attrib['href']
                    if k >=4:
                        d = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li[4]/a").attrib['href']
                else:
                    a = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[1]/a").attrib['href']
                    if k >=2:
                        b = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[2]/a").attrib['href']
                    if k >= 3:    
                        c = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[3]/a").attrib['href']
                    if k >=4:    
                        d = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[4]/a").attrib['href']
            else:
                    a = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[1]/a").attrib['href']
                    if k >=2:
                        b = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[2]/a").attrib['href']
                    if k >= 3:    
                        c = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[3]/a").attrib['href']
                    if k >=4:    
                        d = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[1]/ul/li[4]/a").attrib['href']

                
            
            

            for i in range (0, k, 1):   
            
                    if i == 0:
                        phone_url = 'https://shopdunk.com' + a
                    yield response.follow (phone_url, callback=self.parse_phone_page)
                    
                    if i == 1:
                        yield response.follow ('https://shopdunk.com' + b , callback=self.parse_phone_page)
                    
                    if i == 2:
                        yield response.follow ('https://shopdunk.com' + c , callback=self.parse_phone_page)
                    
                    if i == 3:
                        yield response.follow ('https://shopdunk.com'  +d,  callback=self.parse_phone_page)      

        
    def parse_phone_page(self,response):  
        
        k = len(response.xpath("//div[@class='attributes']/dl/dd"))
               
        if len(response.xpath("//div[@class='attributes']/dl/dd")) > 3:
            m = response.xpath("//form/div[2]/div[1]/div[4]/div[4]/dl/dd[3]/ul/li[1]").get()
            if m is not None:
                x = len(response.xpath("//div[@class='attributes']/dl/dd")) - 1
            else: 
                x = len(response.xpath("//div[@class='attributes']/dl/dd")) - 3
        else: 
                x = len(response.xpath("//div[@class='attributes']/dl/dd")) - 1
       
    
        yield{
                'url': response.xpath("//html/head/link[3]").attrib['href'],
                'name':response.css('h1 .main-name ::text').get(),
                'img_url': response.css('div .product-essential .gallery .picture a::attr(href)').get(),
                'price': response.css('div .prices .product-price span::text').get(),
                'memory': response.xpath("//div[@class='attributes']/dl/dt[{0}]/span[1]/text()".format(str(x))).get(),
                'color1':response.xpath("///div[4]/dl/dd[{0}]/ul/li[1]/label/span".format(str(k))).attrib['title'],
                'color2':response.xpath("///div[4]/dl/dd[{0}]/ul/li[2]/label/span".format(str(k))).attrib['title'],
                #'color3':response.xpath("///div[4]/dl/dd[{0}]/ul/li[3]/label/span".format(str(k))).attrib['title'],
            
            }
                

       
