import re
import requests

from root.general_tools.tools import getHtmlResponse, getSoup, make_soup, save_logo, get_google_formatted_address_using_address

from googletrans import Translator
translator = Translator()

def facebook_adress(soup):
    res = soup.select('._5aj7._20ud ._2iem')
    sss = ''
    for i in res:
        sss += i.get_text()
    return sss

def facebook_email(soup, email_validation=False):
    res = soup.select('._50f4')
    email_list = []
    for i in res:
        ss = i.get_text()
        facebook_re = re.findall(r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9-\.\-_]+\.[a-zA-Z\.]+', ss)
        if facebook_re:
            email_list = facebook_re
    return email_list
    '''
    if email_validation:
        result = email_list_verifier(email_list)
    else:
        result = email_list
    return result
    '''

def facebook_phone(soup):
    res = soup.select('._50f4')
    sss = ''
    for i in res:
        if 'Call' in i.get_text():
            sss += i.get_text()
    return sss[5:]

def facebook_foundation_year(soup):
    res = soup.select('._4bl9')
    a = ''
    for i in res:
        text = i.get_text()

        if 'found' in text.lower():
            text2 = re.findall('[1-2]\d{3}', text)
            if text2 == []:
                a = ''
            else:
                a = text2[0]
            break

    return str(a)

def facebook_logo(url):
    if url[-1] != '/':
        url += '/'

    if 'pg/' in url:
        index1 = url.index('pg/')
        fb = url[index1 + 3:]
        index2 = fb.index('/')
        fb_id = fb[:index2]
    else:
        fb_id_index = url.index('facebook.com/')

        fb_id2 = url[fb_id_index + 13:]

        if '/' in fb_id2:
            index2 = fb_id2.index('/')
            fb_id = fb_id2[:index2]
        else:

            fb_id = fb_id2

    return 'http://graph.facebook.com/' + fb_id + '/picture?type=large'

def facebook_industry(soup):
    res = soup.select('._5m_o')
    sss = ''
    try:
        sss = res[0].get_text()
    except:
        pass
    return sss

def facebook_more_info(soup):
    mi = soup.find('div', text= re.compile('MORE INFO'))
    result = ''
    if mi:
        tag = mi.next_sibling
        txt = tag.get_text()
        if txt:
            result = txt.replace('About', '')

    return result


def facebook_info(fb_url, domain, email_validation=False):
    print('>>>>>>>>>>>>>>>>>> NOW FACEBOOK INFO: ', fb_url)
    soup = make_soup(fb_url, use_proxy=True)
    fb_phone, fb_address, fb_email, fb_foundation_year, fb_industry, fb_logo, saved_logo, fb_more = '', '', '', '', '', '', '', ''

    link = soup.find('div', attrs={"data-key": "tab_about"})
    if link:
        about_link = f"https://www.facebook.com{link.a['href']}"
        about_soup = make_soup(about_link, use_proxy=True)
        
        fb_phone = facebook_phone(about_soup)
        fb_address = facebook_adress(about_soup)
        fb_email = facebook_email(about_soup, email_validation=email_validation)
        fb_foundation_year = facebook_foundation_year(about_soup)
        fb_industry = facebook_industry(about_soup)
        fb_logo = facebook_logo(about_link)
        saved_logo = save_logo(fb_logo, domain)
        fb_more = facebook_more_info(about_soup)

    fb_data = {
        'URL': fb_url,
        'address': fb_address,
        'phone': fb_phone,
        'email': fb_email,
        'foundation': fb_foundation_year,
        'industry': fb_industry,
        'fb_logo': fb_logo,
        'saved_logo': saved_logo,
        'more_info': fb_more
        }
    return fb_data


def verify_facebook_link(link, domain, country, country_code):
    response = getHtmlResponse(link, use_proxy=True)
    if(response):
        soup = getSoup(response)
        if(soup):
            link = soup.find('div', attrs={"data-key": "tab_about"})
            if link:
                about_link = f"https://www.facebook.com{link.a['href']}"
                about_response = getHtmlResponse(about_link, use_proxy=True)
                if(about_response):
                    about_soup = getSoup(about_response)
                    if(about_soup):
                        fb_phone = facebook_phone(about_soup)
                        fb_address = facebook_adress(about_soup)
                        print(fb_phone, fb_address)

                        if(fb_phone):
                            phone = "".join(d for d in fb_phone if(re.search("\d", d)))
                            if(phone.startswith(country_code)):
                                phone_match_status = "matched"
                            else:
                                return False
                        else:
                            phone_match_status = "not_found"
                        
                        if(fb_address):
                            if(re.search(country, fb_address, flags=re.IGNORECASE)):
                                address_match_status = "matched"
                            else:
                                address_dic = get_google_formatted_address_using_address(fb_address, "en")
                                if(address_dic):
                                    address_country = translator.translate(address_dic["components"]["country"], dest="en").text
                                    if(country == address_country.lower()):
                                        address_match_status = "matched"
                                    else:
                                        return False
                                else:
                                    address_match_status = "not_found"
                        else:
                            address_match_status = "not_found"
                        
                        if(phone_match_status == "not_found" and address_match_status == "not_found"):
                            items = about_soup.select('._50f4')
                            if(items):
                                main_domain = domain.replace("www.", "")
                                main_domain = main_domain.split("/")[0]
                                for item in items:
                                    if(re.search(domain, item.text)):
                                        return True
                                return False
                            else:
                                return False
                        else:
                            return True
    return False