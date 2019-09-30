import pytest

@pytest.fixture
def setup_app():

    print('i am root')
    # from app.config import URL
    # from app.collectors import Scraper
    # import os
    # import sys
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))