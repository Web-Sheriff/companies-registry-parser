import scrapy
from pymongo import MongoClient


class CompanySpider(scrapy.Spider):
    name = "company"
    core_site = "https://www.difc.ae"
    query1 = 'https://www.difc.ae/public-register/?companyName=&registrationNo=&status=&type=&sortBy=&page='
    query2 = '&isAjax=true'
    counter = 1
    cluster = MongoClient(
        "mongodb+srv://dbUser:dbUserPassword@cluster1.du6xm.mongodb.net/com_registry?retryWrites=true&w=majority")
    db = cluster["com_registry"]
    collection = db['companies']

    def start_requests(self):
        yield scrapy.Request(f'{self.query1}{self.counter}{self.query2}', callback=self.basic_parser)

    def basic_parser(self, response, **kwargs):
        field = {}
        for div_i in range(1, len(response.xpath("//div[@class='wrap']")) + 1):
            company = response.xpath(f'/html/body/div[{div_i}]/h4/a/text()').get()
            location = response.xpath(f'/html/body/div[{div_i}]/div/div[2]/p').get()
            location = location.split('</span>')[1][:-4].replace('\u00a0', '').strip() if location else None
            status = response.xpath(f'/html/body/div[{div_i}]/div/div[1]/p[1]/text()').get()
            reg_number = response.xpath(f'/html/body/div[{div_i}]/div/div[1]/p[2]/text()').get()
            reg_number = int(reg_number.split('#')[1].strip()) if reg_number else None
            license_n = response.xpath(f'/html/body/div[{div_i}]/div/div[1]/p[3]/text()').get()

            field = {'company': company,
                     'location': location,
                     'status': status,
                     'reg_number': reg_number,
                     'license': license_n}
            self.collection.insert_one(field)
            yield field

        if field:
            self.logger.info(f'COMPANIES PACK #{self.counter} PROCESSED')
            self.counter += 1
            yield scrapy.Request(f'{self.query1}{self.counter}{self.query2}', callback=self.basic_parser)

    def advanced_parser(self, response):
        company_view = ''
        for div_i in range(1, len(response.xpath("//div[@class='wrap']")) + 1):
            company_view = response.xpath(f'/html/body/div[{div_i}]/div/div[4]/a/@href').get()
            yield scrapy.Request(f'{self.core_site}{company_view}', callback=self.sub_parser)

        if company_view:
            self.logger.info(f'COMPANIES PACK #{self.counter} PROCESSED')
            self.counter += 1
            yield scrapy.Request(f'{self.query1}{self.counter}{self.query2}', callback=self.advanced_parser)

    def sub_parser(self, response):
        total_items = len(response.xpath("//div[@class='col-sm-6 left']/div[@class='row']"))
        top_items = len(response.xpath(
            "//div[@class='register-top']/div[@class='container']/div[@class='row']\
            /div[@class='col-sm-6 left']/div[@class='row']"))
        bot_items = total_items - top_items
        field = {}

        for div_i in range(1, bot_items + 1):
            key = response.xpath(
                f'/html/body/div[1]/div[9]/div[2]/div[2]/div/div[1]/div[{div_i}]/div[1]/p/strong/text()').get().split(
                ':')[0].strip()
            value = response.xpath(
                f'/html/body/div[1]/div[9]/div[2]/div[2]/div/div[1]/div[{div_i}]/div[2]/p/text()').get()
            field[key] = value

        yield field
