from data_scraper import get_companies_data_by_method
from data_writer import CompanyDataWriter


def write_companies_data():
    with CompanyDataWriter() as writer:
        print('Scraping companies data...')
        for company_data in get_companies_data_by_method(method='yahoo'):
            writer.add_company_data(company_data)
            print('Writed data for {}'.format(company_data.get('key')))


def get_companies_data_from_db():
    with CompanyDataWriter() as reader:
        for data in reader.get_all_companies():
            print(data)


if __name__ == '__main__':
    print('You can write companies data or retrieve companies data.')
    print('Please type "1" for write data or "2" for retrieve.')
    selected_option = input()
    if selected_option == 1:
        write_companies_data()
    elif selected_option == 2:
        get_companies_data_from_db()
    else:
        SystemExit(0)
