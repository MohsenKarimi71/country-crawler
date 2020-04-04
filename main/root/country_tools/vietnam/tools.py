from root.general_tools.tools import get_google_formatted_address_using_address
import re

# VARIABLES
to_be_deleted_from_address = [
    "văn phòng mới", "Văn phòng\s?:", "Trụ sở chính", "trụ sở",
    "xưởng mộc chính", "xưởng mộc", "Tổng kho", "Miền Trung",
    "VPGD", "Địa chỉ", "Điạ chỉ", "VPDD", "Xưởng sản xuất"
]
number_founder_pattern = "\D?(\d+)\D?"
vietnam_states = {
    "(Hồ Chí Minh)|(HCM)": "Hồ Chí Minh",
    "(Hà Nội)|(HN)": "Hà Nội",
    "Cần Thơ": "Cần Thơ",
    "Đà Nẵng": "Đà Nẵng",
    "Hải phòng": "Hải phòng",
    "An Giang": "An Giang",
    "Bà Rịa\s?-?\s?Vũng Tàu": "Bà Rịa-Vũng Tàu",
    "Bắc Giang": "Bắc Giang",
    "Bắc Kạn": "Bắc Kạn",
    "Bạc Liêu": "Bạc Liêu",
    "Bắc Ninh": "Bắc Ninh",
    "Bến Tre": "Bến Tre",
    "Bình Định": "Bình Định",
    "Bình Dương": "Bình Dương",
    "Bình Phước": "Bình Phước",
    "Bình Thuận": "Bình Thuận",
    "Cà Mau": "Cà Mau",
    "Cao Bằng": "Cao Bằng",
    "Đắk Lắk": "Đắk Lắk",
    "Đắk Nông": "Đắk Nông",
    "Điện Biên": "Điện Biên",
    "Đồng Nai": "Đồng Nai",
    "Đồng Tháp": "Đồng Tháp",
    "Gia Lai": "Gia Lai",
    "Hà Giang": "Hà Giang",
    "Hà Nam": "Hà Nam",
    "Hà Tĩnh": "Hà Tĩnh",
    "Hải Dương": "Hải Dương",
    "Hậu Giang": "Hậu Giang",
    "Hòa Bình": "Hòa Bình",
    "Hưng Yên": "Hưng Yên",
    "Khánh Hòa": "Khánh Hòa",
    "Kiến Giang": "Kiến Giang",
    "Kon Tum": "Kon Tum",
    "Lai Châu": "Lai Châu",
    "Lâm Đồng": "Lâm Đồng",
    "Lạng Sơn": "Lạng Sơn",
    "Lào Cai": "Lào Cai",
    "Long An": "Long An",
    "Nam Định": "Nam Định",
    "Nghệ An": "Nghệ An",
    "Ninh Bình": "Ninh Bình",
    "Ninh Thuận": "Ninh Thuận",
    "Phú Thọ": "Phú Thọ",
    "Phú Yên": "Phú Yên",
    "Quảng Bình": "Quảng Bình",
    "Quảng Nam": "Quảng Nam",
    "Quảng Ngãi": "Quảng Ngãi",
    "Quảng Ninh": "Quảng Ninh",
    "Quảng Trị": "Quảng Trị",
    "Sóc Trăng": "Sóc Trăng",
    "Sơn La": "Sơn La",
    "Tây Ninh": "Tây Ninh",
    "Thái Bình": "Thái Bình",
    "Thái Nguyên": "Thái Nguyên",
    "Thanh Hóa": "Thanh Hóa",
    "Thừa Thiên\s?-?\s?Huế": "Thừa Thiên-Huế",
    "Tiền Giang": "Tiền Giang",
    "Trà Vinh": "Trà Vinh",
    "Tuyên Quang": "Tuyên Quang",
    "Vĩnh Long": "Vĩnh Long",
    "Vĩnh Phúc": "Vĩnh Phúc",
    "Yên Bái": "Yên Bái"
}

# FUNCTIONS
def find_vietnamese_addresses(text, patterns):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text, flags=re.IGNORECASE)
        if(items):
            for item in items:
                found_addresses.append(item[0])
    return list(set(found_addresses))


def recheck_vietnamese_address(address):
    if(not "..." in address):
        address = re.sub("\n", " ", address)
        for phrase in to_be_deleted_from_address:
            ptr = phrase + "\s?:?"
            address = re.sub(ptr, " ", address, flags=re.IGNORECASE)
        address = re.sub("\s{2,}", " ", address)
        if(len(address.strip()) > 15):
            return address.strip()
        else:
            return None
    else:
        return None

