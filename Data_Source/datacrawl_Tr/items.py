# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()
    pass


# class BookItem(scrapy.Item):
#     url = scrapy.Field()
#     title = scrapy.Field()
#     upc = scrapy.Field()
#     product_type = scrapy.Field()
#     tax = scrapy.Field()
#     num_reviews = scrapy.Field()
#     price_excl_tax = scrapy.Field(serializer = serialize_price)
#     price_incl_tax = scrapy.Field(serializer = serialize_price)
#     star = scrapy.Field()
#     description = scrapy.Field()
#     price = scrapy.Field()
#     category = scrapy.Field()
