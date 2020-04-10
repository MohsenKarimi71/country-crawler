from unit_test_tools.india.functions import test_address_regex_india, test_recheak_address_india, test_find_indian_addresses, test_find_indian_phones, test_get_indian_address_parts
from root.general_tools.tools import getHtmlResponse, getSoup, load_country_context
from root.website_tools.company_website import find_second_page_url, website_info

import os
import json

dir_path = os.path.dirname(os.path.abspath(__file__))

def get_domain_contact_page_text(domain):
    data = {"main_page_text": None, "contact_page_text": None}
    if domain:
        url = "http://" + domain
        print("url >>> ", url)
    
    country_context = load_country_context("india", add_with_global_setting=False)

    # getting main-page and contact-page soup object
    main_page_soup = None
    contact_page_soup = None
    res = getHtmlResponse(url, use_proxy=False)
    if(res):
        final_url = res.url
        main_page_soup = getSoup(res)
        if(main_page_soup):
            # trying to find contact page url
            contact_page_url = find_second_page_url(main_page_soup, final_url, country_context)
            if(contact_page_url):
                print("contact_page_url >>> ", contact_page_url)
                res = getHtmlResponse(contact_page_url, use_proxy=False)
                if(res):
                    contact_page_soup = getSoup(res)
                    if(not contact_page_soup):
                        print("No contact page soup")
                else:
                    contact_page_url = find_second_page_url(main_page_soup, url, country_context)
                    if(contact_page_url):
                        print("contact_page_url >>> ", contact_page_url)
                        res = getHtmlResponse(contact_page_url, use_proxy=False)
                        if(res):
                            contact_page_soup = getSoup(res)
                            if(not contact_page_soup):
                                print("No contact page soup")
                        else:
                            print("No contact page response...")
            else:
                print("No contact page url...")
        else:
            print("No main page soup...")
    else:
        print("No main response...")
    
    if(main_page_soup):
        data["main_page_text"] = "\n".join(string for string in main_page_soup.stripped_strings)
    if(contact_page_soup):
        data["contact_page_text"] = "\n".join(string for string in contact_page_soup.stripped_strings)
    #print(data["contact_page_text"])
    return data

##################################################################### INDIA ###################################################################
#************************************************************************#

def run_test_address_regex_india_by_domain(domain):
    print(50 * "*")
    context = load_country_context(country="india", add_with_global_setting=False)
    if(domain):
        url = "http://" + domain
        print("\nLooking in domain main page...")
        print("url: ", url)
        res = getHtmlResponse(url, use_proxy=False)
        if(res):
            soup = getSoup(res)
            if(soup):
                text = "\n".join(string for string in soup.stripped_strings)
                #print("\n", text, "\n")
                result = test_address_regex_india(text, context)
                if(result):
                    print(len(result), " item found:")
                    for item in result:
                        print(">>> ", item[0], " <<<\n")
                else:
                    print("no item found.")
                
                print("********************************************************\nLooking in domain contact page...")
                final_url = res.url
                print("final_url: ", final_url)
                contact_page_soup = None
                contact_url = find_second_page_url(soup, final_url, context)
                if(contact_url):
                    res = getHtmlResponse(contact_url, use_proxy=False)
                    if(res):
                        print("contact_url: ", contact_url)
                        contact_page_soup = getSoup(res)
                    else:
                        if(final_url in contact_url):
                            contact_url = contact_url.replace(final_url, url)
                            res = getHtmlResponse(contact_url, use_proxy=False)
                            if(res):
                                print("contact_url: ", contact_url)
                                contact_page_soup = getSoup(res)
                            else:
                                print("no response for url >>> ", contact_url)
                    
                    if(contact_page_soup):
                        text = "\n".join(string for string in contact_page_soup.stripped_strings)
                        #print(text)
                        #print("\n", text, "\n")
                        result = test_address_regex_india(text, context)
                        if(result):
                            print(len(result), " item found:")
                            for item in result:
                                print(">>> ", item[0], " <<<\n")
                        else:
                            print("no item found.")
                    else:
                        print("can not get soup object for response")
                else:
                    print("contact url not found")
            else:
                print("can not get soup object for response")
        else:
            print("no response for url >>> ", url)
    else:
        print("invalid domain >>> ", domain)
    print(50 * "*")

