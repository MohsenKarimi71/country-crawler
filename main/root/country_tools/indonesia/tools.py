from root.general_tools.tools import get_google_formatted_address_using_address
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

def get_indonesian_unique_addresses(address_list):
    unique_addresses = []
    if(len(address_list) > 1):
        filtered_add_list = [add.lower() for add in address_list]

        for index, add in enumerate(filtered_add_list):
            # deleting common words
            for phrase in to_be_deleted_from_address:
                add = add.replace(phrase, " ")

            # splitting addresses on space
            splitted_list = add.split(" ")

            # extracting all numbers
            word_list = []
            for word in splitted_list:
                m = re.search(number_founder_pattern, word)
                if(m):
                    word_list.append(m.group(1))
                    word = word.replace(m.group(0), " ")
                word = (re.sub("\s{2,}", " ", word)).strip()
                if(not word.endswith(".")):
                    if(len(word) >= 2):
                        word_list.append(word)
            word_list = list(set(word_list))
            filtered_add_list[index] = word_list
        # getting unique addresses
        max_length = 0
        max_index = 0
        for i in range(len(filtered_add_list)):
            if(len(filtered_add_list[i]) > max_length):
                max_length = len(filtered_add_list[i])
                max_index = i
        unique_addresses.append({"original":address_list[max_index], "splitted":filtered_add_list[max_index]})
        for index1, splitted_list in enumerate(filtered_add_list):
            if(len(splitted_list) > 0):
                is_unique = True
                if(index1 != max_index):
                    add_results = {"original":address_list[index1], "splitted":splitted_list}
                    for index2, unq_dic in enumerate(unique_addresses):
                        if(len(unq_dic["splitted"]) > len(splitted_list)):
                            score = 0
                            for word in splitted_list:
                                if(word in unq_dic["splitted"]):
                                    score += 1
                            if(score / len(splitted_list)) > 0.6:
                                unique_addresses[index2]["splitted"] = list(set(unique_addresses[index2]["splitted"] + splitted_list))
                                is_unique = False
                                break
                        else:
                            score = 0
                            for word in unq_dic["splitted"]:
                                if(word in splitted_list):
                                    score += 1
                            if(score / len(unq_dic["splitted"])) > 0.6:
                                unique_addresses[index2]["splitted"] = list(set(unique_addresses[index2]["splitted"] + splitted_list))
                                unique_addresses[index2]["original"] = address_list[index1]
                                is_unique = False
                                break
                    if(is_unique):
                        unique_addresses.append(add_results)
            
        unique_addresses = [dic["original"] for dic in unique_addresses]
        return unique_addresses
    else:
        return address_list

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

    unique_addresses = get_indonesian_unique_addresses(rechecked_addresses)

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

def purify_indonesian_phones(phone_list):
    '''
    This function takes a list of phone numbers as input, extracts all unique 
    phone numbers from input list and finally return a list of unique phone numbers.
    '''
    if(phone_list):
        if(len(phone_list) == 1):
            return phone_list
        else:
            unique_phones = []
            filtered_list = [re.sub("[\D]", "", phone)[-10:] for phone in phone_list]

            unique_phones.append({"original": phone_list[0], "filtered":filtered_list[0]})
            for i in range(1, len(phone_list)):
                is_unique = True
                for dic in unique_phones:
                    if(filtered_list[i] == dic["filtered"]):
                        is_unique = False
                        break
                if(is_unique):
                    unique_phones.append({"original": phone_list[i], "filtered":filtered_list[i]})
            return [dic["original"] for dic in unique_phones]
    else:
        return []

