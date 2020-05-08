import re
from bs4 import NavigableString
from root.general_tools.tools import getHtmlResponse, getSoup, load_country_context, getDomainTitle, get_google_pin_address, getGoogleMatchedData, find_emails, purify_emails, find_addresses, purify_addresses, find_phones, purify_phones
#from mylib.mymodules import validate_domain
#from mylib.mymodules import fixed_title, save_logo

# Functions
def find_second_page_url(main_page_soup, url, country_context):
    body = main_page_soup.body
    if(body):
        if(url[-1] == "/"):
            url = url[:-1]
        second_page_url = None
        anchors = body.find_all(href=True)
        found = False
        for txt in country_context.get('contact_text'):
            t_ignore_case = re.compile(txt, re.IGNORECASE)
            for a in anchors:
                a_text = a.get_text()
                found_txt = re.search(t_ignore_case, a_text)
                if found_txt:
                    h = a['href']
                    h = h.strip()
                    # avoid emails as second page url
                    if h.find('@') != -1:
                        continue
                    if(len(h) > 0):
                        found = True
                        if (h[0] == '/'):
                            second_page_url = url + h
                        elif re.search("http", h):
                            second_page_url = h
                        else:
                            second_page_url = url + "/" + h
                        break
            if found:
                break
        return second_page_url
    else:
        return None

def get_website_logo(soup_obj):
    if(soup_obj):
        body = soup_obj.body
        if(body):
            img = body.find('img')
            if img:
                return img.get('src')
            else:
                return None
        else:
            return None

def get_page_social_links(soup_obj):
    social = {}
    if(soup_obj):
        links = soup_obj.find_all('a')
        for l in links:
            h = l.get('href')
            if h:
                if re.search('facebook.com', h):
                    social['facebook'] = h
                if re.search('instagram.com', h):
                    social['instagram'] = h
                if re.search('linkedin.com', h):
                    social['linkedin'] = h
                if re.search('twitter.com', h):
                    social['twitter'] = h
                if re.search('youtube.com', h):
                    social['youtube'] = h
    return social


def get_website_data(main_page_soup, contact_page_soup, country, country_context, domain, url, org_name, language):
    website_data = {}
    # get and save website logo
    
    logo_url = get_website_logo(main_page_soup)
    if(logo_url):
        website_data["logo_url"] = logo_url
    '''
        print(logo_url)
        ext = logo_url[-3:].lower()
        if ext in ['peg', 'png', 'png']:
            website_data['saved_logo'] = save_logo(logo_url, domain)
    
    # get website title
    main_page_title = fixed_title(main_page_soup, domain)
    if main_page_title:
        website_data['web_title'] = main_page_title  
    '''
    web_title = getDomainTitle(domain)
    if(web_title):
        website_data['web_title'] = web_title
    # get website social links
    main_page_social_links = get_page_social_links(main_page_soup)
    contact_page_social_links = get_page_social_links(contact_page_soup)
    
    # merge social links
    for key in contact_page_social_links.keys():
        main_page_social_links[key] = contact_page_social_links[key]
    website_data["social_pages"] = main_page_social_links

    # get addresses, phones and emails
    website_data["phones"] = []
    website_data["emails"] = []
    website_data["addresses"] = []

    if(contact_page_soup):
        text = "\n".join(string for string in contact_page_soup.stripped_strings)
        website_data["addresses"] = find_addresses(text[:20000], country_context["address_patterns"], country, is_contact_page=True)
        google_pin_address = get_google_pin_address(contact_page_soup, url, language)

        website_data["addresses"] += google_pin_address

        website_data["phones"] = find_phones(text, country_context["phone_patterns"], country)
        website_data["emails"] = find_emails(text)

    if(main_page_soup):
        text = "\n".join(string for string in main_page_soup.stripped_strings)
        website_data["addresses"] += find_addresses(text[:20000], country_context["address_patterns"], country)

        google_pin_address = get_google_pin_address(main_page_soup, url, language)
        website_data["addresses"] += google_pin_address

        website_data["phones"] += find_phones(text, country_context["phone_patterns"], country)
        website_data["emails"] += find_emails(text)
    
    # purify addresses, phones and emails
    if(website_data["addresses"]):
        website_data["addresses"] = purify_addresses(website_data["addresses"], country, "company-website")
        
    if(not website_data["addresses"]):
        print("No address from website, Using google API ...")
        google_data = getGoogleMatchedData(org_name, domain, language)
        if(google_data):
            website_data["addresses"].append({"source": "google_geo_api", "address":google_data["formatted_address"], "components":google_data["address_components"]})
    
    if(website_data["phones"]):
        website_data["phones"] = purify_phones(website_data["phones"], country)
    
    if(website_data["emails"]):
        website_data["emails"] = purify_emails(website_data["emails"])

    return website_data

def website_info(domain, org_name, country="global"):
    #domain = validate_domain(domain)
    print('>>>>>>>>>>>>>>>>>> NOW website_info: ', domain, 'Country :', country)
    if domain:
        url = "http://" + domain
        print("url >>> ", url)
    else:
        return {"domain": domain, "result": {}}
    
    country_context = load_country_context(country, add_with_global_setting=False) if country else load_country_context("global")
    language = country_context.get("language", "en")
    # getting main-page and contact-page soup object
    main_page_soup = None
    contact_page_soup = None
    res = getHtmlResponse(url, use_proxy=False)
    if(res):
        print("status code >>> ", res.status_code)
        final_url = res.url
        print("final_url: ", final_url)
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
    
    # getting website data using main-page and contact page
    if(main_page_soup):
        website_data = get_website_data(main_page_soup, contact_page_soup, country, country_context, domain, url, org_name, language)
        return {"domain": domain, "result": website_data}
    else:
        return {"domain": domain, "result": {}}