#run_test_address_regex_india_by_domain("novatechprojects.com")
'''
samples = json.loads(open(os.path.join(dir_path, "samples", "india", "samples.json"), mode="r", encoding="utf-8").read())
for dic in samples[376:385]:
    domain = dic["Website"]
    run_test_address_regex_india_by_domain(domain)
    print(80 * "#")
'''
#************************************************************************#

def run_test_address_regex_india_by_text(text):
    print(50 * "*")
    context = load_country_context(country="india", add_with_global_setting=False)
    print("\n", text, "\n")
    result = test_address_regex_india(text, context)
    if(result):
        print(len(result), " item found:")
        for item in result:
            print(item[0])
    else:
        print("no item found.")

#samples = json.loads(open(os.path.join(dir_path, "samples", "india", "addresses.json"), mode="r", encoding="utf-8").read())
#for dic in samples:
#    #print("Address: ", dic["address"])
#    run_test_address_regex_india_by_text(dic["address"])

t = ''''''
#run_test_address_regex_india_by_text(t)
#************************************************************************#

def run_test_recheak_address_india_by_text(text):
    print("input address: ", text)
    result = test_recheak_address_india(text)
    if(result):
        print("output address: ", result)
    else:
        print("Not valid address")

#samples = json.loads(open(os.path.join(dir_path, "samples", "india", "addresses.json"), mode="r", encoding="utf-8").read())
#for dic in samples:
#    run_test_recheak_address_india_by_text(dic["address"])
#    print(80 * "#")
#************************************************************************#

def run_test_find_indian_addresses_by_domain(domain):
    texts = get_domain_contact_page_text(domain)
    context = load_country_context(country="india", add_with_global_setting=False)
    domain_data = []
    
    if(texts["main_page_text"]):
        domain_data = test_find_indian_addresses(texts["main_page_text"], context)
        if(texts["contact_page_text"]):
            domain_data.extend(test_find_indian_addresses(texts["contact_page_text"], context, is_contact_page=True))
        else:
            print("no contact page text for domain: ", domain)
    else:
        print("no main page text for domain: ", domain)
    
    return domain_data

'''
samples = json.loads(open(os.path.join(dir_path, "samples", "india", "samples.json"), mode="r", encoding="utf-8").read())
all_data = []
for dic in samples[450:600]:
    domain = dic["Website"]
    found_addresses = run_test_find_indian_addresses_by_domain(domain)
    #checked_addresses = []
    #for add in found_addresses:
    #    checked_addresses.append({"pure": add, "checked": test_recheak_address_india(add)})

    #all_data.append({"domain": domain, "addresses": checked_addresses})
    all_data.append({"domain": domain, "addresses": found_addresses})
    with open(os.path.join(dir_path, "output", "india", "address_only_output4.json"), mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all_data, indent=4, ensure_ascii=False))
    print(80 * "#")
'''
'''
found_addresses = run_test_find_indian_addresses_by_domain("www.murugappa.com")
for add in found_addresses:
    res = test_recheak_address_india(add)
    print("add >>> ", add)
    print("res >>> ", res, "\n")
'''


#************************************************************************#

def run_test_find_indian_addresses_phones_by_domain(domain):
    texts = get_domain_contact_page_text(domain)
    context = load_country_context(country="india", add_with_global_setting=False)
    domain_data = {"addresses": [], "phones": []}
    
    if(texts["main_page_text"]):
        domain_data["addresses"] = test_find_indian_addresses(texts["main_page_text"], context)
        domain_data["phones"] = test_find_indian_phones(texts["main_page_text"], context)
        if(texts["contact_page_text"]):
            domain_data["addresses"].extend(test_find_indian_addresses(texts["contact_page_text"], context))
            domain_data["phones"].extend(test_find_indian_phones(texts["contact_page_text"], context))
        else:
            print("no contact page text for domain: ", domain)
    else:
        print("no main page text for domain: ", domain)
    
    return domain_data

