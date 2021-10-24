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

    '''
    - Phương thức này sẽ lấy dữ liệu 10 trang của từng địa điểm tương ứng với từng loại bất động sản
        locations: Một dict lưu trữ các địa điểm cần crawl (3 địa điểm)
        type_real_estates: Loại bất động sản (3 loại bất động sản)
    - Mỗi loại bất động sản tương ứng với mỗi địa điểm sẽ được lấy dữ liệu 10 trang trên Chotot.com.
    - Mỗi trang sẽ có một danh sách các sản phẩm, mỗi sản phẩm sẽ có một đường dẫn, trong đây sẽ có một id mà
      chúng ta sẽ có thể dùng để lấy được các thông tin chi tiết của sản phẩm thông qua việc gọi api.
    - Mỗi sản phẩm trên từng trang sẽ được gọi api lấy thông tin chi tiết và chuyển đến phương thức parse_item
      để merge dữ liệu và dataframe
    '''
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

    '''
    - Phương thức này nhận json từ api đã request trước đó và map vào item
        response:   là phản hồi sau khi request từ api
        attribute_map:  là các thuộc tính sẽ được map từ json vào item
    - Các thuộc tính có type_name là cần mua sẽ bỏ qua.
    - Loại bất động sản là giá trị hiện tại của current_type_name khi phương thức này được gọi thực hiện.
    - Trong chuỗi json sẽ có parameter, tương ứng mỗi parameter sẽ có id, value tương ứng (có thể bị khuyết tùy theo dữ liệu), trong đó:
        id: tương ứng với tên thuộc tính trong attribute_map
        value: tương ứng với giá trị các thuộc tính đó
    - Giá trị trả về là item - sẽ được merge vào dataframe sau khi kết thúc quá trình crawl
    '''
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