from root.general_tools.tools import get_google_formatted_address_using_address, get_unique_addresses
import re

to_be_deleted_from_address = []
number_founder_pattern = "[^\d]?(\d+)[^\d]?"

def find_Colombian_addresses(text, patterns, is_contact_page=False):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        if(items):
            for item in items:
                # cleaning addresses
                add = re.sub("\n", " ", item[0])
                add = add.strip()
                add = re.sub("\s{2,}", " ", add)
                found_addresses.append(add)
    return list(set(found_addresses))

def get_Colombian_address_parts(address, language="es"):
    return {"address":address, "components":[], "source":"company-website"}

def recheck_Colombian_address(address):
    address = re.sub("(Dirección[\W]*)|(Dirc[\W]*)", "", address, flags=re.IGNORECASE)
    return address.strip()

def purify_Colombian_addresses(address_list):
    '''
    get a list of Colombian addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = [recheck_Colombian_address(add) for add in address_list]
    unique_addresses = get_unique_addresses(rechecked_addresses, to_be_deleted_from_address)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_Colombian_address_parts(add))
    return splitted_addresses

def find_Colombian_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phones.append(item)
    return list(set(phones))
