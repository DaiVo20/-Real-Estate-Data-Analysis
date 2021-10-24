import scrapy
from scrapy import Spider
from BatDongSan.items import RealEstateItem
import re
import json


# cd BatDongSan\data
# scrapy crawl crawl-data -o dataset.csv

class RealEstateChoTotSpider(Spider):
    name = "crawl-data"
    allowed_domains = ["nha.chotot.com", "gateway.chotot.com"]
    start_urls = ["https://nha.chotot.com"]
    base_url = "https://nha.chotot.com/{}/{}?page={}"
    api = 'https://gateway.chotot.com/v1/public/ad-listing/{}'
    current_type_name = None

    def parse(self, response):
        locations = {"tp-ho-chi-minh": "TP Hồ Chí Minh", "binh-duong": "Bình Dương", "dong-nai": "Đồng Nai"}
        type_real_estates = {"mua-ban-can-ho-chung-cu": "Căn hộ/Chung cư", "mua-ban-nha-dat": "Nhà ở",
                             "mua-ban-dat": "Đất"}

        for location, location_name in locations.items():
            for type_real_estate, type_name in type_real_estates.items():
                url = self.base_url.format(location, type_real_estate, 1)
                self.current_type_name = type_name
                scrapy.Request(url)
                total_page = 10
                page = 1
                while True:
                    items = response.xpath('//div//li//a[@class="AdItem_adItem__2O28x"]')
                    for item in items:
                        href = item.attrib.get('href')
                        id_extract = re.findall(r'(\d+).htm', href)
                        if len(id_extract) == 0:
                            continue
                        yield scrapy.Request(self.api.format(id_extract[0]), callback=self.parse_item)
                    page += 1
                    if page > total_page:
                        break
                    yield scrapy.Request(self.base_url.format(location, type_real_estate, page),
                                         callback=self.parse)

    def parse_item(self, response):
        item = RealEstateItem()
        attribute_map = ['unitnumber', 'ward', 'area', 'region', 'address', 'property_status',
                         'price_m2', 'direction', 'balconydirection', 'property_legal_document',
                         'size', 'block', 'price', 'floornumber', 'apartment_type', 'floornumber',
                         'furnishing_sell', 'apartment_feature', 'rooms', 'toilets', 'floors',
                         'house_type', 'furnishing_sell', 'living_size', 'width', 'length',
                         'land_type', 'property_road_condition', 'land_feature', 'property_back_condition']
        json_data = json.loads(response.text)
        item['type_real_estate'] = self.current_type_name
        item['price'] = json_data['ad']['price']

        if 'type_name' in json_data['ad'] and json_data['ad']['type_name'] == 'Cần mua':
            return

        for para in json_data['parameters']:
            if 'id' in para:
                para_id = para['id']
                if 'value' in para and para_id in attribute_map:
                    value = para['value']
                    item[para_id] = value

        yield item