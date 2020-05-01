from root.facebook_tools.tools import verify_facebook_link
from root.general_tools.tools import *
import re
import os
import shutil
from urllib.parse import urljoin
import validators

from googletrans import Translator
translator = Translator()


def get_unique_addresses_for_composite_data(original_address_list, country):
    if(country == "russia"):
        from root.country_tools.russia.tools import get_russian_unique_addresses
        unique_function = get_russian_unique_addresses
    
    elif(country == "china"):
        from root.country_tools.china.tools import get_chinese_unique_addresses
        unique_function = get_chinese_unique_addresses

    if(len(original_address_list) >= 2):
        uniques = []
        uniques.append(original_address_list[0])
        original_address_list = original_address_list[1:]

        for i, original_add in enumerate(original_address_list):
            is_unique = True
            for j, unique_add in enumerate(uniques):
                result = unique_function([original_add, unique_add], composite_mode=True)
                if(len(result) == 1):
                    is_unique = False
                    if(unique_add["source"] != "company-website"):
                        if(original_add["source"] == "company-website"):
                            uniques[j] = original_add
                        elif(original_add["source"] == "country-module" and unique_add["source"] != "country-module"):
                            uniques[j] = original_add
                    break
            if(is_unique):
                uniques.append(original_add)
        return uniques

    else:
        return original_address_list 

def get_unique_phones_for_composite_data(original_phone_list):
    if(len(original_phone_list) >= 2):
        uniques = []
        uniques.append(original_phone_list[0])
        original_phone_list = original_phone_list[1:]

        for i, original_phone in enumerate(original_phone_list):
            is_unique = True
            for j, unique_phone in enumerate(uniques):
                result = purify_phones_global([original_phone, unique_phone], composite_mode=True)
                if(len(result) == 1):
                    is_unique = False
                    if(unique_phone["source"] != "company-website"):
                        if(original_phone["source"] == "company-website"):
                            uniques[j] = original_phone
                        elif(original_phone["source"] == "country-module" and unique_phone["source"] != "country-module"):
                            uniques[j] = original_phone
                    break
            if(is_unique):
                uniques.append(original_phone)
        return uniques

    else:
        return original_phone_list 

def get_unique_emails_for_composite_data(original_email_list):
    if(len(original_email_list) >= 2):
        uniques = []
        uniques.append(original_email_list[0])
        original_email_list = original_email_list[1:]

        for i, original_email in enumerate(original_email_list):
            is_unique = True
            for j, unique_email in enumerate(uniques):
                result = purify_emails([original_email, unique_email], composite_mode=True)
                if(len(result) == 1):
                    is_unique = False
                    if(unique_email["source"] != "country-module"):
                        if(original_email["source"] == "country-module"):
                            uniques[j] = original_email
                        elif(original_email["source"] == "company-website" and unique_email["source"] != "company-website"):
                            uniques[j] = original_email
                    break
            if(is_unique):
                uniques.append(original_email)
        return uniques

    else:
        return original_email_list 


def get_country_module_composite_data(country_module_data, composite_data, country):
    if(country == "russia"):
        from root.country_tools.russia.tools import get_russian_country_module_composite_data
        composite_data = get_russian_country_module_composite_data(country_module_data, composite_data)
  
    elif(country == "china"):
        from root.country_tools.china.tools import pick_matched_case_for_composite, get_chinese_country_module_composite_data

        selected_data = pick_matched_case_for_composite(country_module_data, composite_data["input_data"]["website"])
        composite_data = get_chinese_country_module_composite_data(selected_data, composite_data)
    
    return composite_data


