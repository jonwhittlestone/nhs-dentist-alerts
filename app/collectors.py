import csv
import requests
import io
import mechanicalsoup
import pandas as pd

from config import *
from utils import empty_dentist, Dentist, strip_newline


class Scraper:

    def __init__(self, url, row_class_to_omit):
        self.url = url
        self.results_page = ''
        self.row_class_to_omit = row_class_to_omit

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
        browser.open(self.url)
        return browser
    
    def search_postcode(self, browser, postcode, per_page):
        '''Search the form to give back results'''
        browser.select_form('.findcompare-search form')
        # Submit search - 25 default per_page
        browser['Location.Name'] = postcode
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
        rows = self.results_table.select(f'tr:not(.{self.row_class_to_omit})')
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

class CsvCollector:



    def __init__(self, url):
        self.url = url

    def connect(self):
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={'features': 'lxml'},
            raise_on_404=True,
            user_agent='MyBot/0.1: mysite.example.com/bot_info',
        )
        browser.open(self.url)
        return browser

    def search_postcode(self, browser, postcode):
        '''Search the form to give back results'''
        browser.select_form('.findcompare-search form')
        # Submit search - 25 default per_page
        browser['Location.Name'] = postcode
        resp = browser.submit_selected()
        self.search_form_results_url = resp.url
        return browser.get_current_page()

    @property
    def web_url(self):
        return self.search_form_results_url

    @property
    def csv_url(self):
        search = '/Results/'
        replace = '/Export/'
        return self.web_url.replace(search,replace)
    

    def results_to_export_url(self):
        return ''

    def download_csv(self, url):
        s=requests.get(url).content
        return pd.read_csv(io.StringIO(s.decode('utf-8')))

        # header uses numbered header cols
        # with requests.Session() as s:
        #     download = s.get(url)
        #     decoded_content = download.content.decode('utf-8')
        #     cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        #     sheet = list(cr)
        return sheet

    def listlist_to_df(self, sheet: list):
        from pandas import DataFrame
        self.df = DataFrame.from_records(sheet)
        return self.df
    
    def headers(self):
        rows_df = self.df.transpose()
        self.headers = [h for h in rows_df[0]]
        return self.headers

    def admissions(self, df):
        '''
            Returns a dataframe with contact details
            and admission categories
        '''
        cat = ADMISSION_CATEGORIES
        return df[[
            'Organisation Name', 
            'PostCode', 
            'Telephone Number', 
        ]
            + list(cat.values())
        ]
