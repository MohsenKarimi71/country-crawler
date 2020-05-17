from root.general_tools.tools import get_google_formatted_address_using_address, get_unique_addresses
import re

to_be_deleted_from_address = []
number_founder_pattern = "[^\d]?(\d+)[^\d]?"

def find_german_addresses(text, patterns, is_contact_page=False):
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
    print("found_addresses >>> ", found_addresses)
    return list(set(found_addresses))

def get_german_address_parts(address, language="de"):
    return {"address":address, "components":[], "source":"company-website"}

def recheck_german_addresses(address):
    digits = re.sub("\D", "", address)
    if(len(digits) > len(address)/2):
        return None
    if("..." in address):
        return None
    
    m = re.search("Telefon", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[0]
    
    m = re.search("Phone", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[0]
    
    m = re.search("Tel\W", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[0]
    
    m = re.search("\WFon\W", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[0]
    
    m = re.search("Fax\W", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[0]
    
    m = re.search("(E-Mail)|(email)", address, flags=re.IGNORECASE):
    if(m):
        address = address.split(m.group(0))[0]

    m = re.search("(Germany)|(Deutschland)", address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[0] + ", " + m.group(0)
    
    #m = re.search("GmbH", address, flags=re.IGNORECASE)
    #if(m):
    #    address = address.split(m.group(0))[1]
    
    ptr = "(address\s?:)|(address\s*\n)|(Adresse\s?:)|(Adresse\s*\n)|(office\s?:)|(office\s*\n)|(Büro\s?:)|(Büro\s*\n)|(Headquarter\s?:)|(Headquarter\s*\n)|(Hauptquartier\s?:)|(Hauptquartier\s*\n)"
    m = re.search(ptr, address, flags=re.IGNORECASE)
    if(m):
        address = address.split(m.group(0))[1]

    address = address.replace("\\n", ", ")
    address = re.sub("•", " ", address)
    address = re.sub("\|", ", ", address)
    address = re.sub(",\W*,", ", ", address)
    address = re.sub(" ,", ",", address)
    address = re.sub("\s{2,}", " ", address)
    address = address.strip("+")
    address = address.strip()
    return address
    

def purify_german_addresses(address_list):
    '''
    get a list of german addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = []
    for add in address_list:
        rechecked_address = recheck_german_addresses(add)
        if(rechecked_address):
            rechecked_addresses.append(rechecked_address)

    unique_addresses = get_unique_addresses(rechecked_addresses, to_be_deleted_from_address)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_german_address_parts(add))
    return splitted_addresses

def find_german_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phones.append(item)
    return list(set(phones))