def purify_composite_data(composite_data):
    composite_data["composite"]["telephones"] = get_unique_phones_for_composite_data(composite_data["composite"]["telephones"])
    composite_data["composite"]["emails"] = get_unique_emails_for_composite_data(composite_data["composite"]["emails"])

    composite_data["composite"]["social_media_links"]["facebook"] = get_unique_social_media_links(composite_data["composite"]["social_media_links"]["facebook"], composite_mode=True)[:MAX_COMPOSITE_FACEBOOK_LINKS]
    composite_data["composite"]["social_media_links"]["instagram"] = get_unique_social_media_links(composite_data["composite"]["social_media_links"]["instagram"], composite_mode=True)[:MAX_COMPOSITE_INSTAGRAM_LINKS]
    composite_data["composite"]["social_media_links"]["linkedin"] = get_unique_social_media_links(composite_data["composite"]["social_media_links"]["linkedin"], composite_mode=True)[:MAX_COMPOSITE_LINKEDIN_LINKS]
    composite_data["composite"]["social_media_links"]["twitter"] = get_unique_social_media_links(composite_data["composite"]["social_media_links"]["twitter"], composite_mode=True)[:MAX_COMPOSITE_TWITTER_LINKS]
    composite_data["composite"]["social_media_links"]["youtube"] = get_unique_social_media_links(composite_data["composite"]["social_media_links"]["youtube"], composite_mode=True)[:MAX_COMPOSITE_YOUTUBE_LINKS]

    if(len(composite_data["composite"]["addresses"]) > MAX_COMPOSITE_ADDRESSES):
        selected = [item for item in composite_data["composite"]["addresses"] if item["source"]=="company-website"]
        for item in composite_data["composite"]["addresses"]:
            if(item["source"] == "country-module"):
                selected.append(item)
        if(len(selected) < MAX_COMPOSITE_ADDRESSES):
            for item in composite_data["composite"]["addresses"]:
                if(not item["source"] in ["company-website", "country-module"]):
                    selected.append(item)
        
        composite_data["composite"]["addresses"] = selected[:MAX_COMPOSITE_ADDRESSES]
    else:
        composite_data["composite"]["addresses"] = composite_data["composite"]["addresses"][:MAX_COMPOSITE_ADDRESSES]
    
    if(len(composite_data["composite"]["emails"]) > MAX_COMPOSITE_EMAILS):
        selected = [item for item in composite_data["composite"]["emails"] if item["source"]=="company-website"]
        for item in composite_data["composite"]["emails"]:
            if(item["source"] == "country-module"):
                selected.append(item)
        if(len(selected) < MAX_COMPOSITE_EMAILS):
            for item in composite_data["composite"]["emails"]:
                if(not item["source"] in ["company-website", "country-module"]):
                    selected.append(item)
        
        composite_data["composite"]["emails"] = selected[:MAX_COMPOSITE_EMAILS]
    else:
        composite_data["composite"]["emails"] = composite_data["composite"]["emails"][:MAX_COMPOSITE_EMAILS]
    
    if(len(composite_data["composite"]["telephones"]) > MAX_COMPOSITE_PHONES):
        selected = [item for item in composite_data["composite"]["telephones"] if item["source"]=="company-website"]
        for item in composite_data["composite"]["telephones"]:
            if(item["source"] == "country-module"):
                selected.append(item)
        if(len(selected) < MAX_COMPOSITE_PHONES):
            for item in composite_data["composite"]["telephones"]:
                if(not item["source"] in ["company-website", "country-module"]):
                    selected.append(item)
        
        composite_data["composite"]["telephones"] = selected[:MAX_COMPOSITE_PHONES]
    else:
        composite_data["composite"]["telephones"] = composite_data["composite"]["telephones"][:MAX_COMPOSITE_PHONES]
    
    return composite_data


def is_phone_country_matched(phone, country_code):
    if(phone.startswith("+")):
        all_digit = re.sub("\D", "", phone)
        all_digit = re.sub("^0*", "", all_digit)
        if(not all_digit.startswith(country_code)):
            return False
    elif(re.search(".*\d+.*\(", phone)):
        all_digit = re.sub("\D", "", phone)
        all_digit = re.sub("^0*", "", all_digit)
        if(not all_digit.startswith(country_code)):
            return False
    
    return True

