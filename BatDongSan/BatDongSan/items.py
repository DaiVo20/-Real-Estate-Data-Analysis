# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BatDongSanItem(scrapy.Item):
    # Mã căn/ Mã căn hộ
    unitnumber = scrapy.Field()
    # Phường
    ward = scrapy.Field()
    # Quận
    area = scrapy.Field()
    # Tỉnh/Thành phố
    region = scrapy.Field()
    # Địa chỉ
    address = scrapy.Field()
    # Tình trạng bất động sản
    property_status = scrapy.Field()
    # Diện tích/m2
    price_m2 = scrapy.Field()
    # Hướng cửa chính
    direction = scrapy.Field()
    # Hướng ban côngc
    balconydirection = scrapy.Field()
    # Giấy tờ pháp lý
    property_legal_document = scrapy.Field()
    # Diện tích
    size = scrapy.Field()
    # Số phòng ngủ
    rooms = scrapy.Field()
    # Số phòng vệ sinh
    toilets = scrapy.Field()
    # Tầng số
    floornumber = scrapy.Field()
    # Tên phân khu/Lô/Block/Tháp
    block = scrapy.Field()
    # Loại hình căn hộ
    apartment_type = scrapy.Field()
    # Tình trạng nội thất
    furnishing_sell = scrapy.Field()
    # Đặc điểm căn hộ
    apartment_feature = scrapy.Field()
    # Giá
    price = scrapy.Field()
