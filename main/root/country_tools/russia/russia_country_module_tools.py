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

from root.country_tools.russia.tools import purify_russian_addresses, purify_russian_phones, find_VK_link
from root.general_tools.tools import getDomainName, getDomainTitle, getGoogleMatchedData, purify_emails


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


def getAllCompanyData(domain, org_name, language):
    '''
    This function takes a domain and a name as input parameters, scrapes 
    russian sources (Spark, org-info and SBIS) and google for matched companies
    using input parameters and return found results as a dictionary
    '''
    domain_tld = getDomainName(domain)
    data = {
        "domain": domain,
        "result": {
            "TIN":"",
            "google":{},
            "spark":{},
            "org-info":{},
            "SBIS":{},
            #"list-org":{}
        }
    }

    # Trying to get data from Spark using domain_tld
    spark_data = getSparkData(domain_tld, check_length=False)
    if(spark_data["TIN"] != ""):
        data["result"]["TIN"] = spark_data["TIN"]
        data["result"]["spark"] = spark_data

        data["result"]["org-info"] = getOrg_InfoData(spark_data["OKPO"])
        data["result"]["SBIS"] = getSBIS_Data(spark_data["TIN"], only_contact=True)
        #data["result"]["list-org"] = getListOrgData(spark_data["OKPO"])
    else:
        # Trying to get data from Spark using org_name
        spark_data = getSparkData(org_name, check_length=True)
        if(spark_data["TIN"] != ""):
            data["result"]["TIN"] = spark_data["TIN"]
            data["result"]["spark"] = spark_data

            data["result"]["org-info"] = getOrg_InfoData(spark_data["OKPO"])
            data["result"]["SBIS"] = getSBIS_Data(spark_data["TIN"], only_contact=True)
            #data["result"]["list-org"] = getListOrgData(spark_data["OKPO"])
        else:
            # Trying to get data from SBIS using org_name
            contact_TIN_from_SBIS = getSBIS_Data(org_name, only_contact=False)
            tin = contact_TIN_from_SBIS["TIN"]
            if(tin):
                data["result"]["TIN"] = tin
                data["result"]["SBIS"] = contact_TIN_from_SBIS

                data["result"]["spark"] = getSparkData(tin, check_length=False)
                data["result"]["org-info"] = getOrg_InfoData(data["result"]["spark"]["OKPO"])
                #data["result"]["list-org"] = getListOrgData(tin)

            else:
                # Trying to get data from SBIS using domain_tld
                contact_TIN_from_SBIS = getSBIS_Data(domain_tld, only_contact=False)
                tin = contact_TIN_from_SBIS["TIN"]
                if(tin):
                    data["result"]["TIN"] = tin
                    data["result"]["SBIS"] = contact_TIN_from_SBIS

                    data["result"]["spark"] = getSparkData(tin, check_length=False)
                    data["result"]["org-info"] = getOrg_InfoData(data["result"]["spark"]["OKPO"])
                    #data["result"]["list-org"] = getListOrgData(tin)
                else:
                    # getting domain title
                    domain_title = getDomainTitle(domain)
                    if(domain_title):
                        # Trying to get data from Spark using domain_title
                        spark_data = getSparkData(domain_title, check_length=True)
                        if(spark_data["TIN"] != ""):
                            data["result"]["TIN"] = spark_data["TIN"]
                            data["result"]["spark"] = spark_data

                            data["result"]["org-info"] = getOrg_InfoData(spark_data["OKPO"])
                            data["result"]["SBIS"] = getSBIS_Data(spark_data["TIN"], only_contact=True)
                            #data["result"]["list-org"] = getListOrgData(spark_data["OKPO"])

                        else:
                            # Trying to get data from SBIS using domain_title
                            contact_TIN_from_SBIS = getSBIS_Data(domain_title, only_contact=False)
                            tin = contact_TIN_from_SBIS["TIN"]
                            if(tin):
                                data["result"]["TIN"] = tin
                                data["result"]["SBIS"] = contact_TIN_from_SBIS

                                data["result"]["spark"] = getSparkData(tin, check_length=False)
                                data["result"]["org-info"] = getOrg_InfoData(data["result"]["spark"]["OKPO"])
                                #data["result"]["list-org"] = getListOrgData(tin)

                    if(data["result"]["TIN"] == ""):
                        # getting google data
                        google_data = getGoogleMatchedData(org_name, domain_tld, language)
                        if(google_data):
                            data["result"]["google"] = google_data
    return data

