import scrapy
from scrapy import Spider
from scrapy.exceptions import CloseSpider
from BatDongSan.items import BatDongSanItem
import re
import json


# scrapy crawl tp-ho-chi-minh -o dataset_HoChiMinh.csv
# type_name

class BatDongSanHCMChoTotSpider(Spider):
    name = "tp-ho-chi-minh"
    allowed_domains = ["nha.chotot.com", "gateway.chotot.com"]
    start_urls = ["https://nha.chotot.com/tp-ho-chi-minh/mua-ban-can-ho-chung-cu", ]

    def parse(self, response):
        url = 'https://nha.chotot.com/tp-ho-chi-minh/mua-ban-can-ho-chung-cu?page={}'
        api_url = 'https://gateway.chotot.com/v1/public/ad-listing/{}'
        page = 1
        # count = 0
        # flag = False
        while True:
            items = response.xpath('//div//li//a[@class="AdItem_adItem__2O28x"]')
            if len(items) == 0:
                raise CloseSpider("Crawled all")
            for item in items:
                href = item.attrib.get('href')
                id_extract = re.findall(r'(\d+).htm', href)
                if len(id_extract) == 0:
                    continue
                yield scrapy.Request(api_url.format(id_extract[0]), callback=self.parse_item)
                # count += 1
                # if count == 1000:
                #     flag = True
                #     break
            # if flag:
            #     break
            # else:
            page += 1
            yield scrapy.Request(url.format(page), callback=self.parse)

    def parse_item(self, response):
        item = BatDongSanItem()
        json_data = json.loads(response.text)
        item['price'] = json_data['ad']['price']

        attribute_map = ['unitnumber', 'ward', 'area', 'region', 'address',
                         'property_status', 'price_m2', 'direction', 'balconydirection',
                         'property_legal_document', 'size', 'rooms', 'toilets', 'floornumber',
                         'block', 'apartment_type', 'furnishing_sell', 'apartment_feature', 'price']

        for para in json_data['parameters']:
            para_id = para['id']
            value = para['value']
            if para_id in attribute_map:
                item[para_id] = value
        yield item
