from root.general_tools.tools import getHtmlResponse, getSoup, get_google_formatted_address_using_address
from root.general_tools.composite_tools import get_unique_addresses_for_composite_data
import re
number_founder_pattern = "[\D]*(\d+)[\D]*"

def find_russian_addresses(text, patterns):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text, flags=re.IGNORECASE)
        for item in items:
            add = re.sub("\n", " ", item[0])
            add = re.sub("\s{2,}", " ", add)
            found_addresses.append(add)
    return list(set(found_addresses))

def get_russian_local_address_parts(address):
    '''
    This function takes an address as input and return different parts 
    (country, state, city, zip-code and street-address) of address as a dictionary.
    '''
    result = {
        "country":"РОССИЯ",
        "state":"",
        "city":"",
        "zip-code":"",
        "street-address":"",
    }
    address = address.upper()
    address = address.replace("РОССИЯ", "")
    m = re.search(".*(\d{6}).*", address)
    if(m):
        zip_code = m.group(1)
        result["zip-code"] = zip_code
        address = address.replace(zip_code, "")

    parts = address.strip().split(",")
    used_indexes = []
    # state
    for index, part in enumerate(parts):
        if(len(part.strip()) > 1):
            if("РЕСПУБЛИКА" in part):
                result["state"] = part.replace("РЕСПУБЛИКА", "").strip()
                used_indexes.append(index)
                break
            elif("РЕСП." in part):
                result["state"] = part.replace("РЕСП.", "").strip()
                used_indexes.append(index)
                break
    # terittory
    for index, part in enumerate(parts):
        if(len(part.strip()) > 1):
            if(index not in used_indexes):
                if("КРАЙ" in part):
                    if(result["state"] == ""):
                        result["state"] = part.replace("КРАЙ", "").strip()
                    else:
                        result["state"] = result["state"] + " (" + part.replace("КРАЙ", "").strip() + ")"
                    used_indexes.append(index)
                    break
                elif(" КР." in part):
                    if(result["state"] == ""):
                        result["state"] = part.replace(" КР.", "").strip()
                    else:
                        result["state"] = result["state"] + " (" + part.replace(" КР.", "").strip() + ")"
                    used_indexes.append(index)
                    break
    # region
    for index, part in enumerate(parts):
        if(len(part.strip()) > 1):
            if(index not in used_indexes):
                if("ОБЛАСТЬ" in part):
                    if(result["state"] == ""):
                        result["state"] = part.replace("ОБЛАСТЬ", "").strip()
                    else:
                        result["state"] = result["state"] + " (" + part.replace("ОБЛАСТЬ", "").strip() + ")"
                    used_indexes.append(index)
                    break
                elif(" ОБЛ." in part):
                    if(result["state"] == ""):
                        result["state"] = part.replace(" ОБЛ.", "").strip()
                    else:
                        result["state"] = result["state"] + " (" + part.replace(" ОБЛ.", "").strip() + ")"
                    used_indexes.append(index)
                    break
                elif(" ОБЛ" in part.strip()):
                    if(result["state"] == ""):
                        result["state"] = part.replace(" ОБЛ", "").strip()
                    else:
                        result["state"] = result["state"] + " (" + part.replace(" ОБЛ", "").strip() + ")"
                    used_indexes.append(index)
                    break
    # city
    for index, part in enumerate(parts):
        if(len(part.strip()) > 1):
            if(index not in used_indexes):
                if("Г." in part):
                    result["city"] = part.replace("Г.", "").strip()
                    used_indexes.append(index)
                    break
                elif((part.strip()).endswith(" Г")):
                    result["city"] = part.replace(" Г", "").strip()
                    used_indexes.append(index)
    st_add = ""
    for index, part in enumerate(parts):
        if(len(part.strip()) >= 1):
            if(index not in used_indexes):
                st_add += part.strip() + ", "
    result["street-address"] = st_add.strip(", ")
    
    return result

def get_russian_address_parts(address, original_source, language="ru"):
    splitted_result = get_russian_local_address_parts(address)
    if(splitted_result["city"] == "" and splitted_result["state"] == ""):
        print("Splitting not successfull. Using google ...")
        # using google API to find formatted address
        address_dic = get_google_formatted_address_using_address(address, language)
        if(address_dic):
            return {"source": "google_geo_api", "address":address_dic["address"], "components":address_dic["components"]}

    m = re.search(".*\d.*", splitted_result["street-address"])
    if(not m):
        print("Splitting not successfull. Using google ...")
        # using google API to find formatted address
        address_dic = get_google_formatted_address_using_address(address, language)
        if(address_dic):
            return {"source": "google_geo_api", "address":address_dic["address"], "components":address_dic["components"]}

    return {"source":original_source, "address":address, "components":splitted_result}

