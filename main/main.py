from unit_test_tools.india.functions import test_address_regex_india, test_recheak_address_india, test_find_indian_addresses, test_find_indian_phones, test_get_indian_address_parts
from root.general_tools.tools import getHtmlResponse, getSoup, load_country_context
from root.website_tools.company_website import find_second_page_url, website_info

import os
import json

import winsound
duration = 300  # milliseconds
freq = 600  # Hz

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

#data = run_company_website_function("www.infinera.com", "Infinera Corporation", "en", "india")
#with open(os.path.join(dir_path, "output", "india", "temp.json"), mode="w", encoding="utf-8") as outfile:
#    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
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
from unit_test_tools.russia.functions import test_json2composite_russia, test_getRussianCompanyInfo

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
#with open(os.path.join(dir_path, "output", "russia", "json2composite_output.json"), mode="w", encoding="utf-8") as outfile:
#    outfile.write(json.dumps(result, indent=4, ensure_ascii=False))

'''
samples = json.loads(open(os.path.join(dir_path, "samples", "russia", "russia_complate.json"), mode="r", encoding="utf-8").read())
all = []
for sample_dic in samples[:5]:
    #print(sample_dic)
    result = run_test_json2composite_russia(sample_dic)
    all.append(result)

    with open(os.path.join(dir_path, "output", "russia", "json2composite_output.json"), mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all, indent=4, ensure_ascii=False))
'''
#************************************************************************#
'''
samples = json.loads(open(os.path.join(dir_path, "samples", "russia", "samples.json"), mode="r", encoding="utf-8").read())
all = []
for sample_dic in samples[:5]:
    print(sample_dic)
    domain = sample_dic["Website"]
    org_name = sample_dic["Organization Name"]
    data = test_getRussianCompanyInfo(domain, org_name)
    all.append(data)

    with open(os.path.join(dir_path, "output", "russia", "country_module_output.json"), mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all, indent=4, ensure_ascii=False))
'''




#************************************************************************#


##############################################################################################################################################
####################################################################### CHINA ################################################################

from root.country_tools.china.tools import get_chinese_country_module_composite_data, pick_matched_case_for_composite
from root.general_tools.composite_tools import json2composite