'''
samples = json.loads(open(os.path.join(dir_path, "samples", "india", "samples.json"), mode="r", encoding="utf-8").read())
all_data = []
for dic in samples[450:600]:
    domain = dic["Website"]
    data = run_test_find_indian_addresses_phones_by_domain(domain)
    checked_addresses = []
    for add in data["addresses"]:
        checked_addresses.append({"pure": add, "checked": test_recheak_address_india(add)})

    all_data.append({"domain": domain, "addresses": checked_addresses, "phones": data["phones"]})
    with open(os.path.join(dir_path, "output", "india", "address_phone_out_put.json"), mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all_data, indent=4, ensure_ascii=False))
    print(80 * "#")
'''
#************************************************************************#
def run_company_website_function(domain, org_name, language, country):
    return website_info(domain, org_name, language, country)

'''
samples = json.loads(open(os.path.join(dir_path, "samples", "india", "samples.json"), mode="r", encoding="utf-8").read())
all_data = []
for dic in samples[732:1100]:
    domain = dic["Website"]
    org_name = dic["Organization Name"]

    data = run_company_website_function(domain, org_name, "en", "india")
    all_data.append(data)

    with open(os.path.join(dir_path, "output", "india", "final_output2.json"), mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all_data, indent=4, ensure_ascii=False))
    print(80 * "#")
'''

#data = run_company_website_function("www.archimedes.in", "Dinsignia Architects", "en", "india")
#print(data)

input_data = {
"domain": "www.fengle.com.cn",
"name": "合肥丰乐种业股份有限公司",
"country": "china"
}

#data = run_company_website_function("www.fengle.com.cn", "合肥丰乐种业股份有限公司", "cn", "china")
#print(data)
#************************************************************************#
def run_test_get_indian_address_parts(address):
    print(test_get_indian_address_parts(address))

'''
samples = json.loads(open(os.path.join(dir_path, "output", "india", "found_addresses.json"), mode="r", encoding="utf-8").read())
for add in samples[10:20]:
    print(add)
    run_test_get_indian_address_parts(add)
    print(80 * "*")
'''
#************************************************************************#

###############################################################################################################################################

####################################################################### RUSSIA ################################################################
from unit_test_tools.russia.functions import test_json2composite_russia


#************************************************************************#
def run_test_json2composite_russia(json_obj):
    data = test_json2composite_russia(json_obj)
    return data

obj = {
        "input_data":{},
        "website_data": {
            "result":{
                "web_title": "Центр коллективного пользования НИУ МГСУ",
                "social_pages": {},
                "phones": [],
                "emails": [],
                "addresses": []
            }
        },
        "google_data": {
            "emails": [
                "root@ckpmgsu.ru"
            ],
            "social_pages": {
                "facebook": "",
                "linkedin": [],
                "instagram": [],
                "twitter": [],
                "youtube": []
            },
            "google_map_address": {
                "address": []
            }
        },
        "info-box": {
            "address": "",
            "phone": "",
            "website": ""
        },
        "country_module": {
            "result":{
                "legal_name": {
                    "en": "Federal State budget institution of higher education \"NATIONAL RESEARCH Moscow State Construction University\"",
                    "ru": "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ \"НАЦИОНАЛЬНЫЙ ИССЛЕДОВАТЕЛЬСКИЙ МОСКОВСКИЙ ГОСУДАРСТВЕННЫЙ СТРОИТЕЛЬНЫЙ УНИВЕРСИТЕТ\""
                },
                "TIN": "7716103391",
                "supervisor": "Акимов Павел Алексеевич",
                "registration_date": "26.12.2002",
                "main_activity": {
                    "en": "Higher education",
                    "ru": "Образование высшее"
                },
                "OKPO": "02066523",
                "faxes": [
                    "1839182"
                ],
                "addresses": [
                    {
                        "source": "google_geo_api",
                        "address": "Ярославское ш., 26, Москва, Россия, 129337",
                        "components": {
                            "country": "Россия",
                            "state": "",
                            "city": "Москва",
                            "street-address": "26, Ярославское шоссе, Северо-Восточный административный округ, Ярославский",
                            "postal-code": "129337"
                        }
                    }
                ],
                "emails": [
                    "meleshkoa@mgsu.ru",
                    "rnstepanov@gmail.com",
                    "kanz@mgsu.ru"
                ],
                "phones": [
                    "7(495)781-80-07",
                    "8 (495) 664-73-40"
                ]
            }
        },
}

