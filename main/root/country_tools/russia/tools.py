# IMPORTS
from bs4 import NavigableString
import requests
import re
import json

from root.general_tools.tools import getHtmlResponse, getSoup
from googletrans import Translator
translator = Translator()

# VARIABLES
spark_search_url = "http://www.spark-interfax.ru/search?Query={}"
org_info_base_url = "https://www.org-info.com{}"
search_org_info_by_OKPO = "https://www.org-info.com/search.php?type=okpo&val={}"
#search_org_info_by_TIN = "https://www.org-info.com/search.php?type=inn&val={}"
#search_org_info_by_name = "https://www.org-info.com/search.php?type=name&val={}"

sbis_search_url = "https://sbis.ru/sbisru/service/?x_version=19.725.b-78"
sbis_info_url = "https://sbis.ru/contragents/{}/{}"

#list_org_search_url_by_OKPO = "https://www.list-org.com/search?type=okpo&val={}"
#list_org_search_url = "https://www.list-org.com/search?type=all&val={}"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}

email_regex = '[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9-\.\-_]+\.[a-zA-Z]+'
rusian_phone_regex = '(\d?(\s|-|\.)?\(\d{3,4}\)(\s|-|\.)?\d{2,3}(\s|-|\.)?\d{2}(\s|-|\.)?\d{2})'
#domain_regex = "^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$"


def getOrg_InfoData(OKPO_number):
    '''
    This function takes OKPO number of a russian company as input parameter, scrape 
    org-info website for this number and return found information of company as a dictionary
    '''
    orgInfo_data = {"address":"", "phones":[], "emails":[], "faxes":[], "website":""}
    try:
        url = search_org_info_by_OKPO.format(OKPO_number)
        res = getHtmlResponse(url, use_proxy=True)
        if(res):
            soup = getSoup(res)
            if(soup):
                content_div = soup.find('div', class_="content")
                href = content_div.find('a')['href']
                info_page_url = org_info_base_url.format(href)
                res = getHtmlResponse(info_page_url, use_proxy=True)
                if(res):
                    new_soup = getSoup(res)
                    if(new_soup):
                        paras = new_soup.find_all('p')
                        for p in paras:
                            text = p.text
                            if(text.startswith("Legal address:")):
                                orgInfo_data["address"] = translator.translate(text.split("Legal address:")[1].strip(), src="en", dest="ru").text
                            elif(text.startswith("E-mail: ")):
                                mails = (text.split("E-mail: ")[1]).split(',')
                                for mail in mails:
                                    orgInfo_data["emails"].append(mail.strip())
                            elif(text.startswith("Site (www):")):
                                orgInfo_data["website"] = text.split("Site (www):")[1].strip()
                            elif(text.startswith("Telephone(s): ")):
                                phones = (text.split("Telephone(s): ")[1]).split(',')
                                for phone in phones:
                                    m = re.search(rusian_phone_regex, phone)
                                    if(m):
                                        orgInfo_data["phones"].append(m.group(0))                                     
                            elif(text.startswith("Fax:")):
                                faxes = (text.split("Fax:")[1]).split(',')
                                for fax in faxes:
                                    orgInfo_data["faxes"].append(fax.strip())
        
        return orgInfo_data
    except:
        return orgInfo_data

