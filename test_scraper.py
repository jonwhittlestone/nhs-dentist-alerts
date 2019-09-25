import os
from pytest import fixture
from app.main import (Scraper, URL, POSTCODE, PER_PAGE, ROW_CLASS_TO_OMIT)

class TestScraper:
    @fixture
    def scraper(self):
        return Scraper(URL)

    @fixture
    def browser(self, scraper):
        return scraper.connect()

    @fixture
    def results_page(self, scraper, browser):
        return scraper.search_postcode(browser, POSTCODE)

    def test_i_can_see_a_results_page(self, results_page):
        h1 = results_page.select('h1')
        assert len(h1) > 0
        try:
            assert POSTCODE in h1[0].text
        except AssertionError as e:
            assert False

    def test_i_can_extract_a_results_table(self, scraper, results_page):
        '''test the extracted table has 1 or more rows'''
        table_wrapper = scraper.results_table
        content_rows = table_wrapper.select(f'tr:not(.{ROW_CLASS_TO_OMIT})')
        try:
            assert len(content_rows) > 0
        except Exception as e:
            assert False

    def test_i_can_get_headings(self, scraper, results_page):
        table_wrapper = scraper.results_table
        assert len(scraper.table_headings) > 0

    def test_i_can_extract_a_result_row_to_a_data_class(self, scraper, results_page):
        extracted = scraper.extract_dentists()
        dentist_data_class = extracted[0]
        
        # arrange first result of table cells to
        # match to dataclass
        rows = scraper.results_table.select(f'tr:not(.{ROW_CLASS_TO_OMIT})')
        first_row = rows[0]
        td_cells = first_row.select('tr>th.fctitle')
        name_cell = td_cells[0]
        assert dentist_data_class.name in name_cell.text.replace('\n','')
