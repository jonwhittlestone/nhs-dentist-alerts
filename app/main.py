#!/usr/bin/env python
from dataclasses import dataclass
import mechanicalsoup

URL = 'https://www.nhs.uk/Service-Search/Dentists/LocationSearch/3'
ROW_CLASS_TO_OMIT = 'fctitles'
POSTCODE = 'RH4 1JJ'
cleaned_results = []


@dataclass
class Dentist:
    '''Extracted, cleaned Dentist from results table'''
    name: str
    address: str
    distance: str

def empty_dentist():
    return Dentist(name='',address='',distance='')

def main():

    qs_args = {
        'proximity_miles':'distance',
        'per_page':'ResultsOnPageValue'
    }

    print('==================')
    print('NHS Dentist Alerts')
    print('==================')

    #1. Set up browser
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )
    browser.open(URL)
    browser.select_form('.findcompare-search form')
    # Submit search - 25 default per_page
    browser['Location.Name'] = POSTCODE
    resp = browser.submit_selected()

    results_page = browser.get_current_page()
    results_table = results_page.select('table.list-view')[0]
    headings = results_table.select('th h2')
    headings = [h.text for h in headings]

    rows = results_table.select('tr:not(.fctitles)')
    # filter to just info rows and not heading row

    # clean, gather results
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

        for d in cleaned_results:
            print('-------------------')
            print(d)
            print('')
            print('')
def strip_newline(value):
    return value.replace('\n', '').replace('\r', '')



if __name__ == '__main__':
    main()
