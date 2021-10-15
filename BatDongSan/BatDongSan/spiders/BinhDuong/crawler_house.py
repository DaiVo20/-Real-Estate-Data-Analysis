import scrapy
from scrapy import Spider
from BatDongSan.items import HouseItem
import re
import json


# cd BatDongSan\data
# scrapy crawl binh-duong-house -o dataset_BinhDuongHouse.csv

class BinhDuongHouseChoTotSpider(Spider):
    name = "binh-duong-house"
    allowed_domains = ["nha.chotot.com", "gateway.chotot.com"]
    start_urls = ["https://nha.chotot.com/binh-duong/mua-ban-nha-dat", ]

    def parse(self, response):
        url = 'https://nha.chotot.com/binh-duong/mua-ban-nha-dat?page={}'
        api_url = 'https://gateway.chotot.com/v1/public/ad-listing/{}'
        page = 1
        # Số trang chứa dữ liệu
        total_page = 109
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
        item = HouseItem()
        json_data = json.loads(response.text)
        item['price'] = json_data['ad']['price']

        if json_data['ad']['type_name'] == 'Cần mua':
            return

        attribute_map = ['ward', 'area', 'region', 'address',
                         'price_m2', 'direction', 'property_legal_document',
                         'size', 'rooms', 'toilets', 'floors', 'house_type',
                         'block', 'furnishing_sell', 'property_road_condition',
                         'land_type', 'living_size', 'width', 'length', 'price']

        for para in json_data['parameters']:
            para_id = para['id']
            value = para['value']
            if para_id in attribute_map:
                item[para_id] = value

        yield item