def get_vietnamese_unique_addresses(address_list):
    unique_addresses = []
    if(len(address_list) > 1 ):
        filtered_add_list = [add.lower() for add in address_list]
        filtered_add_list = [add.replace(",", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace(".", ". ") for add in filtered_add_list]
        filtered_add_list = [add.replace("-", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace("(", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace(")", " ") for add in filtered_add_list]
        filtered_add_list = [re.sub("\s{2,}", " ", add) for add in filtered_add_list]
        filtered_add_list = [add.split(" ") for add in filtered_add_list]
        temp_list = [splitted_list for splitted_list in filtered_add_list]
        filtered_add_list = []
        # extracting all numbers
        for splitted_list in temp_list:
            word_list = []
            for word in splitted_list:
                m = re.search(number_founder_pattern, word)
                if(m):
                    word_list.append(m.group(1))
                    word = re.sub(m.group(0), " ", word)
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
                            if(score / len(splitted_list)) >= 0.6:
                                unique_addresses[index2]["splitted"] = list(set(unique_addresses[index2]["splitted"] + splitted_list))
                                is_unique = False
                                break
                        else:
                            score = 0
                            for word in unq_dic["splitted"]:
                                if(word in splitted_list):
                                    score += 1
                            if(score / len(unq_dic["splitted"])) >= 0.6:
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

def get_vietnamese_address_parts(address, language="vi"):
    print(80 * "*")
    print(address)
    temp = address
    parts = {
        "country":"Việt Nam",
        "state":"",
        "city":"",
        "street-address":"",
        "zip-code":""
    }
    m = re.search("\D(\d{6})\D", address)
    if(m):
        parts["zip-code"] = m.group(1)
        temp = re.sub(m.group(1), "", temp)

    splitted = temp.split(",")
    if(len(splitted) >= 3):
        last_index = -1
        part = splitted[-1]
        if(re.search("(Việt Nam)|(Vietnam)", part, flags=re.IGNORECASE)):
            last_index += -1   #-2
        part = splitted[last_index]   #-2 or -1
        if(re.search("Tỉnh", part, flags=re.IGNORECASE)):
            print("1")
            part = re.sub("Tỉnh", "", part, flags=re.IGNORECASE).strip()
            parts["state"] = part
            last_index += -1  #-2 or -3
            if(not re.search("\d", splitted[last_index])):
                parts["city"] = splitted[last_index].strip()
            
        else:
            for state_ptr in vietnam_states.keys():
                if(re.search(state_ptr, part, flags=re.IGNORECASE)):
                    print("2")
                    parts["state"] = vietnam_states[state_ptr]
                    last_index += -1   #-2 or -3
                    if(not re.search("\d", splitted[last_index])):
                        parts["city"] = splitted[last_index].strip()
                    break
        if(not parts["state"]):
            print("3")
            if(not re.search("\d", part)):
                parts["city"] = part.strip()
        if(parts["city"]):
            parts["street-address"] = ", ".join(i for i in splitted[:last_index])
        else:
            print("Splitting not successfull. Using google ...")
            # using google API to find formatted address
            address_dic = get_google_formatted_address_using_address(address, language)
            if(address_dic):
                return {"address":address_dic["address"], "components":address_dic["components"], "source": "google_geo_api"}
    else:
        print("Splitting not successfull. Using google ...")
        # using google API to find formatted address
        address_dic = get_google_formatted_address_using_address(address, language)
        if(address_dic):
            return {"address":address_dic["address"], "components":address_dic["components"], "source": "google_geo_api"}

    return {"address":address, "components":parts, "source":"company-website"}

def purify_vietnamese_addresses(address_list):
    '''
    get a list of vietnamese addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = set()
    for address in address_list:
        new_add = recheck_vietnamese_address(address)
        if(new_add):
            rechecked_addresses.add(new_add)
    
    unique_addresses = get_vietnamese_unique_addresses(list(rechecked_addresses))

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_vietnamese_address_parts(add))
    return splitted_addresses


def find_vietnamese_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for i in items:
            phones.append(i[0])
    return list(set(phones))

def purify_vietnamese_phones(phone_list):
    '''
    This function takes a list of phone numbers as input, extracts all unique 
    phone numbers from input list and finally return a list of unique phone numbers.
    '''
    unique_phones = []
    if(phone_list):
        if(len(phone_list) == 1):
            return phone_list
        else:
            ten_digit_set = set()
            new_phones = []
            for phone in phone_list:
                numbers = re.sub("\D", "", phone).strip()[-10:]
                new_phones.append({"phone": phone, "numbers":numbers})
            for dic in new_phones:
                if(not dic["numbers"] in ten_digit_set):
                    if(("(" in dic["phone"] and ")" in dic["phone"]) or (not "(" in dic["phone"] and not ")" in dic["phone"])):
                        ten_digit_set.add(dic["numbers"])
                        unique_phones.append(dic["phone"])
            return unique_phones
    else:
        return []