sample1 = {
    "input_data": {
        "search_category": "full_search",
        "country": "china",
        "query": "www.zte.com.cn",
        "email_validation": "false",
        "apikey": "1234",
        "csrfmiddlewaretoken": "Whb4XTj4LzdVXhMQUjkmJKaAxyAzW9tjiRVprPiSNSdiDePVdnF8eSR0wO6k2fLR",
        "name": "",
        "website": "www.zte.com.cn"
    },
    "website_data": {
        "result": {
            "logo_url": "https://scontent-frt3-1.xx.fbcdn.net/v/t1.0-1/p200x200/29425894_1791435460908059_2444277213982359552_n.jpg?_nc_cat=107&_nc_sid=dbb9e7&_nc_ohc=2roDHJXYkFwAX_fq4td&_nc_ht=scontent-frt3-1.xx&_nc_tp=6&oh=3dc6143c806640e1417d164e649e8d55&oe=5EBF92EA",
            "web_title": "ZTE ZTE Offical Website Leading G Innovations The worlds leading communications ",
            "social_pages": {},
            "phones": [],
            "emails": [],
            "addresses": []
        }
    },
    "google_data": {
        "emails": [
            "support@zte.com.cn",
            "mobile@zte.com.cn",
            "zte.press.release@zte.com.cn",
            "audit@zte.com.cn",
            "privacy@zte.com.cn",
            "tech.sp@zte.com.cn",
            "ma.gaili@zte.com.cn",
            "liujiawei@zte.com.cn"
        ],
        "social_pages": {
            "facebook": "https://www.facebook.com/ZTEUK/",
            "linkedin": [
                "https://www.linkedin.com/company/zte"
            ],
            "instagram": [
                "https://www.instagram.com/singhchinese/"
            ],
            "twitter": [],
            "youtube": [
                "https://www.youtube.com/watch?v=mjjsGL6Lkho"
            ]
        },
        "google_map_address": {
            "address": []
        }
    },
    "facebook_data": [
        {
            "URL": "https://www.facebook.com/ZTEUK/",
            "address": "",
            "phone": "+20 3 4508722",
            "email": [],
            "foundation": "1985",
            "industry": "Telecommunication Company · Mobile Phone Shop",
            "fb_logo": "http://graph.facebook.com/ZTEUK/picture?type=large",
            "saved_logo": "www.zte.com.cn.jpg",
            "more_info": "UK Website http://www.zte.com.cn/global/ UK Twitter  www.twitter.com/zte_uk  Technical Support -mobile@zte.com.cn or visit www.facebook.com/ZTEMobileSupport"
        }
    ],
    "whois": {
        "name": "中兴通讯股份有限公司",
        "email": "chen.xiaojun101@zte.com.cn",
        "createDate": "1998-12-28 00:00:00",
        "expireDate": "2023-12-28 00:00:00"
    },
    "country_module": {
        "result": [
            {
                "EnglishName": "Zte Kangxun Telecom Co., Ltd.",
                "RegistrationNumbers": [
                    "440301279285671",
                    "440301103342143"
                ],
                "ImageUrl": "https://qccdata.qichacha.com/AutoImage/53dec43940f7d48ba90cc2eec4c9d47c.jpg?x-oss-process=image/resize,w_160",
                "PhoneNumbers": [
                    "0755-26770912",
                    "26770912"
                ],
                "Emails": [
                    "zhang.yu68@zte.com.cn"
                ],
                "StockNumber": None,
                "StockType": "其他投资者",
                "Employees": "3307",
                "Location": {
                    "Country": "China",
                    "Address": "深圳市南山区科技南路55号中兴通讯研发楼A座3楼",
                    "City": "深圳市",
                    "Province": "广东省",
                    "County": "盐田区"
                },
                "Address_english": "China, Nanshan District, Shenzhen Science and Technology Road 55, ZTE R & D Building, 3rd Floor, Block A",
                "saved_logo": "LM_www.zte.com.cn.jpg"
            },
            {
                "EnglishName": "Zte International Investment Limited",
                "RegistrationNumbers": [
                    "440301103114530"
                ],
                "ImageUrl": "https://qccdata.qichacha.com/AutoImage/6c10fc5c61cd3d88adfb3435ae62dde6.jpg?x-oss-process=image/resize,w_160",
                "PhoneNumbers": [
                    "18675555667"
                ],
                "Emails": [
                    "lou.wei@zte-i.com",
                    "chen.lifei@zte-i.com"
                ],
                "StockNumber": None,
                "StockType": "自然人股东",
                "Employees": "8",
                "Location": {
                    "Country": "China",
                    "Address": "深圳市南山区科技南路中兴通讯研发大楼31楼B区",
                    "City": "深圳市",
                    "Province": "广东省",
                    "County": "南山区"
                },
                "Address_english": "China, South Road, Nanshan District, Shenzhen Science and Technology ZTE R & D Building B, Building 31",
                "saved_logo": "LM_www.zte.com.cn.jpg"
            },
            {
                "EnglishName": "<<No English Name>>",
                "RegistrationNumbers": [
                    "440301103105643"
                ],
                "ImageUrl": "https://co-image.qichacha.com/CompanyImage/b4e25fe750b3dc8827702af5020fe428.jpg?x-oss-process=image/resize,w_160",
                "PhoneNumbers": [
                    "0755-26771637"
                ],
                "Emails": [
                    "guo.biao1@zte.com.cn"
                ],
                "StockNumber": None,
                "StockType": "企业法人",
                "Employees": "24",
                "Location": {
                    "Country": "China",
                    "Address": "深圳市南山区高新技术产业园科技南路中兴通讯大厦A座四楼",
                    "City": "深圳市",
                    "Province": "广东省",
                    "County": "南山区"
                },
                "Address_english": "China, South Road, Hi-Tech Industrial Park, Nanshan District, Shenzhen Science and Technology ZTE fourth floor of Building A",
                "saved_logo": "LM_www.zte.com.cn.jpg",
                "CompanyName": "深圳市中兴通讯资产管理有限公司",
                "baidu_emails": [
                    "liang.ping@zte.com.cn",
                    "doc@zte.com.cn",
                    "tian.tao@zte.com.cn",
                    "IR@zte.com.cn",
                    "wang.xin37@zte.com.cn",
                    "chen.youquan@zte.com.cn",
                    "xazp@zte.com.cn"
                ]
            },
            {
                "EnglishName": "Hangzhou Zhongxing Development Co., Ltd.",
                "RegistrationNumbers": [
                    "91330108773554769P",
                    "330108000003561"
                ],
                "ImageUrl": "https://qccdata.qichacha.com/AutoImage/c0cefe644ed1ec7cd118149cea818662.jpg?x-oss-process=image/resize,w_160",
                "PhoneNumbers": [
                    "0571-87817799",
                    "87817799"
                ],
                "Emails": [
                    None
                ],
                "StockNumber": None,
                "StockType": "企业法人",
                "Employees": "1",
                "Location": {
                    "Country": "China",
                    "Address": "浙江省杭州市滨江区浦沿街道火炬南路1213号",
                    "City": "杭州市",
                    "Province": "浙江省",
                    "County": "滨江区"
                },
                "Address_english": "China, Binjiang District, Hangzhou, Zhejiang Province torch Road street Puyan 1213",
                "saved_logo": "LM_www.zte.com.cn.jpg"
            }
        ]
    }
}

