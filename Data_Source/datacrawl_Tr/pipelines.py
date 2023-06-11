# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


#class ScraperPipeline:
    # def process_item(self, item, spider):
    
    #     adapter = ItemAdapter(item)

    #     field_names = adapter.field_names()
    #     for field_name in field_names:
    #         if field_name != 'description':
    #             value = adapter.get(field_name)
    #             print("***")
    #             adapter[field_name] = value[0].strip()

    #     lowercase_keys = ['category', 'product_type']
    #     for lowercase_key in lowercase_keys:
    #         value = adapter.get(lowercase_key)
    #         adapter[lowercase_key] = value.lower()
        
    #     price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
    #     for price_key in price_keys:
    #         value = adapter.get(price_key)
    #         value = value.replace('£', '')
    #         adapter[price_key] = float(value)

    #     availability_string = adapter.get('availability')
    #     split_string_array = availability_string.split('(')
    #     if len(split_string_array) <2:
    #         adapter['availability'] = 0
    #     else:
    #         availability_array = split_string_array[1].split(' ')
    #         adapter ['availability'] = int (availability_array[0])

    #     num_reviews_string = adapter.get('num_reviews')
    #     adapter['num_reviews'] = int (num_reviews_string)

    #     star_string = adapter.get('star')
    #     split_stars_array = star_string.split(' ')
    #     starts_text_value = split_stars_array[1].lower()
    #     if starts_text_value == "zero":
    #         adapter['star'] = 0
    #     elif starts_text_value == "one":
    #         adapter['star'] = 1
    #     elif starts_text_value == "two":
    #         adapter['star'] = 2
    #     elif starts_text_value == "three":
    #         adapter['star'] = 3
    #     elif starts_text_value == "four":
    #         adapter['star'] = 4
    #     elif starts_text_value == "five":
    #         adapter['star'] = 5

 




    # return item