def getMergedPurifiedData(data_dic):
    '''
    This function takes a dictionary of company data that is scraped from different 
    sources, merge them by deleting repetitive data and finally split each address 
    into its constituent parts.
    '''
    if(data_dic["result"]["TIN"] == ""):
        return {"domain":data_dic["domain"], "result":{}}
    else:
        final_data = {
            "domain": data_dic["domain"],
            "result": {
            }
        }
        addresses = []
        emails = []
        phones = []
        websites = []
        for key in data_dic["result"].keys():
            if(key == "google"):
                dic = data_dic["result"]["google"]
                if(dic):
                    for k in dic.keys():
                        if(k == "formatted_address"):
                            addresses.append(dic[k])
                        elif(k == "international_phone_number"):
                            phones.append(dic[k])
                        elif(k == "website"):
                            websites.append(dic[k])
                        elif(k == "name"):
                            final_data["result"]["google-name"] = dic[k]

            elif(key != "TIN"):
                dic = data_dic["result"][key]
                if(dic):
                    for k in dic.keys():
                        if(k == "address"):
                            if(dic[k]):
                                addresses.append(dic[k])
                        elif(k == "emails"):
                            if(dic[k]):
                                emails += dic[k]
                        elif(k == "phones"):
                            if(dic[k]):
                                phones += dic[k]
                        elif(k == "website"):
                            if(dic[k]):
                                websites.append(dic[k])
                        elif(dic[k]):
                            final_data["result"][k] = dic[k]

        if(addresses):
            final_data["result"]["addresses"] = purify_russian_addresses(addresses, "country-module")
        if(emails):
            final_data["result"]["emails"] = purify_emails(emails)
        if(phones):
            final_data["result"]["phones"] = purify_russian_phones(phones)
        if(websites):
            final_data["result"]["websites"] = list(set(websites))
        return final_data

# main function
def getRussianCompanyInfo(domain, org_name, language="ru"):
    not_filtered_data = getAllCompanyData(domain, org_name, language)
    refined_data = getMergedPurifiedData(not_filtered_data)
    if("main_activity" in refined_data["result"].keys()):
        refined_data["result"]["main_activity"] = {
            "en":translator.translate(refined_data["result"]["main_activity"], src="ru", dest="en").text, 
            "ru":refined_data["result"]["main_activity"]
        }
    if("legal_name" in refined_data["result"].keys()):
        refined_data["result"]["legal_name"] = {
            "en": translator.translate(refined_data["result"]["legal_name"], src="ru", dest="en").text,
            "ru": refined_data["result"]["legal_name"]
        }
    '''
    if("addresses" in refined_data["result"].keys()):
        adds = refined_data["result"]["addresses"]
        new_adds = []
        for add_dic in adds:
            new_add_dic = {"en":{}, "ru":add_dic}
            for k in add_dic.keys():
                if(add_dic[k] != ""):
                    new_add_dic["en"][k] = translator.translate(add_dic[k], src="ru", dest="en").text
                else:
                    new_add_dic["en"][k] = ""
            new_adds.append(new_add_dic)
        refined_data["result"]["addresses"] = new_adds
    '''
    vk_link = find_VK_link(domain)
    if(vk_link):
        refined_data["result"]["vk_link"] = {"source": "google", "url": vk_link}

    return refined_data
    