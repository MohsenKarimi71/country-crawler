from root.general_tools.tools import get_google_formatted_address_using_address, get_unique_addresses
import re

to_be_deleted_from_address = ["jalan", "jln\W+", "jl\W+"]
number_founder_pattern = "[^\d]?(\d+)[^\d]?"

def find_indonesian_addresses(text, patterns, is_contact_page=False):
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

def get_indonesian_address_parts(address, language="id"):
    return {"address":address, "components":[], "source":"company-website"}

def recheck_indonesian_address(address):
    address = re.sub('"|\(|\)', " ", address)
    m = re.search("(^address[\W]+)", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")
    
    m = re.search("(^Alamat[\W]+)", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")
    
    m = re.search("(^OFFICE[\W]+)", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")
    
    m = re.search("(^KANTOR[\W]+)", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")

    m = re.search("(postalCode[\W]+)", address, flags=re.IGNORECASE)
    if(m):
        address = address.replace(m.group(0), "")

    address = address.replace("\\n", ", ")
    address = re.sub(",\W*,", ", ", address)
    address = re.sub(" ,", ",", address)
    address = re.sub("\s{2,}", " ", address)
    return address
    
def purify_indonesian_addresses(address_list):
    '''
    get a list of indonesian addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = [recheck_indonesian_address(add) for add in address_list]

    unique_addresses = get_unique_addresses(rechecked_addresses, to_be_deleted_from_address)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_indonesian_address_parts(add))
    return splitted_addresses

def find_indonesian_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phones.append(item)
    return list(set(phones))
