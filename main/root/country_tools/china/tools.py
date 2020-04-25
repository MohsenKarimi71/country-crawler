from googletrans import Translator
translator = Translator()
import re

from root.general_tools.tools import getHtmlResponse, getSoup, stringCookiesToDict, getSeleniumBrowser
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



from fake_useragent import UserAgent
ua = UserAgent()

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {
    'Host':'www.baidu.com',
    'User-Agent':ua.random,
}

'''
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding: gzip, deflate, br
    'Accept-Language: en-US,en;q=0.9
    'Connection: keep-alive
    'Cookie: BIDUPSID=D4562B3D765D9EE8865A416B207004A8; PSTM=1587546470; BAIDUID=D4562B3D765D9EE89A3F2E290EEA5717:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=31358_1450_31325_21117_31254_31421_31341_31270_30824_26350_31163_31196; delPer=0; BD_CK_SAM=1; PSINO=7; BD_HOME=1; BDSVRTM=13
    'Host: www.baidu.com
    'Referer: https://www.baidu.com/
    'Sec-Fetch-Dest: document
    'Sec-Fetch-Mode: navigate
    'Sec-Fetch-Site: same-origin
    'Upgrade-Insecure-Requests: 1
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537
'''

def get_baidu_result_divs(url, domain):
    response = getHtmlResponse(url, use_proxy=True, headers=headers)
    if(response):
        soup = getSoup(response)
        print(soup.title)
        if(soup):
            result_container_divs = soup.find_all('div', class_='c-container')
            for d in result_container_divs:
                print(d.text[:100], "\n")
            result_container_divs = [container for container in result_container_divs if domain in container.text]
            return result_container_divs
        else:
            return []
    else:
        return []

def extract_legal_names_baidu(div):
    name = None
    title = div.find('h3', {'class': 't'}).get_text()
    if("限公司" in title):
        name = title.split("限公司")[0] + "限公司"
        if("-" in name):
            name = name.split("-")[1]
        if("_" in name):
            name = name.split("_")[1]
    return name

def get_legal_name_from_baidu(domain):
    baidu_search_url = "https://www.baidu.com/s?wd='{}' site:www.qichacha.com"
    #baidu_search_url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_idx=1&tn=baidu&wd={0}%20site%3A{1}&oq={0}'
    #baidu_search_url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_idx=1&tn=baidu&wd=%22{0}%22%20site%3A{1}&fenlei=256&rqlang=cn&rsv_enter=0&rsv_dl=tb&oq=%2526quot%253Bwww.hdbp.com%2526quot%253B%2520site%253Awww.qichacha.com'
    url = baidu_search_url.format(domain, "www.qichacha.com").replace(" ", "%20")
    print(url)
    names = []

    divs = get_baidu_result_divs(url, domain)
    if(divs):
        for div in divs:
            name = extract_legal_names_baidu(div)
            if(name):
                names.append(name)
    return list(set(names))


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

baidu_home_url = "https://www.baidu.com/"

def get_legal_name_from_baidu_using_selenium(domain, check_for_matched_domain=False):
    page_loaded = False
    max_try = 10
    try_counter = 0
    while((not page_loaded) and (try_counter < 10)):
        try_counter += 1
        try:
            browser = getSeleniumBrowser(headless=True)
            browser.get(baidu_home_url)
            search_input = browser.find_element(By.CLASS_NAME, "s_ipt")
            #print('search input enabled? ==>', search_input.is_enabled())
            page_loaded = True
        except:
            browser.close()
            print("baidu main page not loaded successfully...")

    if(not page_loaded):
        print("browser not loaded successfully after", try_counter, " try")
        return None

    names = []
    q = "'{}' site:www.qichacha.com".format(domain)
    print(q)
    search_input.send_keys(q)
    search_input.send_keys(u'\ue007')    #press Enter key

    try:
        result_divs = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".result.c-container"))
        )
        result_divs = browser.find_elements_by_css_selector(".result.c-container")
        
        for div in result_divs:
            if(check_for_matched_domain):
                if(domain in div.text):
                    title_tag = div.find_element_by_css_selector("h3.t")
                    title = title_tag.text
                    if("限公司" in title):
                        name = title.split("限公司")[0] + "限公司"
                        if("-" in name):
                            name = name.split("-")[1]
                        if("_" in name):
                            name = name.split("_")[1]
                        names.append(name)
            else:
                title_tag = div.find_element_by_css_selector("h3.t")
                title = title_tag.text
                if("限公司" in title):
                    name = title.split("限公司")[0] + "限公司"
                    if("-" in name):
                        name = name.split("-")[1]
                    if("_" in name):
                        name = name.split("_")[1]
                    names.append(name)
    except Exception as e:
        print("error : ", str(e))
        print("divs not found...")
    return list(set(names))


