from googletrans import Translator
translator = Translator()
import re

def select_dictionary_for_composite_data(country_module_data, domain):
    if(len(country_module_data) == 1):
        return country_module_data[0]
    else:
        for dic in country_module_data:
            if(dic.get("Link")):
                if(domain in dic["Link"]):
                    return dic
        return country_module_data[0]


def get_chinese_country_module_composite_data(country_data):
    composite_data_extention = {
        "company-name": [],
        "addresses": [],
        "telephones":[],
        "emails":[],
    }
    if(country_data.get("EnglishName")):
        composite_data_extention["company-name"].append({"source": "country-module", "data": country_data["EnglishName"]})

    if(country_data.get("CompanyName")):
        composite_data_extention["company-name"].append({"source": "country-module", "data": country_data["CompanyName"]})

    if(country_data.get("Location")):
        add_dic = country_data["Location"]
        address = add_dic["Address"] + ", " + add_dic["County"] + ", " + add_dic["City"] + ", " + add_dic["Province"] + ", " + add_dic["Country"]
        address = re.sub(",\s*,", ",", address)

        composite_data_extention["addresses"].append(
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

        composite_data_extention["addresses"].append(
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
            composite_data_extention["telephones"].append({"source": "country-module", "phone": phone})
    
    if(country_data.get("Emails")):
        for email in country_data["Emails"]:
            composite_data_extention["emails"].append({"source": "country-module", "email": email})
    
    if(country_data.get("ImageUrl")):
        composite_data_extention["logo"] = {"source": "country-module", "data": {"url": country_data["ImageUrl"], "path": None}}
    
    company_description_items = []
    
    if(country_data.get("RegistrationNumbers")):
        numbers = ", ".join(i for i in country_data["RegistrationNumbers"])
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
        composite_data_extention["company-description"] = {"source": "country-module", "data": company_description}

    return composite_data_extention

