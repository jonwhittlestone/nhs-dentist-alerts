#!/usr/bin/env python

from .config import *
from .collectors import Scraper
from .utils import empty_dentist, Dentist


print('==================')
print('NHS Dentist Alerts')
print('==================')


def extract_dentists_scraper():
    s = Scraper(URL, ROW_CLASS_TO_OMIT)
    browser = s.connect()
    results_page = s.search_postcode(browser, POSTCODE, per_page=PER_PAGE)
    results_table = s.results_table
    all_dentists, extracted = s.extract_dentists()
    return all_dentists, extracted

def print_results(extracted: list):
    print(f'Found {len(extracted)} results:')
    for d in extracted:
        print('-------------------')
        print(d)
        print('')
        print('')

    print(f'Found {len(extracted)} results.')


def main():
    all_dentists, extracted = extract_dentists_scraper()
    # all_dentists, extracted = extract_dentists_csv()
    # results_page = s.update_search_per_page(PER_PAGE)

    print_results(extracted)



if __name__ == '__main__':
    main()
