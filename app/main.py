#!/usr/bin/env python
from dataclasses import dataclass
import mechanicalsoup

URL = 'https://www.nhs.uk/Service-Search/Dentists/LocationSearch/3'
ROW_CLASS_TO_OMIT = 'fctitles'
POSTCODE = 'RH4 1JJ'
PER_PAGE = 100
MAIN_ROW_COL_ORDER = ['rating', 'by_referral',
                      'new_adult', 'new_adult_entitled', 'new_children', 'urgent_nhs']
IMG_AVAIL_MAP = {'icon-yes': True,
                 'icon-no': False, 'icon-question': None}


print('==================')
print('NHS Dentist Alerts')
print('==================')

def empty_dentist():
    d = Dentist(name='', address_contact='', distance='', by_referral=None,
                new_adult=None, new_adult_entitled=None, new_children=None, urgent_nhs=None, all_null=True)
    for hdg in MAIN_ROW_COL_ORDER:
        setattr(d, hdg, None)
    return d



def strip_newline(value):
    return value.replace('\n', ' ').replace('\r', ' ').strip()

@dataclass
class Dentist:
    '''Extracted, cleaned Dentist from results table'''
    name: str
    address_contact: str
    distance: str
    by_referral: bool
    new_adult: bool
    new_adult_entitled: bool
    new_children: bool
    urgent_nhs: bool

    all_null: bool

    def __str__(self):
        return f"Name:\t\t\t\t{self.name}" \
            f"\nAddress:\t\t\t{self.address_contact}" \
            f"\nBy Referral Only:\t\t{self.by_referral}" \
            f"\nNew Adult Only:\t\t\t{self.new_adult}" \
            f"\nNew NHS Entitled Adult Only:\t{self.new_adult_entitled}" \
            f"\nNew Children:\t\t\t{self.new_children}" \
            f"\nUrgent NHS Treatments:\t\t{self.urgent_nhs}"


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

    def connect(self, per_page=None):
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='MyBot/0.1: mysite.example.com/bot_info',
        )
        browser.open(URL)
        return browser
    
    def search_postcode(self, browser, postcode, per_page):
        '''Search the form to give back results'''
        browser.select_form('.findcompare-search form')
        # Submit search - 25 default per_page
        browser['Location.Name'] = POSTCODE
        resp = browser.submit_selected()


        # Todo.
        # if per_page:
            # update form per_page input
            # browser.select_form('.findcompare-search form')

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

    def td_contains_result_icon(self, td, new_dentist):
        '''
            Determine 'Yes,'No, N/A' from img
            eg. <img src="..yes.png">
        '''
        try:
            for c in td.contents:
                for k, v in IMG_AVAIL_MAP.items():
                    if k in str(c):
                        return v, new_dentist
        except Exception:
            pass
        return None, new_dentist


    def extract_dentists(self):
        '''clean, return data'''
        all_results = []
        cleaned_results = []
        rows = self.results_table.select(f'tr:not(.{ROW_CLASS_TO_OMIT})')
        new_dentist = empty_dentist()
        for row_count, row in enumerate(rows):
            if row_count % 2 == 0:  # if odd, then start a new
                new_dentist = empty_dentist()
                td_cells = row.select('tr>th.fctitle')
                new_dentist.name = strip_newline(td_cells[0].text)
                continue
            else:
                td_cells = row.select('tr>td')
                for td_count, td in enumerate(td_cells):
                    for adm in MAIN_ROW_COL_ORDER:
                        availability, new_dentist = self.td_contains_result_icon(td, new_dentist) 
                        setattr(new_dentist, adm, availability)
                        if (availability is not None):
                            new_dentist.all_null = False

                    # now get the address from the first column
                    if td_count == 0:
                        new_dentist.address_contact = strip_newline(td.get_text())
                # Capture results, unless all empty
                all_results.append(new_dentist)
                if not new_dentist.all_null:
                    cleaned_results.append(new_dentist)
        return all_results, cleaned_results


def main():
    s = Scraper(URL)
    browser = s.connect()
    results_page = s.search_postcode(browser, POSTCODE, per_page=PER_PAGE)
    results_table = s.results_table
    # results_page = s.update_search_per_page(PER_PAGE)
    all_dentists, extracted = s.extract_dentists()

    print(f'Found {len(extracted)} results:')
    for d in extracted:
        print('-------------------')
        print(d)
        print('')
        print('')

    print(f'Found {len(extracted)} results.')



if __name__ == '__main__':
    main()