def is_address_country_matched(address, country, language, is_address_dict):
    if(is_address_dict):
        address = address["address"]
    country_local = translator.translate(country, dest=language).text
    if(re.search(country, address, flags=re.IGNORECASE) or (re.search(country_local, address, flags=re.IGNORECASE))):
        return True
    else:
        address_dic = get_google_formatted_address_using_address(address, "en")
        if(address_dic):
            address_country = translator.translate(address_dic["components"]["country"], dest="en").text
            if(country == address_country.lower()):
                return True
            else:
                return False
        else:
            return False

def purify_matched_unmatched_data(data):
    new_data = {}
    if(data.get("website_data")):
        new_data["website_data"] = {}
        for k in data["website_data"].keys():
            if(not k in ["phones", "addresses"]):
                new_data["website_data"][k] = data["website_data"][k]
            else:
                if(data["website_data"][k]):
                    new_data["website_data"][k] = data["website_data"][k]

    if(data.get("google_data")):
        new_data["google_data"] = {}
        for k in data["google_data"].keys():
            if(k == "emails"):
                if(data["google_data"][k]):
                    new_data["google_data"][k] = data["google_data"][k]
            elif(k == "social_pages"):
                for sk in data["google_data"][k]:
                    if(data["google_data"][k][sk]):
                        if(not "social_pages" in new_data["google_data"].keys()):
                            new_data["google_data"]["social_pages"] = {}

                        new_data["google_data"][k][sk] = data["google_data"][k][sk]
            elif(k == "google_map_address"):
                if(data["google_data"][k]["address"]):
                    new_data["google_data"][k] = {"address": data["google_data"][k]["address"]}

    if(data.get("facebook_data")):
        new_data["facebook_data"] = data["facebook_data"]

    if(data.get("whois")):
        new_data["whois"] = data["whois"]

    if(data.get("infobox_info")):
        new_data["infobox_info"] = data["infobox_info"]

    if(data.get("country_module")):
        new_data["country_module"] = data["country_module"]

    final_data = {}
    for k in new_data.keys():
        if(new_data[k]):
            final_data[k] = new_data[k]
    return final_data