sample2 = {
    "input_data": {
        "search_category": "full_search",
        "country": "china",
        "query": "www.goldzb.com",
        "email_validation": "false",
        "apikey": "1234",
        "csrfmiddlewaretoken": "XPUOkMfdwniV2JM1XnoFkpnvlsK65dQpjpE9OIe1yGiiIGP6grJrPx4VkIgRbj8X",
        "name": "",
        "website": "www.goldzb.com"
    },
    "google_data": {
        "emails": [],
        "social_pages": {
            "facebook": "",
            "linkedin": [
                "https://www.linkedin.com/company/goldleaf-jewelry-co-ltd"
            ],
            "instagram": [],
            "twitter": [],
            "youtube": []
        },
        "google_map_address": {
            "address": []
        }
    },
    "country_module": {
        "result": [
            {
                "EnglishName": "Jinzhou Cihang Group Co., Ltd.",
                "CompanyName": "金洲慈航集团股份有限公司",
                "RegistrationNumbers": [
                    None,
                    "230000100000347"
                ],
                "Link": "http://www.goldzb.com",
                "ImageUrl": "https://img.qichacha.com/Product/ff45d840-bacb-4dec-b0e6-cd6ee4972415.jpg",
                "Domain": "电子商务",
                "Description": "金洲慈航是一个黄金珠宝首饰品牌，主要从事珠宝首饰研发设计、加工制造、批发零售、品牌加盟及电子商务、黄金金融等业务，产品涵盖千足金和足金的项链、戒指、耳环、手镯及金条等，已开设直营加盟实体店300余家。",
                "PhoneNumbers": [
                    "010-64100338"
                ],
                "Emails": [
                    "jinye000587@163.com"
                ],
                "StockNumber": "000587",
                "StockType": "自然人股东",
                "Employees": None,
                "Location": {
                    "Country": "China",
                    "Address": "黑龙江省伊春市伊春区青山西路118号",
                    "City": "伊春市",
                    "Province": "黑龙江省",
                    "County": "伊美区"
                },
                "Description_english": "Jinzhou Cihang is a gold jewelery brand, mainly engaged in research and development of jewelry design, manufacturing, wholesale and retail, and e-commerce brand to join, gold and other financial services products cover thousands of gold and gold necklaces, rings, earrings, bracelets and gold bullion and so on, has been set up to join the Direct store more than 300.",
                "Domain_english": "E-commerce",
                "Address_english": "China, Yichun City, Heilongjiang Province, Yichun District 118 Castle Peak Road",
                "saved_logo": "LM_www.goldzb.com.jpg"
            },
            {
                "EnglishName": "<<No English Name>>",
                "RegistrationNumbers": [
                    "91440300056170965F",
                    "440300056170965",
                    "440301106629277"
                ],
                "ImageUrl": "https://qccdata.qichacha.com/AutoImage/aa8732bfefdac4a5b78a070a5a827e4e.jpg?x-oss-process=image/resize,w_160",
                "PhoneNumbers": [
                    "0755-22929922"
                ],
                "Emails": [
                    "1054502237@qq.com"
                ],
                "StockNumber": None,
                "StockType": "其他投资者",
                "Employees": "45",
                "Location": {
                    "Country": "China",
                    "Address": "深圳市罗湖区翠竹街道贝丽北路水贝金座大厦4层402",
                    "City": "深圳市",
                    "Province": "广东省",
                    "County": "罗湖区"
                },
                "Address_english": "China, Luohu District, Shenzhen Tsui Chuk Street Beili Road water Pui Golden Tower Building, 4th floor 402",
                "saved_logo": "LM_www.goldzb.com.jpg",
                "CompanyName": "深圳市金叶珠宝有限公司"
            },
            {
                "EnglishName": "<<No English Name>>",
                "RegistrationNumbers": [
                    "420103000350422"
                ],
                "ImageUrl": "https://co-image.qichacha.com/CompanyImage/04c4a5e7a67ebc7118a983009208112d.jpg?x-oss-process=image/resize,w_160",
                "PhoneNumbers": [
                    "027-85680816"
                ],
                "Emails": [
                    "280062554@qq.com"
                ],
                "StockNumber": None,
                "StockType": "企业法人",
                "Employees": "55",
                "Location": {
                    "Country": "China",
                    "Address": "武汉市江汉区中山大道744号1-4层",
                    "City": "武汉市",
                    "Province": "湖北省",
                    "County": "江汉区"
                },
                "Address_english": "China, Jianghan District, Zhongshan Road 744 Layer 1-4",
                "saved_logo": "LM_www.goldzb.com.jpg",
                "CompanyName": "金叶珠宝（武汉）有限公司"
            }
        ]
    }
}

