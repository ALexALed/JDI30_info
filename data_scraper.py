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
        self.parsed_data = BeautifulSoup(self.html_body)

    def get_parsed_data(self):
        if self.url and not self.parsed_data:
            self.run_parse()
            self.run_scrape()
        return self.parsed_data


class YahooFinanceScraper(object):
    profile_url_pattern = "quote/{company_key}/profile?p={company_key}"
    JDI_url = "https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
    JDI_companies_css_class = "C($actionBlue) Cur(p) Td(u)"

    def get_companies(self):
        scraper = self.ScraperEngine(JDI_companies_css_class)
        soup_data = scraper.get_parsed_data()
        companies = []
        if soup_data:
            companies = [company_tag.get('title')
                         for company_tag in soup_data.findAll(class=JDI_companies_css_class)]

        self.companies_data = {}
        for company_key in self.companies_data:
            self.companies_data[company_key] = get_company_data(profile_url_pattern.format(company_key=company_key))

    def get_company_data(self, url):
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
        for address_row in parsed_data.find(class_="D(ib) W(47.727%) Pend(40px)"):
            pass
