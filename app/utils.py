from config import *
from dataclasses import dataclass

def empty_dentist():
    d = Dentist(name='', address_contact='', distance='', by_referral=None,
                new_adult=None, new_adult_entitled=None, new_children=None, urgent_nhs=None, all_null=True)
    for hdg in MAIN_ROW_COL_ORDER:
        setattr(d, hdg, None)
    return d

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



def strip_newline(value):
    return value.replace('\n', ' ').replace('\r', ' ').strip()