#data = json2composite(sample1, "china")
#with open(os.path.join(dir_path, "output", "china", "json2composite_output.json"), mode="w", encoding="utf-8") as outfile:
#    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))

##############################################################################################################################################

################################################################### FACEBOOK #################################################################
from root.facebook_tools.tools import verify_facebook_link, facebook_info

#print(verify_facebook_link("https://www.facebook.com/rassadatd/", "rassadatd.ru", "russia", "7"))
#print(verify_facebook_link("https://www.facebook.com/mars.energo", "mars-energo.ru", "russia", "7"))
#print(verify_facebook_link("https://www.facebook.com/chelpipe/", "chtpz.ru", "russia", "7"))
#print(verify_facebook_link("https://www.facebook.com/pages/%D0%9C%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D0%B5%D1%80%D1%81%D1%82%D0%B2%D0%BE-%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D0%BD%D1%8B-%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9-%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8/1492252324350852", "mil.ru", "russia", "7"))
#print(facebook_info("https://www.facebook.com/chelpipe/", "chtpz.ru"))


obj = {
    "input_data": {
        "name": "Infinera Corporation",
        "website": "www.infinera.com",
        "country": "India"
    },
    "website_data": {
        "result": {
            "logo_url": "https://www.facebook.com/tr?id=408868526654095&ev=PageView&noscript=1",
            "web_title": "Infinera The Infinite Network",
            "social_pages": {
                "linkedin": "https://www.linkedin.com/company/infinera/",
                "facebook": "https://www.facebook.com/Infinera/",
                "youtube": "http://www.youtube.com/user/InfineraCorp",
                "twitter": "https://twitter.com/Infinera"
            },
            "phones": [],
            "emails": [
                "avue@infinera.com",
                "IR@infinera.com",
                "techsupport@infinera.com"
            ],
            "addresses": [
                {
                    "source": "google_geo_api",
                    "address": "140 Caspian Ct, Sunnyvale, CA 94089, USA",
                    "components": {
                        "country": "United States",
                        "state": "California",
                        "city": "Sunnyvale",
                        "street-address": "140, Caspian Court",
                        "postal-code": "94089"
                    }
                }
            ]
        }
    },
    "google_data": {
        "emails": [
            "info@infinera.com"
        ],
        "social_pages": {
            "facebook": "https://www.facebook.com/Infinera-Sweden-Office-460235947676938/",
            "linkedin": [
                "https://www.linkedin.com/company/infinera"
            ],
            "instagram": [],
            "twitter": [],
            "youtube": []
        },
        "google_map_address": {
            "address": [
                "401, Level GF, 3, 4 & 6 Prestige Solitaire Building, Brunton Rd, behind Ajantha Hotel, Craig Park Layout, Ashok Nagar, Bengaluru, Karnataka 560025, India",
                "Global Signature Tower, 707 & 708, South City I, Sector 30, Gurugram, Haryana 122022, India"
            ]
        }
    },
    "facebook_data": [
        {
            "URL": "https://www.facebook.com/Infinera-Sweden-Office-460235947676938/",
            "address": "",
            "phone": "",
            "email": [],
            "foundation": "",
            "industry": "Telecommunication Company",
            "fb_logo": "http://graph.facebook.com/Infinera-Sweden-Office-460235947676938/picture?type=large",
            "saved_logo": "www.infinera.com.jpg",
            "more_info": ""
        }
    ],
    "info-box": {
        "address": "",
        "phone": "",
        "website": ""
    }
}

#data = json2composite(sample1, "china")
#with open(os.path.join(dir_path, "ttt.json"), mode="w", encoding="utf-8") as outfile:
#    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))


from root.general_tools.composite_tools import is_phone_country_matched
#print(is_phone_country_matched(" 4 -123656) 4-554", "4"))

