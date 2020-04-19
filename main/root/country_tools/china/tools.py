from googletrans import Translator
translator = Translator()
import re

from root.general_tools.composite_tools import get_unique_addresses_for_composite_data
number_founder_pattern = "[\D]*(\d+)[\D]*"

def get_chinese_unique_addresses(original_address_list, composite_mode=False):
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


def pick_matched_case_for_composite(country_module_data, domain):
    if(len(country_module_data) == 1):
        return country_module_data[0]
    else:
        for dic in country_module_data:
            if(dic.get("Link")):
                if(domain in dic["Link"]):
                    return dic
        
        # no matching link found, trying to find case with matched email and company name data
        main_domain = domain.replace("www.", "")
        main_domain = main_domain.split("/")[0]
        dics_with_matched_email = []
        for dic in country_module_data:
            if(dic.get("Emails")):
                for email in dic["Emails"]:
                    if(main_domain in email):
                        if(dic.get("CompanyName")):
                            return dic
                        else:
                            dics_with_matched_email.append(dic)
                            break
        
        # no case with matched email and company-name, return first item with matched email only
        if(dics_with_matched_email):
            return dics_with_matched_email[0]
        # no case with matched email, retrun first case
        return country_module_data[0] 


def get_chinese_country_module_composite_data(country_data, composite_data):
    if(country_data.get("EnglishName")):
        composite_data["composite"]["company-name"].append({"source": "country-module", "data": country_data["EnglishName"]})

    if(country_data.get("CompanyName")):
        composite_data["composite"]["company-name"].append({"source": "country-module", "data": country_data["CompanyName"]})

    if(country_data.get("Location")):
        add_dic = country_data["Location"]
        address = add_dic["Address"] + ", " + add_dic["County"] + ", " + add_dic["City"] + ", " + add_dic["Province"] + ", " + add_dic["Country"]
        address = re.sub(",\s*,", ",", address)

        composite_data["composite"]["addresses"].append(
            {
                "source": "country-module",
                "address": address,
                "components": {
                    "country": add_dic["Country"],
                    "state": add_dic["Province"],
                    "city": add_dic["City"],
                    "street-address": add_dic["Address"],
                    "postal-code": ""
                }
            }
        )

        composite_data["composite"]["addresses"].append(
            {
                "source": "country-module",
                "address": translator.translate(address, src="zh-cn", dest="en").text,
                "components": {
                    "country": "china",
                    "state": translator.translate(add_dic["Province"], src="zh-cn", dest="en").text,
                    "city": translator.translate(add_dic["City"], src="zh-cn", dest="en").text,
                    "street-address": translator.translate(add_dic["Address"], src="zh-cn", dest="en").text,
                    "postal-code": ""
                }
            }
        )

    if(country_data.get("PhoneNumbers")):
        for phone in country_data["PhoneNumbers"]:
            if(phone):
                composite_data["composite"]["telephones"].append({"source": "country-module", "phone": phone})
    
    if(country_data.get("Emails")):
        for email in country_data["Emails"]:
            if(email):
                composite_data["composite"]["emails"].append({"source": "country-module", "email": email})
    
    if(country_data.get("ImageUrl")):
        composite_data["composite"]["logo"].append({"source": "country-module", "data": {"url": country_data["ImageUrl"], "path": None}})
    
    company_description_items = []
    
    if(country_data.get("RegistrationNumbers")):
        numbers = ", ".join(i for i in country_data["RegistrationNumbers"] if i)
        company_description_items.append("'Registration-Numbers': '" + numbers + "'")

    if(country_data.get("Domain")):
        company_description_items.append("'Activity': '" + country_data["Domain"] + "'")

    if(country_data.get("Domain_english")):
        company_description_items.append("'Activity(english)': '" + country_data["Domain_english"] + "'")
    
    if(country_data.get("Description")):
        company_description_items.append("'Description': '" + country_data["Description"] + "'")

    if(country_data.get("Description_english")):
        company_description_items.append("'Description(english)': '" + country_data["Description_english"] + "'")

    if(country_data.get("StockNumber")):
        company_description_items.append("'Stock-Number': '" + country_data["StockNumber"] + "'")
   
    if(country_data.get("StockType")):
        company_description_items.append("'Stock-Type': '" + country_data["StockType"] + "'")
    
    if(country_data.get("Employees")):
        company_description_items.append("'Employees': '" + country_data["Employees"] + "'")

    if(len(company_description_items) > 0):
        company_description = "\n".join(item for item in company_description_items)
        composite_data["composite"]["company-description"].append({"source": "country-module", "data": company_description})

    # purifying addresses
    for index, dic in enumerate(composite_data["composite"]["addresses"]):
        if(dic["source"] in ["google", "facebook", "info-box"]):
            try:
                translated = translator.translate(dic["address"], src="en", dest="zh-cn").text
                composite_data["composite"]["addresses"][index]["address"] = translated
            except:
                pass

    composite_data["composite"]["addresses"] = get_unique_addresses_for_composite_data(composite_data["composite"]["addresses"], "china")

    return composite_data
