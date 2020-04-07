from root.general_tools.tools import load_country_context
from root.country_tools.india.tools import recheck_indian_address, find_indian_addresses, find_indian_phones, get_indian_address_parts
import re


def test_address_regex_india(text, context):
    address_pattern = context["address_patterns"]
    for pattern in address_pattern[1:]:
        items = re.findall(pattern, text, flags=re.IGNORECASE)
        if(items):
            return items
        else:
            return None

def test_recheak_address_india(address):
    return recheck_indian_address(address)

def test_find_indian_addresses(text, context, is_contact_page=False):
    address_pattern = context["address_patterns"]
    addresses = find_indian_addresses(text, address_pattern, is_contact_page=is_contact_page)
    return addresses

def test_find_indian_phones(text, context):
    phone_patterns = context["phone_patterns"]
    phones = find_indian_phones(text, phone_patterns)
    return phones

def test_get_indian_address_parts(address):
    return get_indian_address_parts(address, language="en")