#result = run_test_json2composite_russia(obj)
#with open(os.path.join(dir_path, "output", "russia", "json2composite_out.json"), mode="w", encoding="utf-8") as outfile:
#    outfile.write(json.dumps(result, indent=4, ensure_ascii=False))
#************************************************************************#

##############################################################################################################################################
####################################################################### CHINA ################################################################

from root.country_tools.china.tools import get_chinese_country_module_composite_data

china_obj = [
                {
                    "EnglishName":"Hefei Fengle Seed Co., Ltd.",
                    "CompanyName":"合肥丰乐种业股份有限公司",
                    "RegistrationNumbers":[
                        "91340100148974717B",
                        "340104148974717",
                        "340000000015283"
                    ],
                    "Link":"http://www.fengle.com.cn",
                    "ImageUrl":"https://img.qichacha.com/Product/5246f863-f779-4eae-8511-1ecc25ac93fe.jpg",
                    "Domain":"农业",
                    "Description":"丰乐种业是一家农业种子提供商，主营农作物种子、农产品、农化产品和相关进出口贸易业务，旗下拥有水稻、玉米、油菜、小麦、棉花、芝麻、西甜瓜、蔬菜等几十个种类的产品，此外还提供香料产品以及农副产品。",
                    "PhoneNumbers":[
                        "0551-62239975"
                    ],
                    "Emails":[
                        "2939188579@qq.com"
                    ],
                    "StockNumber":"000713",
                    "StockType":"其他投资者",
                    "Employees":"417",
                    "Location":{
                        "Country":"China",
                        "Address":"安徽省合肥市蜀山区创业大道 4 号",
                        "City":"合肥市",
                        "Province":"安徽省",
                        "County":"蜀山区"
                    },
                    "Description_english":"Fengle Seed is an agricultural seed providers, the main crop seeds, agricultural products, agricultural products and related import and export business, which owns dozens of rice, corn, canola, wheat, cotton, sesame, melon, vegetables, etc. types of products, in addition to providing fragrance products and agricultural products.",
                    "Domain_english":"agriculture",
                    "Address_english":"China, Hefei, Anhui Province Shushan venture Avenue 4",
                    "saved_logo":""
                }
]

#data = get_chinese_country_module_composite_data(china_obj, "")
#for k in data.keys():
#    print(k, "\t\t\t\t >>> ", data[k])

##############################################################################################################################################

################################################################### FACEBOOK #################################################################
from root.facebook_tools.tools import verify_facebook_link, facebook_info

#print(verify_facebook_link("https://www.facebook.com/rassadatd/", "rassadatd.ru", "russia", "7"))
#print(verify_facebook_link("https://www.facebook.com/mars.energo", "mars-energo.ru", "russia", "7"))
#print(verify_facebook_link("https://www.facebook.com/chelpipe/", "chtpz.ru", "russia", "7"))
#print(verify_facebook_link("https://www.facebook.com/pages/%D0%9C%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D0%B5%D1%80%D1%81%D1%82%D0%B2%D0%BE-%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D0%BD%D1%8B-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9-%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8/1492252324350852", "mil.ru", "russia", "7"))
print(facebook_info("https://www.facebook.com/chelpipe/", "chtpz.ru"))