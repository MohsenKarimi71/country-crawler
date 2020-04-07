from root.general_tools.tools import get_google_formatted_address_using_address
import re

# VARIABLES
to_be_deleted_from_address = ["Floor", "No\.", "Office"]
number_founder_pattern = "[^\d]?(\d+)[^\d]?"

indian_address_end_pattern1 = [
                                "(" +
                                    "(india)|" +
                                    "((?<!\d)\d{3}[\s\-\.]?\d{3}(?!\d))|" + 
                                    "(Andhra Pradesh)|(Arunachal Pradesh)|(Assam)|(Bihar)|(Chhattisgarh)|(Goa)|(Gujarat)|(Haryana)|(Himachal Pradesh)|" +
                                    "(Jharkhand)|(Karnataka)|(Kerala)|(Madhya Pradesh)|(Maharashtra)|(Manipur)|(Meghalaya)|(Mizoram)|(Nagaland)|(Odisha)|(Punjab)|" +
                                    "(Rajasthan)|(Sikkim)|(Tamil Nadu)|(Telangana)|(Tripura)|(Uttar Pradesh)|(Uttarakhand)|(West Bengal)|(Andaman and Nicobar Islands)|"
                                    "(Chandigarh)|(Dadra and Nagar Haveli and Daman and Diu)|(Delhi)|(Jammu and Kashmir)|(Ladakh)|(Lakshadweep)|(Puducherry)$"
                                ")",
]

indian_address_end_pattern2 = [
                                "(" +
                                    "((?<!\w)AP(?!\w))|((?<!\w)AR(?!\w))|((?<!\w)AS(?!\w))|((?<!\w)BR(?!\w))|((?<!\w)CG(?!\w))|((?<!\w)GA(?!\w))|((?<!\w)GJ(?!\w))|" +
                                    "((?<!\w)HR(?!\w))|((?<!\w)HP(?!\w))|((?<!\w)JH(?!\w))|((?<!\w)KA(?!\w))|((?<!\w)KL(?!\w))|((?<!\w)MP(?!\w))|((?<!\w)MH(?!\w))|" +
                                    "((?<!\w)MN(?!\w))|((?<!\w)ML(?!\w))|((?<!\w)MZ(?!\w))|((?<!\w)NL(?!\w))|((?<!\w)OD(?!\w))|((?<!\w)PB(?!\w))|((?<!\w)RJ(?!\w))|" +
                                    "((?<!\w)SK(?!\w))|((?<!\w)TN(?!\w))|((?<!\w)TS(?!\w))|((?<!\w)TR(?!\w))|((?<!\w)UP(?!\w))|((?<!\w)UK(?!\w))|((?<!\w)WB(?!\w))|" +
                                    "((?<!\w)AN(?!\w))|((?<!\w)CH(?!\w))|((?<!\w)DD(?!\w))|((?<!\w)DL(?!\w))|((?<!\w)JK(?!\w))|((?<!\w)LA(?!\w))|((?<!\w)LD(?!\w))|" +
                                    "((?<!\w)PY(?!\w))" +
                                "$)",
]

india_states = {
    "AP":"Andhra Pradesh",
    "AR":"Arunachal Pradesh",
    "AS":"Assam",
    "BR":"Bihar",
    "CG":"Chhattisgarh",
    "GA":"Goa",
    "GJ":"Gujarat",
    "HR":"Haryana",
    "HP":"Himachal Pradesh",
    "JH":"Jharkhand",
    "KA":"Karnataka",
    "KL":"Kerala",
    "MP":"Madhya Pradesh",
    "MH":"Maharashtra",
    "MN":"Manipur",
    "ML":"Meghalaya",
    "MZ":"Mizoram",
    "NL":"Nagaland",
    "OD":"Odisha",
    "PB":"Punjab",
    "RJ":"Rajasthan",
    "SK":"Sikkim",
    "TN":"Tamil Nadu",
    "TS":"Telangana",
    "TR":"Tripura",
    "UP":"Uttar Pradesh",
    "UK":"Uttarakhand",
    "WB":"West Bengal",

    "AN":"Andaman and Nicobar Islands",
    "CH":"Chandigarh",
    "DD":"Dadra and Nagar Haveli and Daman and Diu",
    "DL":"Delhi",
    "JK":"Jammu and Kashmir",
    "LA":"Ladakh",
    "LD":"Lakshadweep",
    "PY":"Puducherry"
}

# FUNCTIONS
def find_indian_addresses(text, patterns, is_contact_page=False):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text, flags=re.IGNORECASE)
        if(items):
            for item in items:
                found_addresses.append(item[0].strip())
    if(is_contact_page and len(found_addresses) == 0):
        pattern = "(\n(\s{,150}[#&\w \-\.\(\)/–:’]{2,40},){2,8}\s{,150}[#&\w \-\.\(\)/–:’]{2,40}\n)"
        items = re.findall(pattern, text)
        if(items):
            for item in items:
                found_addresses.append(item[0])
    return list(set(found_addresses))