from root.general_tools.composite_tools import save_logo_from_composite_data
data = {
        "composite": {
            "website-title": {
                "source": "company-website",
                "data": "ZTE ZTE Offical Website Leading G Innovations The worlds leading communications "
            },
            "addresses": [
                {
                    "source": "country-module",
                    "address": "深圳市南山区高新技术产业园科技南路中兴通讯大厦A座四楼, 南山区, 深圳市, 广东省, China",
                    "components": {
                        "country": "China",
                        "state": "广东省",
                        "city": "深圳市",
                        "street-address": "深圳市南山区高新技术产业园科技南路中兴通讯大厦A座四楼",
                        "postal-code": ""
                    }
                },
                {
                    "source": "country-module",
                    "address": "Hi-Tech Industrial Park, Nanshan District, Shenzhen Science and Technology Road ZTE fourth floor of Building A, Nanshan District, Shenzhen City, Guangdong Province, China",
                    "components": {
                        "country": "china",
                        "state": "Guangdong Province",
                        "city": "Shenzhen",
                        "street-address": "Hi-Tech Industrial Park, Nanshan District, Shenzhen Science and Technology Road ZTE fourth floor of Building A",
                        "postal-code": ""
                    }
                }
            ],
            "emails": [
                {
                    "source": "country-module",
                    "email": "guo.biao1@zte.com.cn"
                },
                {
                    "source": "google",
                    "email": "support@zte.com.cn"
                },
                {
                    "source": "google",
                    "email": "mobile@zte.com.cn"
                },
                {
                    "source": "google",
                    "email": "zte.press.release@zte.com.cn"
                },
                {
                    "source": "google",
                    "email": "audit@zte.com.cn"
                }
            ],
            "telephones": [
                {
                    "source": "country-module",
                    "phone": "0755-26771637"
                }
            ],
            "social_media_links": {
                "facebook": [
                    {
                        "source": "google",
                        "url": "https://www.facebook.com/ZTEUK/"
                    }
                ],
                "instagram": [
                    {
                        "source": "google",
                        "url": "https://www.instagram.com/singhchinese/"
                    }
                ],
                "linkedin": [
                    {
                        "source": "google",
                        "url": "https://www.linkedin.com/company/zte"
                    }
                ],
                "twitter": [],
                "youtube": [
                    {
                        "source": "google",
                        "url": "https://www.youtube.com/watch?v=mjjsGL6Lkho"
                    }
                ]
            },
            "company-description": [
                {
                    "source": "country-module",
                    "data": "'Registration-Numbers': '440301103105643'\n'Stock-Type': '企业法人'\n'Employees': '24'"
                }
            ],
            "company-name": [
                {
                    "source": "country-module",
                    "data": "<<No English Name>>"
                },
                {
                    "source": "country-module",
                    "data": "深圳市中兴通讯资产管理有限公司"
                }
            ],
            "logo": [
                {
                    "source": "company-website",
                    "data": {
                        "url": "https://res-www.zte.com.cn/mediares/zte/Global/logo/zte_logo_en.png?h=55&la=en&w=120",
                        "path": None
                    }
                },
                {
                    "source": "country-module",
                    "data": {
                        "url": "https://co-image.qichacha.com/CompanyImage/b4e25fe750b3dc8827702af5020fe428.jpg?x-oss-process=image/resize,w_160",
                        "path": None
                    }
                }
            ]
        },
        "input_data": {
            "search_category": "full_search",
            "country": "china",
            "query": "www.zte.com.cn",
            "email_validation": "false",
            "apikey": "1234",
            "csrfmiddlewaretoken": "Whb4XTj4LzdVXhMQUjkmJKaAxyAzW9tjiRVprPiSNSdiDePVdnF8eSR0wO6k2fLR",
            "name": "",
            "website": "www.zte.com.cn"
        },
        "matched_data": {
            "website_data": {
                "web_title": "ZTE ZTE Offical Website Leading G Innovations The worlds leading communications ",
                "logo_url": "https://res-www.zte.com.cn/mediares/zte/Global/logo/zte_logo_en.png?h=55&la=en&w=120"
            },
            "google_data": {
                "emails": [
                    "support@zte.com.cn",
                    "mobile@zte.com.cn",
                    "zte.press.release@zte.com.cn",
                    "audit@zte.com.cn",
                    "privacy@zte.com.cn",
                    "tech.sp@zte.com.cn",
                    "ma.gaili@zte.com.cn",
                    "liujiawei@zte.com.cn"
                ],
                "social_pages": {
                    "facebook": "https://www.facebook.com/ZTEUK/",
                    "linkedin": [
                        "https://www.linkedin.com/company/zte"
                    ],
                    "instagram": [
                        "https://www.instagram.com/singhchinese/"
                    ],
                    "youtube": [
                        "https://www.youtube.com/watch?v=mjjsGL6Lkho"
                    ]
                }
            },
            "whois": {
                "name": "中兴通讯股份有限公司",
                "email": "chen.xiaojun101@zte.com.cn",
                "createDate": "1998-12-28 00:00:00",
                "expireDate": "2023-12-28 00:00:00"
            },
            "country_module": [
                {
                    "EnglishName": "Zte Kangxun Telecom Co., Ltd.",
                    "RegistrationNumbers": [
                        "440301279285671",
                        "440301103342143"
                    ],
                    "ImageUrl": "https://qccdata.qichacha.com/AutoImage/53dec43940f7d48ba90cc2eec4c9d47c.jpg?x-oss-process=image/resize,w_160",
                    "PhoneNumbers": [
                        "0755-26770912",
                        "26770912"
                    ],
                    "Emails": [
                        "zhang.yu68@zte.com.cn"
                    ],
                    "StockNumber": None,
                    "StockType": "其他投资者",
                    "Employees": "3307",
                    "Location": {
                        "Country": "China",
                        "Address": "深圳市南山区科技南路55号中兴通讯研发楼A座3楼",
                        "City": "深圳市",
                        "Province": "广东省",
                        "County": "盐田区"
                    },
                    "Address_english": "China, Nanshan District, Shenzhen Science and Technology Road 55, ZTE R & D Building, 3rd Floor, Block A",
                    "saved_logo": "LM_www.zte.com.cn.jpg"
                },
                {
                    "EnglishName": "Zte International Investment Limited",
                    "RegistrationNumbers": [
                        "440301103114530"
                    ],
                    "ImageUrl": "https://qccdata.qichacha.com/AutoImage/6c10fc5c61cd3d88adfb3435ae62dde6.jpg?x-oss-process=image/resize,w_160",
                    "PhoneNumbers": [
                        "18675555667"
                    ],
                    "Emails": [
                        "lou.wei@zte-i.com",
                        "chen.lifei@zte-i.com"
                    ],
                    "StockNumber": None,
                    "StockType": "自然人股东",
                    "Employees": "8",
                    "Location": {
                        "Country": "China",
                        "Address": "深圳市南山区科技南路中兴通讯研发大楼31楼B区",
                        "City": "深圳市",
                        "Province": "广东省",
                        "County": "南山区"
                    },
                    "Address_english": "China, South Road, Nanshan District, Shenzhen Science and Technology ZTE R & D Building B, Building 31",
                    "saved_logo": "LM_www.zte.com.cn.jpg"
                },
                {
                    "EnglishName": "<<No English Name>>",
                    "RegistrationNumbers": [
                        "440301103105643"
                    ],
                    "ImageUrl": "https://co-image.qichacha.com/CompanyImage/b4e25fe750b3dc8827702af5020fe428.jpg?x-oss-process=image/resize,w_160",
                    "PhoneNumbers": [
                        "0755-26771637"
                    ],
                    "Emails": [
                        "guo.biao1@zte.com.cn"
                    ],
                    "StockNumber": None,
                    "StockType": "企业法人",
                    "Employees": "24",
                    "Location": {
                        "Country": "China",
                        "Address": "深圳市南山区高新技术产业园科技南路中兴通讯大厦A座四楼",
                        "City": "深圳市",
                        "Province": "广东省",
                        "County": "南山区"
                    },
                    "Address_english": "China, South Road, Hi-Tech Industrial Park, Nanshan District, Shenzhen Science and Technology ZTE fourth floor of Building A",
                    "saved_logo": "LM_www.zte.com.cn.jpg",
                    "CompanyName": "深圳市中兴通讯资产管理有限公司",
                    "baidu_emails": [
                        "liang.ping@zte.com.cn",
                        "doc@zte.com.cn",
                        "tian.tao@zte.com.cn",
                        "IR@zte.com.cn",
                        "wang.xin37@zte.com.cn",
                        "chen.youquan@zte.com.cn",
                        "xazp@zte.com.cn"
                    ]
                },
                {
                    "EnglishName": "Hangzhou Zhongxing Development Co., Ltd.",
                    "RegistrationNumbers": [
                        "91330108773554769P",
                        "330108000003561"
                    ],
                    "ImageUrl": "https://qccdata.qichacha.com/AutoImage/c0cefe644ed1ec7cd118149cea818662.jpg?x-oss-process=image/resize,w_160",
                    "PhoneNumbers": [
                        "0571-87817799",
                        "87817799"
                    ],
                    "Emails": [
                        None
                    ],
                    "StockNumber": None,
                    "StockType": "企业法人",
                    "Employees": "1",
                    "Location": {
                        "Country": "China",
                        "Address": "浙江省杭州市滨江区浦沿街道火炬南路1213号",
                        "City": "杭州市",
                        "Province": "浙江省",
                        "County": "滨江区"
                    },
                    "Address_english": "China, Binjiang District, Hangzhou, Zhejiang Province torch Road street Puyan 1213",
                    "saved_logo": "LM_www.zte.com.cn.jpg"
                }
            ]
        },
        "unmatched_data": {
            "facebook_data": [
                {
                    "URL": "https://www.facebook.com/ZTEUK/",
                    "address": "",
                    "phone": "+20 3 4508722",
                    "email": [],
                    "foundation": "1985",
                    "industry": "Telecommunication Company · Mobile Phone Shop",
                    "fb_logo": "http://graph.facebook.com/ZTEUK/picture?type=large",
                    "saved_logo": "www.zte.com.cn.jpg",
                    "more_info": "UK Website http://www.zte.com.cn/global/ UK Twitter  www.twitter.com/zte_uk  Technical Support -mobile@zte.com.cn or visit www.facebook.com/ZTEMobileSupport"
                }
            ]
        }
    }

