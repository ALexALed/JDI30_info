import dryscrape
from bs4 import BeautifulSoup


class ScraperEngine(object):

    def __init__(self, url):
        self.url = url
        self.html_body = ''
        self.parsed_data = None

    def run_scrape(self):
        session = dryscrape.Session()
        session.visit(self.url)
        self.html_body = session.body()

    def run_parse(self):
        self.parsed_data = BeautifulSoup(self.html_body, "lxml")

    def get_parsed_data(self):
        self.run_scrape()
        self.run_parse()
        return self.parsed_data


class YahooFinanceScraper(object):
    profile_url_pattern = "https://finance.yahoo.com/quote/{company_key}/profile?p={company_key}"
    JDI_url = "https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
    JDI_companies_css_class = "C($actionBlue) Cur(p) Td(u)"

    def get_companies(self):
        print(YahooFinanceScraper.JDI_url)
        scraper = ScraperEngine(YahooFinanceScraper.JDI_url)
        self.soup_data = scraper.get_parsed_data()
        companies = []
        if self.soup_data:
            companies = [company_tag.get('title')
                         for company_tag in self.soup_data.findAll(class_=YahooFinanceScraper.JDI_companies_css_class)]
        print(companies)
        self.companies_data = {}
        for company_key in companies:
            scraper.url = YahooFinanceScraper.profile_url_pattern.format(company_key=company_key)
            self.soup_data = scraper.get_parsed_data()
            self.companies_data[company_key] = self.get_company_data()

    def get_company_data(self):
        address_data = self.get_company_address()
        company_data_keys = {
            'name': '',
            'est_revenue': 0,
            'url': '',
            'street': '',
            'city': '',
            'zip_code': '',
            'country': '',
            'employees_count': 0,
            'industry': ''
        }

    def get_company_address(self):
        for address_row in self.soup_data.find(class_="D(ib) W(47.727%) Pend(40px)"):
            print(address_row)