def getSparkData(query, check_length=False):
    '''
    This function takes a name or a TIN as first input parameter "query"
    and search Spark website for information of the company. If second parameter is
    set to "False", the default case, the function do not check for unique result 
    and return registered information of first result (in case where the query parameter is 
    a TIN or a domain). If second parameter is set to "True", the function will ensure result 
    to be unique and return registered information of found result (in case where the query parameter is a name).
    '''
    url = spark_search_url.format(query)
    spark_data = {
        "legal_name":'',
        "address":"",
        'TIN':'',
        'founders':[],
        'supervisor':'',
        'registration_date':'',
        'main_activity':'',
        "OKPO":"",
    }
    try:
        # getting registered data from spark
        if(check_length):
            soup = getSoup(getHtmlResponse(url, use_proxy=True))
            if(len(soup.find_all("li", class_="search-result-list__item")) == 1):
                result = soup.find("li", class_="search-result-list__item")
                new_url = "http://www.spark-interfax.ru/" + result.find("a")["href"]
                new_soup = getSoup(getHtmlResponse(new_url, use_proxy=True))

                spark_data["legal_name"] = new_soup.find("div", attrs={"itemprop" : "legalName"}).text
                spark_data["address"] = new_soup.find("div", attrs={"itemprop" : "address"}).text
                spark_data["TIN"] = new_soup.find("div", attrs={"itemprop" : "taxID"}).text

                name_divs = new_soup.find_all('div', class_="company-characteristics__name")
                for div in name_divs:
                    if(div.text == "ОКПО"):
                        for d in div.next_siblings:
                            if(not isinstance(d, NavigableString)):
                                if(d['class'][0] == "company-characteristics__value"):
                                    spark_data["OKPO"] = d.text
                    elif(div.text == "Руководитель"):
                        for d in div.next_siblings:
                            if(not isinstance(d, NavigableString)):
                                if(d['class'][0] == "company-characteristics__value"):
                                    m = re.search('\w[\s\w,]+\w+', d.text)
                                    if(m != None):
                                        spark_data["supervisor"] = m.group(0).split(',')[0]
                    elif(div.text == "Учредители"):
                        for d in div.next_siblings:
                            if(not isinstance(d, NavigableString)):
                                if(d['class'][0] == "company-characteristics__value"):
                                    m = re.search('\w[\s\w,]+\w+', d.text)
                                    if(m != None):
                                        founders = m.group(0).split(',')
                                        for founder in founders:
                                            spark_data["founders"].append((re.search('\w+\s*\w+', founder)).group(0))
                    elif(div.text == "Дата регистрации"):
                        for d in div.next_siblings:
                            if(not isinstance(d, NavigableString)):
                                if(d['class'][0] == "company-characteristics__value"):
                                    spark_data["registration_date"] = d.text

                spark_data["main_activity"] = new_soup.find('div', class_="okved-list__name").text
        else:
            soup = getSoup(getHtmlResponse(url, use_proxy=True))
            result = soup.find("li", class_="search-result-list__item")
            new_url = "http://www.spark-interfax.ru/" + result.find("a")["href"]
            new_soup = getSoup(getHtmlResponse(new_url, use_proxy=True))

            spark_data["legal_name"] = new_soup.find("div", attrs={"itemprop" : "legalName"}).text
            spark_data["address"] = new_soup.find("div", attrs={"itemprop" : "address"}).text
            spark_data["TIN"] = new_soup.find("div", attrs={"itemprop" : "taxID"}).text
                
            name_divs = new_soup.find_all("div", class_="company-characteristics__name")
            for div in name_divs:
                if(div.text == "ОКПО"):
                    for d in div.next_siblings:
                        if(not isinstance(d, NavigableString)):
                            if(d['class'][0] == "company-characteristics__value"):
                                spark_data["OKPO"] = d.text
                elif(div.text == "Руководитель"):
                    for d in div.next_siblings:
                        if(not isinstance(d, NavigableString)):
                            if(d['class'][0] == "company-characteristics__value"):
                                m = re.search('\w[\s\w,]+\w+', d.text)
                                if(m != None):
                                    spark_data["supervisor"] = m.group(0).split(',')[0]
                elif(div.text == "Учредители"):
                    for d in div.next_siblings:
                        if(not isinstance(d, NavigableString)):
                            if(d['class'][0] == "company-characteristics__value"):
                                m = re.search('\w[\s\w,]+\w+', d.text)
                                if(m != None):
                                    founders = m.group(0).split(',')
                                    for founder in founders:
                                        spark_data["founders"].append((re.search('\w+\s*\w+', founder)).group(0))
                elif(div.text == "Дата регистрации"):
                    for d in div.next_siblings:
                        if(not isinstance(d, NavigableString)):
                            if(d['class'][0] == "company-characteristics__value"):
                                spark_data["registration_date"] = d.text

            spark_data["main_activity"] = new_soup.find('div', class_="okved-list__name").text    
        return spark_data
    except:
        return spark_data
    
