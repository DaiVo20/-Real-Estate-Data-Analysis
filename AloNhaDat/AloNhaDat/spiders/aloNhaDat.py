import scrapy
from scrapy import Spider
from AloNhaDat.items import AlonhadatItem
from datetime import date, timedelta

today = date.today().strftime("%d/%m/%Y")
yesterday = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")

class AloNhaDatSpider(Spider):
    name = "AloNhaDat"
    allowed_domains = ["alonhadat.com.vn"]
    start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban.html"]
    base_url = "https://alonhadat.com.vn/nha-dat/can-ban/trang--{}.html"
    total_page = 2

    def parse(self, response):
        ads_urls = response.xpath("//div[@class='ct_title']/a/@href").getall()
        for i in ads_urls:
            current_url = "https://alonhadat.com.vn" + i
            yield response.follow(current_url, callback=self.parse_item)
        for page in range(2, self.total_page + 1):
            yield response.follow(self.base_url.format(page), callback=self.parse)


    def parse_item(self, response):
        item = AlonhadatItem()

        date = response.xpath("//div[@class='title']/span[@class='date']/text()").get()
        ls_date = date.split(': ')
        if ls_date[1] == 'Hôm nay':
            item['date'] = today
        elif ls_date[1] == 'Hôm qua':
            item['date'] = yesterday
        else:
            item['date'] = ls_date[1]

        item['price'] = response.xpath("//span[@class='price']/span[@class='value']/text()").get()
        item['size'] = response.xpath("//span[@class='square']/span[@class='value']/text()").get()
        
        address = response.xpath("//div[@class='address']/span[@class='value']/text()").get()
        ls_add = address.split(', ')
        item['city'] = ls_add[-1]
        item['district'] = ls_add[-2]
        try:
            item['ward'] = ls_add[-3]
        except:
            item['ward'] = ''


        item['id'] = response.xpath("//div[@class='infor']/table/tr[1]/td[2]/text()").get()
        item['direction'] = response.xpath("//div[@class='infor']/table/tr[1]/td[4]/text()").get()
        item['type_adv'] = response.xpath("//div[@class='infor']/table/tr[2]/td[2]/text()").get()
        item['front_road'] = response.xpath("//div[@class='infor']/table/tr[2]/td[4]/text()").get()
        item['type_real_estate'] = response.xpath("//div[@class='infor']/table/tr[3]/td[2]/text()").get()
        item['property_legal_document'] = response.xpath("//div[@class='infor']/table/tr[3]/td[4]/text()").get()
        item['width'] = response.xpath("//div[@class='infor']/table/tr[4]/td[2]/text()").get()
        item['floors'] = response.xpath("//div[@class='infor']/table/tr[4]/td[4]/text()").get()
        item['length'] = response.xpath("//div[@class='infor']/table/tr[5]/td[2]/text()").get()
        item['rooms'] = response.xpath("//div[@class='infor']/table/tr[5]/td[4]/text()").get()

        yield item

class HCMSpider(AloNhaDatSpider):
    name = "AloHCM"
    start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/2/ho-chi-minh.html"]
    base_url = "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/2/ho-chi-minh/trang--{}.html"
    total_page = 5705

class BDpider(AloNhaDatSpider):
    name = "AloBD"
    start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/14/binh-duong.html"]
    base_url = "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/14/binh-duong/trang--{}.html"
    total_page = 215

class DNSpider(AloNhaDatSpider):
    name = "AloDN"
    start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/23/dong-nai.html"]
    base_url = "https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/23/dong-nai/trang--{}.html"
    total_page = 500

