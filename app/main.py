#!/usr/bin/env python
from dataclasses import dataclass
import mechanicalsoup

URL = 'https://www.nhs.uk/Service-Search/Dentists/LocationSearch/3'
ROW_CLASS_TO_OMIT = 'fctitles'
POSTCODE = 'RH4 1JJ'
PER_PAGE = 100


print('==================')
print('NHS Dentist Alerts')
print('==================')

def empty_dentist():
    return Dentist(name='',address='',distance='')


def strip_newline(value):
    return value.replace('\n', ' ').replace('\r', ' ').strip()

@dataclass
class Dentist:
    '''Extracted, cleaned Dentist from results table'''
    name: str
    address: str
    distance: str


class Scraper:

    def __init__(self, url):
        self.url = url
        self.results_page = ''

    @property
    def results_table(self):
        return self._results_table

    @results_table.setter
    def results_table(self, value):
        self._results_table = value

    def connect(self):
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='MyBot/0.1: mysite.example.com/bot_info',
        )
        browser.open(URL)
        return browser
    
    def search_postcode(self, browser, postcode):
        '''Search the form to give back results'''
        browser.select_form('.findcompare-search form')
        # Submit search - 25 default per_page
        browser['Location.Name'] = POSTCODE
        resp = browser.submit_selected()

        self.results_page = browser.get_current_page()
        return self.results_page

    @property
    def results_table(self):
        try:
            self._results_table = self.results_page.select('table.list-view')[0]
            return self._results_table
        except Exception as e:
            pass
    
    @property
    def table_headings(self) -> list:
        headings = self.results_table.select('th h2')
        return [h.text for h in headings]

    def update_search_per_page(self, results_page, PER_PAGE):
        return results_page

    def extract_dentists(self):
        '''clean, return data'''
        cleaned_results = []
        rows = self.results_table.select(f'tr:not(.{ROW_CLASS_TO_OMIT})')
        new_dentist = empty_dentist()
        for count, row in enumerate(rows):
            if count % 2 == 0:  # if odd, then start a new
                new_dentist = empty_dentist()
                td_cells = row.select('tr>th.fctitle')
                new_dentist.name = strip_newline(td_cells[0].text)
                continue
            else:
                td_cells = row.select('tr>td')
                for count, td in enumerate(td_cells):
                    if count == 0:
                        new_dentist.address = strip_newline(td.get_text())
                    cleaned_results.append(new_dentist)
        return cleaned_results


def main():
    s = Scraper(URL)
    browser = s.connect()
    results_page = s.search_postcode(browser, POSTCODE)
    results_table = s.results_table
    # results_page = s.update_search_per_page(PER_PAGE)
    extracted = s.extract_dentists()

    for d in extracted:
        print('-------------------')
        print(d)
        print('')
        print('')




if __name__ == '__main__':
    main()
