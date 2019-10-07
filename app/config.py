URL = 'https://www.nhs.uk/Service-Search/Dentists/LocationSearch/3'
MY_POSTCODE = 'RH4 1JJ'
PER_PAGE = 100

# scraper config
ROW_CLASS_TO_OMIT = 'fctitles'
MAIN_ROW_COL_ORDER = ['rating', 'by_referral',
                      'new_adult', 'new_adult_entitled', 'new_children', 'urgent_nhs']
IMG_AVAIL_MAP = {'icon-yes': True,
                 'icon-no': False, 'icon-question': None}

# csv colllector config
CSV_VALUE_FOR_TRUE = 'true'
ADMISSION_CATEGORIES = {
    'by_referral': 'Value  (Accepting NHS patients by referral only)',
    'new_adult':'Value  (Accepting new adult NHS patients)',
    'new_adult_entitled': 'Value  (Accepting new adult patients entitled to free NHS dental care)',
    'new_children': 'Value  (Accepting children as new NHS patients)',
    'urgent_nhs': 'Value  (Urgent NHS dental appointments)',
}