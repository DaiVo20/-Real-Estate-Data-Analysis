import scrapy
from scrapy import Spider
from BatDongSan.items import LandItem
import re
import json


# cd BatDongSan\data
# scrapy crawl binh-duong-land -o dataset_BinhDuongLand.csv

class BinhDuongLandChoTotSpider(Spider):
    name = "binh-duong-land"
    allowed_domains = ["nha.chotot.com", "gateway.chotot.com"]
    start_urls = ["https://nha.chotot.com/binh-duong/mua-ban-dat", ]

    def parse(self, response):
        url = 'https://nha.chotot.com/binh-duong/mua-ban-dat?page={}'
        api_url = 'https://gateway.chotot.com/v1/public/ad-listing/{}'
        page = 1
        # Số trang chứa dữ liệu
        total_page = 153
        while True:
            items = response.xpath('//div//li//a[@class="AdItem_adItem__2O28x"]')
            for item in items:
                href = item.attrib.get('href')
                id_extract = re.findall(r'(\d+).htm', href)
                if len(id_extract) == 0:
                    continue
                yield scrapy.Request(api_url.format(id_extract[0]), callback=self.parse_item)
            page += 1
            if page > total_page:
                return
            yield scrapy.Request(url.format(page), callback=self.parse)

    def parse_item(self, response):
        item = LandItem()
        json_data = json.loads(response.text)
        item['price'] = json_data['ad']['price']

        if json_data['ad']['type_name'] == 'Cần mua':
            return

        attribute_map = ['ward', 'area', 'region', 'address',
                         'price_m2', 'direction', 'property_legal_document',
                         'size', 'land_feature', 'property_road_condition',
                         'property_back_condition', 'block', 'land_type',
                         'width', 'length', 'price']

        for para in json_data['parameters']:
            para_id = para['id']
            value = para['value']
            if para_id in attribute_map:
                item[para_id] = value

        yield item