def getSBIS_Data(query, only_contact=True):
    '''
    This function takes a name or a TIN as first input parameter "query"
    and search SBIS website for information of the company. If second parameter is
    set to "True", the default case, the function do not check for unique result 
    and return contact information of first result (in case where the query parameter is a TIN).
    If second parameter is set to "False", the function will ensure result to be unique 
    and return TIN and contact information of found result (in case where the query parameter is a name).
    '''
    if(only_contact):
        sbis_data = {"address": "", "phones":[], "emails":[], "website":""}
    else:
        sbis_data = {"address": "", "phones":[], "emails":[], "website":"", "TIN":None}
    sbis_query = {"jsonrpc":"2.0","protocol":5,"method":"Контрагент.List","params":{"Фильтр":{"d":[True,None,True,None,query,1,None],"s":[{"t":"Логическое","n":"Misspelling"},{"t":"Строка","n":"ИдВидДеятельности"},{"t":"Логическое","n":"ИскатьВФилиалах"},{"t":"Строка","n":"Регион"},{"t":"Строка","n":"Реквизиты"},{"t":"Число целое","n":"Состояние"},{"t":"Строка","n":"ТипЛица"}],"_type":"record"},"Сортировка":{"d":[[False,"Релевантность",True]],"s":[{"t":"Логическое","n":"l"},{"t":"Строка","n":"n"},{"t":"Логическое","n":"o"}],"_type":"recordset"},"Навигация":{"d":[True,30,0],"s":[{"t":"Логическое","n":"ЕстьЕще"},{"t":"Число целое","n":"РазмерСтраницы"},{"t":"Число целое","n":"Страница"}],"_type":"record"},"ДопПоля":[]},"id":1}
    try:
        r = requests.post(sbis_search_url, json=sbis_query, headers=headers, timeout=35)
        json_data = r.json()["result"]["d"]
        if(only_contact):   # query is TIN, No need to check length of json_data
            if(json_data):
                for candidate in json_data:
                    if(len(candidate[3]) == 10):
                        url = sbis_info_url.format(candidate[3], candidate[4])
                        res = getHtmlResponse(url, use_proxy=True)
                        if(res):
                            soup = getSoup(res)
                            if(soup):
                                add_div = soup.find("div", class_="cCard__Contacts-Address")
                                if(add_div):
                                    sbis_data["address"] = add_div.text.strip()
                                main_div = soup.find('div', class_="cCard__Contacts-Additional cCard__Contacts-Additional-Mobile")
                                if(main_div):
                                    child_divs = main_div.find_all("div", class_="cCard__Contacts-Values")
                                    if(child_divs):
                                        text = ""
                                        for div in child_divs:
                                            a = div.find("a")
                                            if(a):
                                                if(a.get("href").startswith("http")):
                                                    sbis_data["website"] = a.text.strip()
                                                else:
                                                    text += div.text + '\n'
                                            else:
                                                text += div.text + '\n'
                                        matches = [m.group(0) for m in re.finditer(rusian_phone_regex, text)]
                                        sbis_data["phones"] = matches    
                                        matches = [m.group(0) for m in re.finditer(email_regex, text)]
                                        sbis_data["emails"] = matches
                        
                        break
        else:
            if(json_data and len(json_data) == 1):
                sbis_data["TIN"] = json_data[0][3]
                url = sbis_info_url.format(json_data[0][3], json_data[0][4])
                res = getHtmlResponse(url, use_proxy=True)
                if(res):
                    soup = getSoup(res)
                    if(soup):
                        add_div = soup.find("div", class_="cCard__Contacts-Address")
                        if(add_div):
                            sbis_data["address"] = add_div.text.strip()
                        main_div = soup.find('div', class_="cCard__Contacts-Additional cCard__Contacts-Additional-Mobile")
                        if(main_div):
                            child_divs = main_div.find_all("div", class_="cCard__Contacts-Values")
                            if(child_divs):
                                text = ""
                                for div in child_divs:
                                    a = div.find("a")
                                    if(a):
                                        if(a.get("href").startswith("http")):
                                            sbis_data["website"] = a.text.strip()
                                        else:
                                            text += div.text + '\n'
                                    else:
                                        text += div.text + '\n'

                                matches = [m.group(0) for m in re.finditer(rusian_phone_regex, text)]
                                sbis_data["phones"] = matches    
                                matches = [m.group(0) for m in re.finditer(email_regex, text)]
                                sbis_data["emails"] = matches
        
        return sbis_data
    except:
        return sbis_data

