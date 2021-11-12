# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlonhadatItem(scrapy.Item):
    # id quang cao
    id = scrapy.Field()
    # ngay dang tin
    date = scrapy.Field()
    # loai tin
    type_adv = scrapy.Field()
    # tinh trang duong truoc nha
    front_road = scrapy.Field()
    # Loại hình bất động sản
    type_real_estate = scrapy.Field()
    # Hướng cửa chính
    direction = scrapy.Field()
    # Phuong
    ward = scrapy.Field()
    # Quận
    district = scrapy.Field()
    # Tỉnh/Thành phố
    city = scrapy.Field()
    # Giấy tờ pháp lý
    property_legal_document = scrapy.Field()
    # Diện tích
    size = scrapy.Field()
    # Giá
    price = scrapy.Field()
    # Số phòng ngủ (Căn hộ/Chung cư - Nhà)
    rooms = scrapy.Field()
    # Số phòng vệ sinh (Căn hộ/Chung cư - Nhà)
    floors = scrapy.Field()
    # Chiều ngang (Nhà - Đất)
    width = scrapy.Field()
    # Chiều dài (Nhà - Đất)
    length = scrapy.Field()
