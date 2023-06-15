import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "phvspider"
    start_urls=[]

    def start_requests(self):    
        start_urls = ['https://phongvu.vn/c/phone-dien-thoai' ]
    
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        phones = response.css('div.minWidthWrapper a.css-pxdb0j')

        for phone in phones:
                phone_url = 'https://phongvu.vn' +phone.css('a::attr(href)').get()
                yield response.follow (phone_url, callback = self.new_color_parse)     
        
    def new_color_parse(self, response): 
        list_phones_color = response.xpath("//div[@class='minWidthWrapper']//div[@class='css-qmrpdk']/div[1]//a/text()")   
        x = len (list_phones_color)
        phones_url = response.css('div.minWidthWrapper div.css-qmrpdk a::attr(href)').getall()
        
        for i in range (0, x):
                phone_url = 'https://phongvu.vn' + phones_url[i]
                
                if len(phone_url) != len(response.xpath("/html/head/link[6]").attrib['href']):
                    phone_url = response.xpath("/html/head/link[6]").attrib['href'] + "?sku=" +phone_url[len(phone_url)-9:len(phone_url)]
                yield response.follow (phone_url, callback=self.new_memory_page)
    
    def new_memory_page(self, response):
        list_phones_color = response.xpath("//div[@class='minWidthWrapper']//div[@class='css-qmrpdk']/div[1]//a/text()")   
        x = len (list_phones_color)
        total_list = response.css('div.minWidthWrapper div.css-6b3ezu div.css-qmrpdk  a ::attr(href)').extract()
        a = len (total_list)
        if x == a:
              yield response.follow (response.xpath("/html/head/link[6]").attrib['href'], callback=self.parse_phone_page)             
        else:
            
            for i in range (x, a, 1):
                
                phone_url = 'https://phongvu.vn' + total_list[i]
                if len(phone_url) != len(response.xpath("/html/head/link[6]").attrib['href']):
                    phone_url = response.xpath("/html/head/link[6]").attrib['href'] + "?sku=" +phone_url[len(phone_url)-9:len(phone_url)]

                yield response.follow (phone_url, callback=self.parse_phone_page)
        
    def parse_phone_page(self,response):  
        phone_infor = response.css('div.minWidthWrapper div.css-qmrpdk  div[type="caption"] ::text').extract()
        color = phone_infor[0]
        phone_infordi = response.css('div.minWidthWrapper div.css-17aam1 ::text').extract()
        
        i = len(phone_infordi)      
        memory = phone_infordi[i-3]
        
        name = response.xpath("//h1/text()").get()        
        if 'iPhone 13 | Chính Hãng VNA' in name:
            memory = phone_infordi[i-2]
           
        yield{                
                'name = ':name,
                'price =': response.xpath("//div[@class='minWidthWrapper']//div[@class='css-1q5zfcu']/div/text()").get(),
                'memory =': memory.replace("Bộ nhớ: ",""),
                'color':color.replace("Màu sắc: ", ""), 
                'url': response.xpath("/html/head/link[6]").attrib['href'],
                'img_url =': response.xpath("//div[@class='minWidthWrapper']//div[@class='css-j4683g']/img").attrib['src'],
            }
                

       