def save_logo_from_composite_data(composite_data, file_name):
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "saved_logos")
    if(not os.path.exists(os.path.join(base_path))):
        os.makedirs(os.path.join(base_path))

    logo_url = None
    if(composite_data["composite"].get("logo")):
        for logo in composite_data["composite"]["logo"]:
            if(logo["source"] == "company-website"):
                logo_url = logo["data"]["url"]
                use_proxy = False

                if(not validators.url(logo_url)):   # relative urls will not pass
                    if(not logo_url.startswith("/")):
                        logo_url = "/" + logo_url
                    website = composite_data["input_data"]["website"]
                    url = "http://" + website
                    response = getHtmlResponse(url)
                    if(not response and "www" not in website):
                        url = "http://www." + website
                        response = getHtmlResponse(url)
                    if(response):
                        final_url = response.url
                        logo_url = urljoin(final_url, logo_url)
                        print("logo url from ", logo["source"], " >>> ", logo_url)
                    else:
                        logo_url = None
                        print("unable to build logo url")
                break

        if(not logo_url):
            use_proxy = True
            for logo in composite_data["composite"]["logo"]:
                if(logo["source"] != "company-website"):
                    logo_url = logo["data"]["url"]
                    print("logo url from ", logo["source"], " >>> ", logo_url)
                    break
        
        if(logo_url):
            x = logo_url.split('.')[-1]
            ext = x[-3:]
            if ext[-3:] in ['png', 'jpg', 'peg', "gif", "tif"]:
                file_path = os.path.join(base_path, file_name + '.' + ext)
            else:
                file_path = os.path.join(base_path, file_name + '.jpg')

            response = getHtmlResponse(logo_url, stream=True, use_proxy=use_proxy)
            if(response):
                with open(file_path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            else:
                print("logo link error")
        else:
            print("no valid logo url found")
    else:
        print("no logo in input data")


def json2composite(json_obj, country):
    out_json = { 
        "composite": {
            "website-title": "",
            "addresses": [],
            "emails": [],
            "telephones": [],
            "social_media_links": {
                "facebook": [],
                "instagram": [],
                "linkedin": [],
                "twitter": [],
                "youtube": [],
            },
            "company-description": [],
            "company-name": [],
            "logo": []
        },
        "input_data": json_obj["input_data"],
        "matched_data": [],
        "unmatched_data": []
    }

    matched_data = {
        "website_data": {},
        "google_data": {},
        "facebook_data": [],
        "infobox_info": {},
        "country_module": {},
        "whois": {}
    }
    unmatched_data = {
        "website_data": {},
        "google_data": {},
        "facebook_data": [],
        "infobox_info": {}
    }

    country_context = load_country_context(country, add_with_global_setting=False)
    language = country_context["language"]

    # getting website data
    if(json_obj.get("website_data")):
        web_data = json_obj["website_data"]["result"]

        if(web_data.get("web_title")):
            matched_data["website_data"]["web_title"] = web_data["web_title"]
            out_json["composite"]["website-title"] = {"source":"company-website", "data": web_data["web_title"]}
        
        if(web_data.get("phones")):
            matched_data["website_data"]["phones"] = []
            unmatched_data["website_data"]["phones"] = []

            for phone in web_data["phones"]:
                if(is_phone_country_matched(phone, country_context["country_code"])):
                    matched_data["website_data"]["phones"].append(phone)
                    out_json["composite"]["telephones"].append({"source": "company-website", "phone": phone})
                else:
                    unmatched_data["website_data"]["phones"].append(phone)
        
        if(web_data.get("emails")):
            matched_data["website_data"]["emails"] = web_data["emails"]
            for email in web_data["emails"]:
                out_json["composite"]["emails"].append({"source": "company-website", "email": email})

        if(web_data.get("addresses")):
            matched_data["website_data"]["addresses"] = []
            unmatched_data["website_data"]["addresses"] = []

            for dic_address in web_data["addresses"]:
                if(is_address_country_matched(dic_address, country, language, True)):
                    matched_data["website_data"]["addresses"].append(dic_address)
                    out_json["composite"]["addresses"].append(dic_address)
                else:
                    unmatched_data["website_data"]["addresses"].append(dic_address)

        if(web_data.get("social_pages")):
            social_pages = web_data["social_pages"]
            matched_data["website_data"]["social_pages"] = social_pages

            if(social_pages.get("facebook")):
                out_json["composite"]["social_media_links"]["facebook"].append({"source":"company-website", "url": social_pages["facebook"]})

            if(social_pages.get("instagram")):
                out_json["composite"]["social_media_links"]["instagram"].append({"source":"company-website", "url": social_pages["instagram"]})

            if(social_pages.get("linkedin")):
                out_json["composite"]["social_media_links"]["linkedin"].append({"source":"company-website", "url": social_pages["linkedin"]})

            if(social_pages.get("twitter")):
                out_json["composite"]["social_media_links"]["twitter"].append({"source":"company-website", "url": social_pages["twitter"]})
            
            if(social_pages.get("youtube")):
                out_json["composite"]["social_media_links"]["youtube"].append({"source":"company-website", "url": social_pages["youtube"]})

        if(web_data.get("logo_url")):
            matched_data["website_data"]["logo_url"] = web_data["logo_url"]
            out_json["composite"]["logo"].append({"source": "company-website", "data": {"url": web_data["logo_url"], "path": None}})

    # getting google data
    if(json_obj.get("google_data")):
        google_data = json_obj["google_data"]

        if(google_data.get("emails")):
            matched_data["google_data"]["emails"] = google_data["emails"]
            for email in google_data["emails"]:
                out_json["composite"]["emails"].append({"source": "google", "email": email})

        if(google_data.get("social_pages")):
            social_pages = google_data["social_pages"]
            matched_data["google_data"]["social_pages"] = social_pages

            if(social_pages.get("facebook")):
                out_json["composite"]["social_media_links"]["facebook"].append({"source":"google", "url": social_pages["facebook"]})

            if(social_pages.get("instagram")):
                for item in social_pages["instagram"]:
                    out_json["composite"]["social_media_links"]["instagram"].append({"source":"google", "url": item})

            if(social_pages.get("linkedin")):
                for item in social_pages["linkedin"]:
                    out_json["composite"]["social_media_links"]["linkedin"].append({"source":"google", "url": item})

            if(social_pages.get("twitter")):
                for item in social_pages["twitter"]:
                    out_json["composite"]["social_media_links"]["twitter"].append({"source":"google", "url": item})
            
            if(social_pages.get("youtube")):
                for item in social_pages["youtube"]:
                    out_json["composite"]["social_media_links"]["youtube"].append({"source":"google", "url": item})

        if(google_data["google_map_address"].get("address")):
            matched_data["google_data"]["google_map_address"] = {"address": []}
            unmatched_data["google_data"]["google_map_address"] = {"address": []}

            for address in google_data["google_map_address"]["address"]:
                if(is_address_country_matched(address, country, language, False)):
                    matched_data["google_data"]["google_map_address"]["address"].append(address)
                    out_json["composite"]["addresses"].append({"source":"google", "address": address})
                else:
                    unmatched_data["google_data"]["google_map_address"]["address"].append(address)

    # getting facebook data
    if(json_obj.get("facebook_data")):
        facebook_data = json_obj["facebook_data"]
        out_json["matched_data"].append({"facebook": facebook_data})

        for dic in facebook_data:
            verified = verify_facebook_link(dic["URL"], out_json["input_data"]["website"], country, country_context["country_code"])
            if(verified):
                matched_data["facebook_data"].append(dic)
                if(dic.get("address")):
                    out_json["composite"]["addresses"].append({"source":"facebook", "address": dic["address"]})

                if(dic.get("phone")):
                    out_json["composite"]["telephones"].append({"source":"facebook", "phone": dic["phone"]})

                if(dic.get("email")):
                    for email in dic["email"]:
                        out_json["composite"]["emails"].append({"source":"facebook", "email": email})
                
                if(dic.get("fb_logo")):
                    out_json["composite"]["logo"].append({"source":"facebook", "data": {"url": dic["fb_logo"], "path": None}})

                if(dic.get("more_info")):
                    out_json["composite"]["company-description"].append({"source":"facebook", "data": dic["more_info"]})
            else:
                unmatched_data["facebook_data"].append(dic)
    
    # getting whois data
    if(json_obj.get("whois")):
        whois_data = json_obj["whois"]
        matched_data["whois"] = whois_data

        if(whois_data.get("organization")):
            out_json["composite"]["company-name"].append({"source": "whois", "data": whois_data["organization"]})

        if(whois_data.get("email")):
            out_json["composite"]["emails"].append({"source": "whois", "email": whois_data["email"]})
    
    # getting info-box data
    if(json_obj.get("infobox_info")):
        info_box_data = json_obj["infobox_info"]
        
        if(info_box_data.get("address")):
            if(is_address_country_matched(info_box_data["address"], country, language, False)):
                matched_data["infobox_info"]["address"] = info_box_data["address"]
                out_json["composite"]["addresses"].append({"source": "info-box", "address": info_box_data["address"]})
            else:
                unmatched_data["infobox_info"]["address"] = info_box_data["address"]

        if(info_box_data.get("phone")):
            if(is_phone_country_matched(info_box_data["phone"], country_context["country_code"])):
                matched_data["infobox_info"]["phone"] = info_box_data["phone"]
                out_json["composite"]["telephones"].append({"source": "info-box", "phone": info_box_data["phone"]})
            else:
                unmatched_data["infobox_info"]["phone"] = info_box_data["phone"]

    # getting country_module data
    if(json_obj.get("country_module")):
        if(json_obj["country_module"].get("result")):
            country_module_data = json_obj["country_module"]["result"]
            matched_data["country_module"] = country_module_data
            out_json = get_country_module_composite_data(country_module_data, out_json, country)
        
    out_json = purify_composite_data(out_json)
    out_json["matched_data"] = purify_matched_unmatched_data(matched_data)
    out_json["unmatched_data"] = purify_matched_unmatched_data(unmatched_data)

    # saving logo
    logo_name = "logo_name"
    save_logo_from_composite_data(out_json, logo_name)

    return {"result": out_json}
