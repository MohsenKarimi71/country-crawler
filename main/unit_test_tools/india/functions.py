from root.general_tools.tools import load_country_context
from root.country_tools.india.tools import recheck_indian_address, find_indian_addresses
import re


def test_address_regex_india(text, context):
    address_pattern = context["address_patterns"]
    for pattern in address_pattern:
        items = re.findall(pattern, text, flags=re.IGNORECASE)
        if(items):
            return items
        else:
            return None

def test_recheak_address_india(address):
    return recheck_indian_address(address)


def test_find_indian_addresses(text, context):
    address_pattern = context["address_patterns"]
    addresses = find_indian_addresses(text, address_pattern)
    return addresses






