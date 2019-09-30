URL = 'https://www.nhs.uk/Service-Search/Dentists/LocationSearch/3'
POSTCODE = 'RH4 1JJ'
PER_PAGE = 100

# scraper config
ROW_CLASS_TO_OMIT = 'fctitles'
MAIN_ROW_COL_ORDER = ['rating', 'by_referral',
                      'new_adult', 'new_adult_entitled', 'new_children', 'urgent_nhs']
IMG_AVAIL_MAP = {'icon-yes': True,
                 'icon-no': False, 'icon-question': None}