data2 = {
    "composite": {
        "logo": [
                {
                    "source": "company-website",
                    "data": {
                        "url": "img/soran2_2.gif",
                        "path": None
                    }
                },
                {
                    "source": "country-module",
                    "data": {
                        "url": "https://co-image.qichacha.com/CompanyImage/b4e25fe750b3dc8827702af5020fe428.jpg?x-oss-process=image/resize,w_160",
                        "path": None
                    }
                },
                {
                    "source": "facebook",
                    "data": {
                        "url": "www.zte.com.cn.jpg",
                        "path": None
                    }
                },
            ]
    },
    "input_data": {
        "case created": "1970-01-01",
        "case id": "2120963#0",
        "organization": "Nsc",
        "website": "nsc.ru",
        "country": "Russia"
        }
}
#save_logo_from_composite_data(data2, "image7")

'''
import requests
from requests.exceptions import HTTPError

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    print(url)
    try:
        response = requests.get(url)
        print(response.status_code, type(response.status_code))

        # If the response was successful, no Exception will be raised
        #response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
'''

u1 = "https://res-www.zte.com.cn/mediares/zte/Global/logo/zte_logo_en.png?h=55&la=en&w=120"
u2 = "https://co-image.qichacha.com/CompanyImage/b4e25fe750b3dc8827702af5020fe428.jpg?x-oss-process=image/resize,w_160"
u3 = "https://www.facebook.com/tr?id=408868526654095&ev=PageView&noscript=1"
u4 = "http://graph.facebook.com/Infinera-Sweden-Office-460235947676938/picture?type=large"
u5 = "https://www.infinera.com/wp-content/uploads/logo-header.png"
u6 = "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/c0.0.200.200a/p200x200/14595822_1600446113593342_3302191685176631477_n.png?_nc_cat=108&_nc_sid=dbb9e7&_nc_ohc=Pr_P9w647RoAX888T8w&_nc_ht=scontent-cdg2-1.xx&oh=b5c4ae60076bee081c112f1e1717ef57&oe=5EC1D4E4"
u7 = "https://scontent-cdt1-1.xx.fbcdn.net/v/t1.30497-1/c59.0.200.200a/p200x200/84702798_579370612644419_4516628711310622720_n.png?_nc_cat=1&_nc_sid=dbb9e7&_nc_ohc=75jDLFIoNbMAX8YSFLH&_nc_ht=scontent-cdt1-1.xx&oh=3367a03385559d60740fb69f2ba94bd7&oe=5EC2069C"
u8 = "http://graph.facebook.com/ZTEUK/picture?type=large"