def recheck_indian_address(address):
    if(("(" in address and ")" in address) or (not "(" in address and not ")" in address)):
        m = re.search("(address\s?:?)", address, flags=re.IGNORECASE)
        if(m):
            address = address.split(m.group(0))[1]
        
        m = re.search("(centre\s?:)", address, flags=re.IGNORECASE)
        if(m):
            address = address.split(m.group(0))[1]

        m = re.search("((office\s?:)|(office\s*\n))", address, flags=re.IGNORECASE)
        if(m):
            address = address.split(m.group(0))[1]
        
        #m = re.search("((Private Limited)|(Pvt\. Ltd\.))", address, flags=re.IGNORECASE)
        #if(m):
        #    address = address.split(m.group(0))[1]
        
        m = re.search("((phone)|(tel(?!\w)))", address, flags=re.IGNORECASE)
        if(m):
            address = address.split(m.group(0))[0]

        address = re.sub("\n", ", ", address)
        address = re.sub("\r", ", ", address)
        address = re.sub("\t", ", ", address)
        address = re.sub("((,\s*){2,})", ", ", address)
        address = re.sub("\s{2,}", " ", address)
        address = address.strip()
        address = address.strip(",")
        address = address.strip(".")
        address = address.strip(",")

        if(len(address) < 25):
            print("not reached minimum length... > ", address)
            return None
        if(address.count(",") > 10 or address.count(",") == 0):
            return None

        if(sum(1 for m in re.finditer("\d", address)) > 14):
            return None
        
        if((not re.search(indian_address_end_pattern1[0], address, flags=re.IGNORECASE)) and (not re.search(indian_address_end_pattern2[0], address))):
            return None

        return address.strip()
    else:
        return None

def get_indian_unique_addresses(address_list):
    unique_addresses = []
    if(len(address_list) > 1):
        filtered_add_list = [add for add in address_list]
        filtered_add_list = [add.lower() for add in filtered_add_list]
        temp_list = [add for add in filtered_add_list]
        filtered_add_list = []
        # deleting common words
        for add in temp_list:
            for phrase in to_be_deleted_from_address:
                add = re.sub(phrase, " ", add, flags=re.IGNORECASE)
            filtered_add_list.append(add)
        temp_list = [add for add in filtered_add_list]
        filtered_add_list = []

        for add in temp_list:
            add = re.sub("-|–|/|,|\|\(\)", " ", add)
            add = re.sub("\s{2,}", " ", add).strip()
            add = add.split(" ")
            filtered_add_list.append(add)
        
        temp_list = [add for add in filtered_add_list]
        filtered_add_list = []
        # extracting all numbers
        for splitted_list in temp_list:
            word_list = []
            for word in splitted_list:
                m = re.search(number_founder_pattern, word)
                if(m):
                    word_list.append(m.group(1))
                    word = re.sub(m.group(1), " ", word)
                word = (re.sub("\s{2,}", " ", word)).strip()
                if(not word.endswith(".")):
                    if(len(word) >= 2):
                        word_list.append(word)
            word_list = list(set(word_list))
            filtered_add_list.append(word_list)

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

def get_indian_address_parts(address, language="en"):
    temp = address
    parts = {
        "country":"india",
        "state":"",
        "city":"",
        "postal-code":"",
        "street-address":"",
    }

    address = re.sub("[\-\.\s\|/–]*india[\-\.\s\|/–]*", "", address, flags=re.IGNORECASE)
    m = re.search("((?<!\d)\d{3}[\s\-\.]?\d{3}(?!\d))", address)
    if(m):
        parts["postal-code"] = m.group(0)
        address = re.sub("[\-\.\s\|/–]*" + m.group(0) + "[\-\.\s\|/–]*", "", address)

    address = re.sub("\s{2,}", " ", address)
    address = address.split(",")
    address = [part.strip() for part in address if sum(1 for m in re.finditer("\w", part)) > 0]

    if(len(address) >= 3):
        for k in india_states.keys():
            if(re.search(india_states[k], address[-1])):
                parts["state"] = india_states[k]
                break
            elif(re.search(k, address[-1])):
                parts["state"] = india_states[k]
                break
        
        if(parts["state"]):
            parts["city"] = address[-2]
            parts["street-address"] = ", ".join(i for i in address[:len(address) - 2])

    if(len(address) < 3 or not parts["state"]):
        print("Splitting not successfull. Using google ...")
        # using google API to find formatted address
        address_dic = get_google_formatted_address_using_address(temp, language)
        if(address_dic):
            return {"address":address_dic["address"], "components":address_dic["components"], "source": "google_geo_api"}

    return {"address":temp, "components":parts, "source":"company-website"}

def purify_indian_addresses(address_list):
    '''
    get a list of brazilian addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = []
    for address in address_list:
        new_add = recheck_indian_address(address)
        if(new_add):
            rechecked_addresses.append(new_add)
    rechecked_addresses = list(set(rechecked_addresses))
    unique_addresses = get_indian_unique_addresses(rechecked_addresses)
    
    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_indian_address_parts(add))
    return splitted_addresses


def find_indian_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phone = item
            if(len(phone) >= 11 and "\n" not in phone):
                phones.append(phone)
    return list(set(phones))

def purify_indian_phones(phone_list):
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



