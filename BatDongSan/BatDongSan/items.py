import scrapy


class RealEstateItem(scrapy.Item):
    """
    Các thuộc tính cần thu thập
    """
    # Loại hình bất động sản
    type_real_estate = scrapy.Field()
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
    # Hướng ban công
    balconydirection = scrapy.Field()
    # Giấy tờ pháp lý
    property_legal_document = scrapy.Field()
    # Diện tích
    size = scrapy.Field()
    # Tên phân khu/Lô/Block/Tháp
    block = scrapy.Field()
    # Giá
    price = scrapy.Field()

    # Tầng số
    floornumber = scrapy.Field()
    # Loại hình căn hộ
    apartment_type = scrapy.Field()
    # Tình trạng nội thất
    furnishing_sell = scrapy.Field()
    # Đặc điểm căn hộ
    apartment_feature = scrapy.Field()

    # Số phòng ngủ (Căn hộ/Chung cư - Nhà)
    rooms = scrapy.Field()
    # Số phòng vệ sinh (Căn hộ/Chung cư - Nhà)
    toilets = scrapy.Field()

    # Tổng số tầng
    floors = scrapy.Field()
    # Loại hình nhà ở
    house_type = scrapy.Field()
    # Tình trạng nội thất
    furnishing_sell = scrapy.Field()

    # Diện tích sử dụng
    living_size = scrapy.Field()

    # Chiều ngang (Nhà - Đất)
    width = scrapy.Field()
    # Chiều dài (Nhà - Đất)
    length = scrapy.Field()
    # Loại hình đất (Nhà - Đất)
    land_type = scrapy.Field()
    # Đặc điểm nhà/đất (Nhà - Đất)
    property_road_condition = scrapy.Field()

    # Đặc điểm nhà/đất
    land_feature = scrapy.Field()
    # Đặc điểm nhà/đất
    property_back_condition = scrapy.Field()


# # Các thuộc tính cần thu thập của Căn hộ/Chung cư
# class ApartmentItem(scrapy.Item):
#     # Mã căn/ Mã căn hộ
#     unitnumber = scrapy.Field()
#     # Phường
#     ward = scrapy.Field()
#     # Quận
#     area = scrapy.Field()
#     # Tỉnh/Thành phố
#     region = scrapy.Field()
#     # Địa chỉ
#     address = scrapy.Field()
#     # Tình trạng bất động sản
#     property_status = scrapy.Field()
#     # Diện tích/m2
#     price_m2 = scrapy.Field()
#     # Hướng cửa chính
#     direction = scrapy.Field()
#     # Hướng ban công
#     balconydirection = scrapy.Field()
#     # Giấy tờ pháp lý
#     property_legal_document = scrapy.Field()
#     # Diện tích
#     size = scrapy.Field()
#     # Số phòng ngủ
#     rooms = scrapy.Field()
#     # Số phòng vệ sinh
#     toilets = scrapy.Field()
#     # Tầng số
#     floornumber = scrapy.Field()
#     # Tên phân khu/Lô/Block/Tháp
#     block = scrapy.Field()
#     # Loại hình căn hộ
#     apartment_type = scrapy.Field()
#     # Tình trạng nội thất
#     furnishing_sell = scrapy.Field()
#     # Đặc điểm căn hộ
#     apartment_feature = scrapy.Field()
#     # Giá
#     price = scrapy.Field()
#
#
# # Các thuộc tính cần thu thập của Nhà ở
# class HouseItem(scrapy.Item):
#     # Phường
#     ward = scrapy.Field()
#     # Quận
#     area = scrapy.Field()
#     # Tỉnh/Thành phố
#     region = scrapy.Field()
#     # Địa chỉ
#     address = scrapy.Field()
#     # Diện tích/m2
#     price_m2 = scrapy.Field()
#     # Hướng cửa chính
#     direction = scrapy.Field()
#     # Giấy tờ pháp lý
#     property_legal_document = scrapy.Field()
#     # Diện tích đất
#     size = scrapy.Field()
#     # Số phòng ngủ
#     rooms = scrapy.Field()
#     # Số phòng vệ sinh
#     toilets = scrapy.Field()
#     # Tổng số tầng
#     floors = scrapy.Field()
#     # Tên phân khu/Lô/Block/Tháp
#     block = scrapy.Field()
#     # Loại hình nhà ở
#     house_type = scrapy.Field()
#     # Tình trạng nội thất
#     furnishing_sell = scrapy.Field()
#     # Đặc điểm nhà/đất
#     property_road_condition = scrapy.Field()
#     # Loại hình đất
#     land_type = scrapy.Field()
#     # Diện tích sử dụng
#     living_size = scrapy.Field()
#     # Chiều ngang
#     width = scrapy.Field()
#     # Chiều dài
#     length = scrapy.Field()
#     # Giá
#     price = scrapy.Field()
#
#
# # Các thuộc tính cần thu thập của Đất
# class LandItem(scrapy.Item):
#     # Phường
#     ward = scrapy.Field()
#     # Quận
#     area = scrapy.Field()
#     # Tỉnh/Thành phố
#     region = scrapy.Field()
#     # Địa chỉ
#     address = scrapy.Field()
#     # Diện tích
#     size = scrapy.Field()
#     # Diện tích/m2
#     price_m2 = scrapy.Field()
#     # Hướng cửa chính
#     direction = scrapy.Field()
#     # Giấy tờ pháp lý
#     property_legal_document = scrapy.Field()
#     # Tên phân khu/Lô/Block/Tháp
#     block = scrapy.Field()
#     # Đặc điểm nhà/đất
#     land_feature = scrapy.Field()
#     # Đặc điểm nhà/đất
#     property_road_condition = scrapy.Field()
#     # Đặc điểm nhà/đất
#     property_back_condition = scrapy.Field()
#     # Loại hình đất
#     land_type = scrapy.Field()
#     # Chiều ngang
#     width = scrapy.Field()
#     # Chiều dài
#     length = scrapy.Field()
#     # Giá
#     price = scrapy.Field()