'''
def getListOrgData(query):
    list_org_data = {"phones":[], "emails":[], "address":"", "faxes":[], "website":""}
    url = list_org_search_url_by_OKPO.format(query)
    try:
        res = getHtmlResponse(url, use_proxy=True)
        soup = getSoup(res)
        content_div = soup.find("div", class_="org_list")
        suggested_results = content_div.find_all("p")
        if(len(suggested_results) >= 1):
            if(len(suggested_results) > 1):
            if(query in suggested_results[0].text):
                a = suggested_results[0].find("a")
                new_url = "https://www.list-org.com" + a.get("href")
                res = getHtmlResponse(new_url, use_proxy=False)
                soup = getSoup(res)
                divs = soup.find_all("div", class_="c2")
                for div in divs:
                    if(div.text == "Контактная информация:"):
                        for sibl_div in div.next_siblings:
                            if(not isinstance(sibl_div, NavigableString)):
                                if("c2m" in sibl_div.get("class")):
                                    info_paras = sibl_div.find_all("p")
                                    for info_para in info_paras:
                                        text = info_para.text
                                        if(text.startswith("Юридический адрес:")):
                                            list_org_data["address"] = text.split("Юридический адрес:")[1].strip()
                                        elif(text.startswith("Телефон:")):
                                            phones = ((text.split("Телефон:")[1]).strip()).split(",")
                                            for phone in phones:
                                                list_org_data["phones"].append(phone.strip())
                                        elif(text.startswith("Факс:")):
                                            faxes = ((text.split("Факс:")[1]).strip()).split(",")
                                            for fax in faxes:
                                                list_org_data["faxes"].append(fax.strip())
                                        elif(text.startswith("E-mail:")):
                                            emails = ((text.split("E-mail:")[1]).strip()).split(",")
                                            for mail in emails:
                                                list_org_data["emails"].append(mail.strip())
                                        elif(text.startswith("Сайт:")):
                                            list_org_data["website"] = text.split("Сайт:")[1].strip()
                                    break 
        return list_org_data
    except:
        return list_org_data
'''

################################## WEBSITE SCRAPING TOOLS #########################################
#Imports
from root.general_tools.tools import get_google_formatted_address_using_address


# VARIABLES
number_founder_pattern = "[\D]*(\d+)[\D]*"


# Functions
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
    return list(set(phones))

def purify_russian_phones(original_phone_list, composite_mode=False):
    '''
    This function takes a list of phone numbers as input, extracts all unique 
    phone numbers from input list and finally return a list of unique phone numbers.
    '''
    if(len(original_phone_list) > 1):
        unique_phones = []
        filtered_list = []
        # adding phones to filtered_list
        if(composite_mode):
            for dic in original_phone_list:
                t = re.sub("\D", "", dic["phone"])
                filtered_list.append(t[-10:])
        else:
            for phone in original_phone_list:
                t = re.sub("\D", "", phone)
                filtered_list.append(t[-10:])

        unique_phones.append({"original": original_phone_list[0], "filtered":filtered_list[0]})
        for i in range(1, len(original_phone_list)):
            is_unique = True
            for dic in unique_phones:
                if(filtered_list[i] == dic["filtered"]):
                    is_unique = False
                    break
            if(is_unique):
                unique_phones.append({"original": original_phone_list[i], "filtered":filtered_list[i]})

        return [dic["original"] for dic in unique_phones]
    else:
        return original_phone_list

def get_russian_country_module_composite_data(country_module_data):
    composite_data_extention = {
        "company-name": "",
        "addresses": [],
        "telephones":[],
        "emails":[],
    }
    if(country_module_data.get("legal_name")):
        composite_data_extention["company-name"] = {"source": "country-module", "data": country_module_data["legal_name"]["ru"]}

    if(country_module_data.get("addresses")):
        composite_data_extention["addresses"] = country_module_data["addresses"]

    if(country_module_data.get("phones")):
        for phone in country_module_data["phones"]:
            composite_data_extention["telephones"].append({"source": "country-module", "phone": phone})
    
    if(country_module_data.get("emails")):
        for email in country_module_data["emails"]:
            composite_data_extention["emails"].append({"source": "country-module", "email": email})
    
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
        composite_data_extention["company-description"] = {"source": "country-module", "data": company_description}

    return composite_data_extention


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
                print('selected vk link:', item)
                link = item[0]['link']
    return link