def get_russian_unique_addresses(original_address_list, composite_mode=False):
    if(len(original_address_list) > 1):
        unique_addresses = []
        addresses_to_be_splitted = []
        # adding addresses to list 'addresses_to_be_splitted'
        if(composite_mode):
            for address_dic in original_address_list:
                addresses_to_be_splitted.append(address_dic["address"])
        
        else:
            addresses_to_be_splitted = [add for add in original_address_list]

        filtered_add_list = [add.lower() for add in addresses_to_be_splitted]
        filtered_add_list = [add.replace(",", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace(".", ". ") for add in filtered_add_list]
        filtered_add_list = [add.replace("-", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace("(", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace(")", " ") for add in filtered_add_list]
        filtered_add_list = [re.sub("\s{2,}", " ", add) for add in filtered_add_list]
        filtered_add_list = [add.strip() for add in filtered_add_list]
        filtered_add_list = [add.split(" ") for add in filtered_add_list]
        filtered_add_list2 = []
        for splitted_list in filtered_add_list:
            temp_list = []
            for word in splitted_list:
                numbers = re.findall(number_founder_pattern, word)
                if(len(numbers) > 0):
                    temp_list.extend(numbers)
                else:
                    if(not word.endswith(".")):
                        if(len(word) > 2):
                            temp_list.append(word)
            temp_list = list(set(temp_list))
            filtered_add_list2.append(temp_list)
        
        max_length = 0
        max_index = 0
        for i in range(len(filtered_add_list2)):
            if(len(filtered_add_list2[i]) > max_length):
                max_length = len(filtered_add_list2[i])
                max_index = i
        unique_addresses.append({"original":original_address_list[max_index], "splitted":filtered_add_list2[max_index]})

        for index1, splitted_list in enumerate(filtered_add_list2):
            if(len(splitted_list) > 0):
                is_unique = True
                if(index1 != max_index):
                    add_results = {"original":original_address_list[index1], "splitted":splitted_list}
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
                                unique_addresses[index2]["original"] = original_address_list[index1]
                                is_unique = False
                                break
                    if(is_unique):
                        unique_addresses.append(add_results)
        
        unique_addresses = [dic["original"] for dic in unique_addresses]
    else:
        unique_addresses = original_address_list

    return unique_addresses

def purify_russian_addresses(address_list, original_source):
    '''
    get a list of russian addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    unique_addresses = get_russian_unique_addresses(address_list)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_russian_address_parts(add, original_source))
    return splitted_addresses


def find_russian_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            if(re.search("(\s|\(.+\)|\-)", item.strip())):
                phones.append(item.strip())
    phones = list(set(phones))
    phones = [phone.replace("\n", "") for phone in phones]
    return phones


def get_russian_country_module_composite_data(country_module_data, composite_data):
    if(country_module_data.get("legal_name")):
        composite_data["composite"]["company-name"].append({"source": "country-module", "data": country_module_data["legal_name"]["ru"]})

    if(country_module_data.get("addresses")):
        composite_data["composite"]["addresses"].extend(country_module_data["addresses"])

    if(country_module_data.get("phones")):
        for phone in country_module_data["phones"]:
            composite_data["composite"]["telephones"].append({"source": "country-module", "phone": phone})
    
    if(country_module_data.get("emails")):
        for email in country_module_data["emails"]:
            composite_data["composite"]["emails"].append({"source": "country-module", "email": email})
    
    if(country_module_data.get("vk_link")):
        composite_data["composite"]["social_media_links"]["VK"] = country_module_data["vk_link"]

    company_description_items = []

    if(country_module_data.get("TIN")):
        company_description_items.append("'TIN': '" + country_module_data["TIN"] + "'")

    if(country_module_data.get("OKPO")):
        company_description_items.append("'OKPO': '" + country_module_data["OKPO"] + "'")

    if(country_module_data.get("registration_date")):
        company_description_items.append("'Registration Date': '" + country_module_data["registration_date"] + "'")
    
    if(country_module_data.get("supervisor")):
        company_description_items.append("'Supervisor': '" + country_module_data["supervisor"] + "'")

    if(country_module_data.get("founders")):
        company_description_items.append("'Founders': '" + ", ".join(item for item in country_module_data["founders"]) + "'")

    if(country_module_data.get("main_activity")):
        company_description_items.append("'Main Activity': '" + country_module_data["main_activity"]["ru"] + "'")
    
    if(len(company_description_items) > 0):
        company_description = "\n".join(item for item in company_description_items)
        composite_data["composite"]["company-description"] = {"source": "country-module", "data": company_description}

    # purifying addresses
    for index, dic in enumerate(composite_data["composite"]["addresses"]):
        if(dic["source"] in ["google", "facebook", "info-box"]):
            try:
                translated = translator.translate(dic["address"], src="en", dest="ru").text
                composite_data["composite"]["addresses"][index]["address"] = translated
            except:
                pass

    composite_data["composite"]["addresses"] = get_unique_addresses_for_composite_data(composite_data["composite"]["addresses"], "russia")

    # getting components of addresses that do not have this part (addresses from 'google', 'facebook', and 'info-box')
    for index, dic in enumerate(composite_data["composite"]["addresses"]):
        if(not dic.get("components")):
            composite_data["composite"]["addresses"][index] = get_russian_address_parts(dic["address"], dic["source"], language="ru")

    return composite_data

def find_VK_link(domain):
    if("www." in domain):
        domain = domain.split("www.")[1]

    searchtext = "intext:" + domain + " inurl:vk.com"
    searchtext = searchtext.replace(" ", "+").replace(":", "%3A")
    url = 'https://www.google.com/search?q=' + searchtext

    link = None
    response = getHtmlResponse(url, use_proxy=True)
    if(response):
        soup = getSoup(response)
        if(soup):
            search_result = soup.select('.r a:first-child')
            vk_result = []
            for a in search_result:
                a_text = a.text
                h_text = a.find('h3')
                if h_text:
                    vk_result.append({"title": h_text.text, "link": a.get('href')})
            item = [h for h in vk_result if re.search('VK.com', h['title'])]
            if item:
                link = item[0]['link']
    return link