#save_logo_from_composite_data(u8, "u13")

from root.facebook_tools.tools import get_facebook_logo
from root.website_tools.company_website import get_website_logo
import shutil


def save_logo(logo_url, website,  file_name):
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_logos")
    if(not os.path.exists(os.path.join(base_path))):
        os.makedirs(os.path.join(base_path))

    if(logo_url.startswith("/")):
        website = website.strip("/")
        logo_url = "http://" + website + logo_url
    
    x = logo_url.split('.')[-1]
    ext = x[-3:]
    if ext[-3:] in ['png', 'jpg', 'peg']:
        file_path = os.path.join(base_path, file_name + '.' + ext)
    else:
        file_path = os.path.join(base_path, file_name + '.jpg')

    response = getHtmlResponse(logo_url, stream=True, use_proxy=False)
    if(response):
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    else:
        print("logo link error")

'''
domain = "www.bwigroup.com"
url = "http://www.bwigroup.com"
r = getHtmlResponse(url)
if(r):
    soup = getSoup(r)
    if(soup):
        logo_url = get_website_logo(soup)
        print(logo_url)
        save_logo(logo_url, domain, "222")
    else:
        print("no soup")
else:
    print("no response")
'''

#logo_url = get_facebook_logo("https://www.facebook.com/pg/www.TGH.com.tw")
#logo_url = get_facebook_logo("https://www.facebook.com/pg/chelpipe/about/?ref=page_internal")
#logo_url = get_facebook_logo("https://www.facebook.com/pg/%D0%9A%D0%B0%D1%84%D0%B5%D0%B4%D1%80%D0%B0-%D0%9F%D0%9C%D0%98-%D0%9A%D0%BD%D0%90%D0%93%D0%A2%D0%A3-1850953428521073/about/")
#logo_url = get_facebook_logo("https://www.facebook.com/pg/knastu.official/about/?ref=page_internal")
#logo_url = get_facebook_logo("https://www.facebook.com/pg/estacons/about/?ref=page_internal")
#logo_url = get_facebook_logo("https://www.facebook.com/chelpipe")
#print(logo_url)
#save_logo(logo_url, "3")


