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
        session.reset()

    def run_parse(self):
        self.parsed_data = BeautifulSoup(self.html_body, "lxml")

    def get_parsed_data(self):
        self.run_scrape()
        self.run_parse()
        return self.parsed_data

def get_companies_by_method(method):
    if method=='yahoo':
        yahoo_scraper = YahooFinanceScraper()
        return yahoo_scraper.get_companies()
    else:
        raise NotImplementedError


class YahooFinanceScraper(object):
    JDI_url = "https://finance.yahoo.com/quote/%5EDJI/components?p=%5EDJI"
    JDI_companies_css_class = "C($actionBlue) Cur(p) Td(u)"
    profile_url_pattern = "https://finance.yahoo.com/quote/{company_key}/profile?p={company_key}"
    analists_url_pattern = "https://finance.yahoo.com/quote/{company_key}/analysts?p={company_key}"

    def get_companies(self):
        scraper = ScraperEngine(YahooFinanceScraper.JDI_url)
        self.soup_data = scraper.get_parsed_data()
        companies = []
        if self.soup_data:
            companies = [company_tag.get('title')
                         for company_tag in self.soup_data.findAll(class_=YahooFinanceScraper.JDI_companies_css_class)]
        self.companies_data = {}
        for company_key in companies:
            self.companies_data[company_key] = self._get_company_data(company_key, scraper)
        return self.companies_data

    def _get_company_data(self, company_key, scraper):
        scraper.url = YahooFinanceScraper.profile_url_pattern.format(company_key=company_key)
        self.soup_data = scraper.get_parsed_data()
        left_block_data = self._get_profile_block_data(
            block_class="D(ib) W(47.727%) Pend(40px)",
            block_keys =('street', 'city', 'country', 'phone', 'url')
        )
        right_block_data = self._get_profile_block_data(
            block_class="D(ib) Va(t)",
            block_keys =('sector', 'industry', 'employees_count')
        )
        company_data = {
            'name': '',
            'est_revenue': '',
            'url': '',
            'street': '',
            'city': '',
            'zip_code': '',
            'country': '',
            'employees_count': 0,
            'industry': ''
        }
        company_data['name'] = self.soup_data.find(class_="Mb(10px)").get_text()
        company_data['est_revenue'] = self._get_est_revenue(company_key, scraper)
        company_data.update(left_block_data)
        company_data.update(right_block_data)
        company_data['zip_code'] = company_data['city'][-5:]
        company_data['employees_count'] = int(company_data['employees_count'].replace(',', '')
            ) if company_data['employees_count'] else ''
        company_data['city'] = company_data['city'].replace(company_data['zip_code'], '').strip()
        company_data['key'] = company_key
        return company_data

    def _get_profile_block_data(self, block_class, block_keys):
        parsed_block_data = []

        for data_row in self.soup_data.find(class_=block_class):
            if ('react-text' in data_row or
                '<br/>' in str(data_row) or
                data_row == ': ' or
                str(data_row) in ['<span>Sector</span>', '<span>Industry</span>', '<span>Full Time Employees</span>']):
                continue
            if not isinstance(data_row, basestring):
                data_row = data_row.get_text()
            parsed_block_data.append(data_row)
        return dict(zip(block_keys, parsed_block_data))

    def _get_est_revenue(self, company_key, scraper):
        scraper.url = YahooFinanceScraper.analists_url_pattern.format(company_key=company_key)
        self.soup_data = scraper.get_parsed_data()
        return self.soup_data.find(text="Revenue Estimate").findNext(
            text="Avg. Estimate"
        ).findNext('td').findNext('td').findNext('td').get_text()
