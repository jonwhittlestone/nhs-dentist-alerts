
from pytest import fixture
from app.collectors import CsvCollector
from app.config import (
    URL, MY_POSTCODE, ADMISSION_CATEGORIES, CSV_VALUE_FOR_TRUE)
import pandas as pd


class TestCsvCollector:
    '''Test Reading and extracting of the NHS Dentist CSV'''

    @fixture
    def csv_collector(self):
        return CsvCollector(URL)

    @fixture
    def browser(self, csv_collector):
        return csv_collector.connect()

    @fixture
    def results_page(self, csv_collector, browser):
        return csv_collector.search_postcode(browser, MY_POSTCODE)

    @fixture 
    def csv(self, csv_collector, browser):
        ctr = csv_collector
        csv_url = ctr.csv_url
        return ctr.download_csv(csv_url)

    def test_csv_is_downloaded_to_dataframe(self, csv_collector, browser, results_page, csv):
        df = csv_collector.listlist_to_df(csv)
        assert df.empty == False
    
    def test_values_for_matching_admission_category_are_true(self, csv_collector, browser, results_page, csv):
        cat = ADMISSION_CATEGORIES
        df = csv
        subset_df = csv_collector.admissions(df)

        desired_category = 'new_children'
        admission_filter = cat[desired_category]
        # filter dataframe to desired admission_category
        filtered = subset_df[
            df[admission_filter] == CSV_VALUE_FOR_TRUE
        ]
        col_true_values = list(filtered[admission_filter])

        # assert all equal and match the string constant
        assert col_true_values[1:] == col_true_values[:-1]
        assert col_true_values[0] == CSV_VALUE_FOR_TRUE