from root.country_tools.china.tools import get_legal_name_from_baidu, scrape_qichacha
domains = [
    "www.yantaimoon.cn",
    "www.topraysolar.com",
    "www.sndf.com.cn",
    "www.hesaitech.com",
    "www.gad.com.cn",
    "www.huasen.com.cn",
    "www.bwigroup.com",
    "www.ecepdi.com",
    "www.dsbj1.com",
    "www.citichmc.com",
    "www.greatwall.com.cn",
    "www.sac-china.com",
    "www.opple.com",
    "www.colibri.com.cn",
    "www.nuctech.com",
    "www.artosyn.com",
    "www.ruentex.com.cn",
    "www.sz-sunway.com",
    "www.surun-tech.com",
    "www.troowin.com",
    "www.szemd.com",
    "www.crland.com.cn",
    "www.bcel-cn.com",
    "www.hdbp.com"
]
'''
query = query21
print("query: ", query)
names = get_legal_name_from_baidu(query)
print("names: ", names)

#print(50 * "***")
#scrape_qichacha(query)
'''

from root.country_tools.china.tools import get_legal_name_from_baidu_using_selenium
'''
all_names = []
for domain in domains[:4]:
    print(domain)
    names = get_legal_name_from_baidu_using_selenium(domain)
    print(names)
    all_names.append({"domain": domain, "names": names})
    print(50 * "*")
    with open(os.path.join(dir_path, "output", "china", "50_baidu_legel_names.json"), encoding="utf-8", mode="w") as outfile:
        outfile.write(json.dumps(all_names, indent=4, ensure_ascii=False))
'''
'''
import time
from root.country_tools.china.tools import get_legal_name_from_baidu_using_selenium_by_list

try:
    samples = json.loads(open(os.path.join(dir_path, "samples", "china", "500_samples.json"), encoding="utf-8", mode="r").read())
    domains = [dic["Website"] for dic in samples]
    print(len(domains))

    s_time = time.time()

    all_names = get_legal_name_from_baidu_using_selenium_by_list(domains[:50])

    print("time: ", time.time() - s_time)

    with open(os.path.join(dir_path, "output", "china", "51_baidu_legel_names.json"), encoding="utf-8", mode="w") as outfile:
        outfile.write(json.dumps(all_names, indent=4, ensure_ascii=False))
except Exception as e:
    print(str(e))
finally:
    print("time: ", time.time() - s_time)
    for i in range(2):
        winsound.Beep(freq, duration)
        time.sleep(1)
'''
'''
samples = json.loads(open(os.path.join(dir_path, "samples", "china", "500_samples.json"), encoding="utf-8", mode="r").read())
domains = [dic["Website"] for dic in samples]
for i in range(10, 20):
    print("http://" + domains[i])
'''

from root.general_tools.tools import load_country_context
import re

country_context = load_country_context("china", add_with_global_setting=False)
address_pattern = country_context["address_patterns"][0]
#print(address_pattern)

'''
addresses = json.loads(open(os.path.join(dir_path, "samples", "china", "addresses.json"), encoding="utf-8", mode="r").read())
for i, add in enumerate(addresses):
    if(i%2 == 0):
        print(add)
        m = re.search(address_pattern, add)
        if(m):
            print(m.group(0))
        print(50 * "*")
'''

phone_patterns = [
    "(\(?86\)?[\s\.\-]+\(?0?\d{3}\)?[\s\.\-]+\d{7,8})",
    "(\(?0?\d{3}\)?[\s\.\-]+\d{7,8})",
]

phones = [
    "0591-87761300",
    "+86-0898-68581891",
    "+86 0535 2788888",
    "0535-2788888",
    "0411-82659666",
    "0731-82183111",
    "0599-7927686",
    "0535-2119065",
    "0771-3218880",
    "(86) (938) 2859968"
]
'''
for p in phones:
    m = re.search(phone_patterns[0], p)
    print(p)
    if(m):
        print(m.group(0))
    print(50 * "*")
'''


from root.website_tools.company_website import website_info

domain = "www.socomec.com"
org_name = ""
language = "fr"
country = "france"
data = website_info(domain, org_name, language, country=country)

with open(os.path.join("temp.json"), encoding="utf-8", mode="a") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))


svg_logo_sample = "http://www.cnrs.fr/themes/custom/cnrs/logo.svg"
'''
from root.country_tools.china.tools import recheck_chinese_address
addresses = json.loads(open(os.path.join(dir_path, "samples", "china", "addresses.json"), encoding="utf-8", mode="r").read())
for i, add in enumerate(addresses):
    if(i%2 == 0):
        print(re.sub("\n", " ", add))
        print(re.sub("\n", " ", recheck_chinese_address(add)))
        print(50 * "*")
'''