def get_legal_name_from_baidu_using_selenium_by_list(domain_list, check_for_matched_domain=False, result_reloading_pause_time=3):
    page_loaded = False
    max_try = 10
    try_counter = 0
    while((not page_loaded) and (try_counter < 10)):
        try_counter += 1
        try:
            browser = getSeleniumBrowser(headless=True)
            browser.get(baidu_home_url)
            search_input = browser.find_element(By.CLASS_NAME, "s_ipt")
            #print('search input enabled? ==>', search_input.is_enabled())
            page_loaded = True
        except:
            browser.close()
            print("baidu main page not loaded successfully...")

    if(not page_loaded):
        print("browser not loaded successfully after", try_counter, " try")
        return None

    result = []
    for domain in domain_list[:10]:
        try:
            dic = {"domain": domain, "names":[]}
            q = "'{}' site:www.qichacha.com".format(domain)
            print(q)
            for i in range(50):
                search_input.send_keys(u'\ue003')   # clear search input for new search(back-space key)
            
            search_input.send_keys(q)
            search_input.send_keys(u'\ue007')    #press Enter key
            time.sleep(result_reloading_pause_time + round((random.random() * 150) / 50))  # pause program to new search result be loaded

            try:
                result_divs = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".result.c-container"))
                )
                result_divs = browser.find_elements_by_css_selector(".result.c-container")
                
                for div in result_divs:
                    if(check_for_matched_domain):
                        if(domain in div.text):
                            title_tag = div.find_element_by_css_selector("h3.t")
                            title = title_tag.text
                            if("限公司" in title):
                                name = title.split("限公司")[0] + "限公司"
                                if("-" in name):
                                    name = name.split("-")[1]
                                if("_" in name):
                                    name = name.split("_")[1]
                                dic["names"].append(name)
                    else:
                        title_tag = div.find_element_by_css_selector("h3.t")
                        title = title_tag.text
                        if("限公司" in title):
                            name = title.split("限公司")[0] + "限公司"
                            if("-" in name):
                                name = name.split("-")[1]
                            if("_" in name):
                                name = name.split("_")[1]
                            dic["names"].append(name)  
            except Exception as e:
                print("error : ", str(e), " >>> divs not found...")
            finally:
                dic["names"] = list(set(dic["names"]))
                result.append(dic)
        except Exception as e:
            print("Error >>> ", str(e))
            browser.close()
            # loading browser again
            try_counter = 0
            page_loaded = False
            while((not page_loaded) and (try_counter < 10)):
                try_counter += 1
                try:
                    browser = getSeleniumBrowser(headless=True)
                    browser.get(baidu_home_url)
                    search_input = browser.find_element(By.CLASS_NAME, "s_ipt")
                    #print('search input enabled? ==>', search_input.is_enabled())
                    page_loaded = True
                except:
                    browser.close()
                    print("baidu main page not loaded successfully...")
            if(not page_loaded):
                print("browser not loaded successfully after", try_counter, " try")
                return result
            continue
    #browser.close()
    return result


def scrape_qichacha(query, search_domain=False):
    qichacha_search_url = 'https://www.qichacha.com/search?key={}'
    my_qichacha_string_cookies = "QCCSESSID=943estaujkcnlmj6617l1qj0d3; UM_distinctid=1719c8ea6862e9-0116078de66c3-5313f6f-100200-1719c8ea68871; CNZZDATA1254842228=997063605-1587466246-%7C1587466246; zg_did=%7B%22did%22%3A%20%221719c8ea8c221b-05c25cf449a31-5313f6f-100200-1719c8ea8c35c9%22%7D; hasShow=1; _uab_collina=158746952916961739338216; acw_tc=2ff62b9e15874695316588568e4820daa195ec4fb6592712661a92bf35; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1587469530,1587470690; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1587470721; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201587469527239%2C%22updated%22%3A%201587470730031%2C%22info%22%3A%201587469527244%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%221056ee824ee53e234a33f1988ac0ea63%22%7D"

    url = qichacha_search_url.format(query)
    print(url)
    lst = []
    response = getHtmlResponse(url, cookies=stringCookiesToDict(my_qichacha_string_cookies), use_proxy=True)
    if(response):
        soup = getSoup(response)
        if(soup):
            table = soup.find("table")
            if(table):
                td_list = table.find_all("td")
                if(td_list):
                    if search_domain:
                        query = query.replace('www.', "")

                    for td in td_list:
                        matched_tag = td.find(text=re.compile(query))   # looking for tags with query provided in text
                        if matched_tag:
                            try:
                                imgUrl = matched_tag.find_parent('tr').find('img')['src']
                            except AttributeError:
                                imgUrl = ''
                            parent_td = matched_tag.find_parent('td')
                            data = extract_td(parent_td, query, search_domain)
                            data['ImageUrl'] = imgUrl
                            lst.append(data)
                
            else:
                print('No Table found!')
    return lst


