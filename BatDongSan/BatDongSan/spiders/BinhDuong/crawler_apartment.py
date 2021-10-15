import scrapy
from scrapy import Spider
from BatDongSan.items import ApartmentItem
import re
import json


# cd BatDongSan\data
# scrapy crawl binh-duong-apartment -o dataset_BinhDuongApartment.csv

class BinhDuongApartmentChoTotSpider(Spider):
    name = "binh-duong-apartment"
    allowed_domains = ["nha.chotot.com", "gateway.chotot.com"]
    start_urls = ["https://nha.chotot.com/binh-duong/mua-ban-can-ho-chung-cu", ]

    def parse(self, response):
        url = 'https://nha.chotot.com/binh-duong/mua-ban-can-ho-chung-cu?page={}'
        api_url = 'https://gateway.chotot.com/v1/public/ad-listing/{}'
        page = 1
        # Số trang chứa dữ liệu
        total_page = 81
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
        item = ApartmentItem()
        json_data = json.loads(response.text)
        item['price'] = json_data['ad']['price']

        if json_data['ad']['type_name'] == 'Cần mua':
            return

        attribute_map = ['unitnumber', 'ward', 'area', 'region',
                         'address', 'property_status', 'price_m2', 'direction',
                         'balconydirection', 'property_legal_document',
                         'size', 'rooms', 'toilets', 'floornumber',
                         'block', 'apartment_type', 'furnishing_sell',
                         'apartment_feature', 'price']

        for para in json_data['parameters']:
            para_id = para['id']
            value = para['value']
            if para_id in attribute_map:
                item[para_id] = value

        yield item
