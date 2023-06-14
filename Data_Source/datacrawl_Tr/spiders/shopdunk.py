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
        phone_url_list = response.css('div.page-body div.product-essential div.overview div.attributes ul.option-list li a ::attr(href)').extract()
        x = len (phone_url_list)
        
        if x == 0:
            phone_url = response.xpath("/html/head/meta[11]").attrib['content']
            yield response.follow (phone_url, callback=self.parse_phone_page) 
        
        else:
            for i in range (0, x):
                phone_url = 'https://shopdunk.com' + phone_url_list[i]
                yield response.follow (phone_url, callback=self.parse_phone_page)   

        
    def parse_phone_page(self,response):  
        c = len(response.css('div.page-body div.product-essential div.overview div.attributes ul.attribute-squares li label span ::attr(title)').extract())
        color_list = response.css('div.page-body div.product-essential div.overview div.attributes ul.attribute-squares li label span ::attr(title)').extract()

        price = response.css('div .prices .product-price span::text').get()
        price = price.replace(" ", "")
        price = price.replace("\n", "")

        memory = response.css('div.page-body div.product-essential div.overview div.attributes ul.option-list li a label.checked-attr ::text').get()
        if memory is None:
            memory = response.css('div.page-body div.product-essential div.overview div.attributes ul.option-list li label ::text').get()
        
        for i in range (0, c):
            color = color_list[i]    
            yield{
                    'url': response.xpath("//html/head/link[3]").attrib['href'],
                    'name':response.css('h1 .main-name ::text').get(),
                    'img_url': response.css('div .product-essential .gallery .picture a::attr(href)').get(),
                    'price': price.replace("\r", ""),
                    'memory': memory,
                    'color1': color
                }
                

       
