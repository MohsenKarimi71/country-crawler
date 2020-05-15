from root.general_tools.tools import get_google_formatted_address_using_address, get_unique_addresses
import re

to_be_deleted_from_address = []

def find_korean_addresses(text, patterns, is_contact_page=False):
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

def get_korean_address_parts(address, language="th"):
    return {"address":address, "components":[], "source":"company-website"}

def recheck_korean_addresses(address):
    digits = re.sub("\D", "", address)
    if(len(digits) > len(address)/2):
        return None

    if(re.search("^\d{5}[\w\W]+\d{5}$", address)):
        return None

    m = re.search("address\W+", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[1]

    m = re.search("주소\W+", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[1]
    
    m = re.search("office\W+", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[1]
    
    address = address.replace("\\n", ", ")
    address = re.sub(",\W*,", ", ", address)
    address = re.sub(" ,", ",", address)
    address = re.sub("\s{2,}", " ", address)
    return address

def purify_korean_addresses(address_list):
    '''
    get a list of korean addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = []
    for add in address_list:
        rechecked_address = recheck_korean_addresses(add)
        if(rechecked_address):
            rechecked_addresses.append(rechecked_address)

    unique_addresses = get_unique_addresses(rechecked_addresses, to_be_deleted_from_address)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_korean_address_parts(add))
    return splitted_addresses

def find_korean_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phones.append(item)
    return list(set(phones))