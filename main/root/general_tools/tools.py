# Imports
from bs4 import BeautifulSoup as bs
import requests
import re
import json
from root.general_tools.search_settings import *

from fake_useragent import UserAgent
ua = UserAgent()

# Variables
proxy_api_key = "a057568fadc410eeffbfa8c72a1149js" # new key

geocoding_search_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}&language={}'

place_search_by_geo_info = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=formatted_address&locationbias=circle:{}@{},{}&key={}&language={}"
place_search_by_place_id = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields={}&key={}&language={}"
place_search_by_query = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields={}&key={}&language={}"

place_api_key = "AIzaSyAURUorT5giGQqfBfcPqJmpYg2tHYOPL8g"
geocoding_api_key = 'AIzaSyAURUorT5giGQqfBfcPqJmpYg2tHYOPL8g'

from googletrans import Translator
translator = Translator()
#print(googletrans.LANGUAGES) # to see list of supported languages

COUNTRY_CONTEXTS = {
    "countries": {
        "usa": {
            "phone_phrases": [],
            "phone_patterns": ["\\+?\\d?[-\\.]?\\d{3}.\\d{3}.\\d{4}"],
            "address_patterns": ["address:.+", "Address:.+"],
            "contact_text": ["contact", "Contact"]
        },
        "global": {
            "phone_phrases": ["phone:", "Phone:", "Tel:"],
            "phone_patterns": ["\+?\d{1,3}[\s|\(]\(?\d{3,4}\)?\s\d{2,3}[\s\-\.]?\d{2}\-?\d{2}",
                               "\+\d{1,3}[\s\-]?\d{1,3}[\s\-]?\d{3,4}[\s\-]?\d{3,4}",
                               "\(\d{3}\)\s\d\s?\s?\s?\d\s?\d[\s\-]\d{4}",
                               "\(\+?\d+\)\s\d+[\s\-]\d{3}[\s\-]?\d+",
                               "\d{3}[\s\-]\d{3}[\s\-]\d{2}[\s\-]?\d{2}"],
            "address_patterns": ["address:\w{,100}", "Address:\w{,100}"],
            "contact_text": ["contact", "contacto", "contacts", "contact us"]
        },
        "brazil": {
            "phone_phrases": ["telefone:", "fone:", "Fone:", "Telefone:"],
            "phone_patterns": [
                "(\+?(\d{2}\s)?\(?\d{2,3}\)?(\)|\s|-|\.)\s?(-|\.)?\s?\d{2,3}\s?(-|\.)?\s?\d{2}(\s|-|\.)\s?(-|\.)?\s?\d{2}\s?(-|\.)?\s?\d{2})",
                "(\d{4}\s?(-|\.)?\s?\d{3}\s?(-|\.)?\s?\d{2}\s?(-|\.)?\s?\d{2}\s?(-|\.)?\s?)",
                "(\(?\d{2}\)?\s?(-|\.)?\s?\d{9})",
            ],
            "address_patterns": [
                "(" + 
                    "(" + 
                        "(AV\.?\W)|(Av\.?\W)|((?<!\w)av\.?\W)|(Avenida)|(AVENIDA)|(avenida)|" +
                        "(RUA\W)|(Rua\W)|((?<!\w)R\.)|(rua\W)|" + 
                        "(Rod\W)|(ROD\W)|(Rodovia)|(RODOVIA)|" + 
                        "(Praça)|(praça)|(PRAÇA)" + 
                    ")" +   
                    "[\w\s\.\|\-\(\):,–]{5,120}" +
                    "(" + 
                        "(Brasil)|(BRASIL)|(brasil)|(Brazil)|(BRAZIL)|" + 
                        "(\D\d{2}\D?\d{3}(-|–)\d{3}\D)|" + 
                        "(\WAC\W)|(\WAL\W)|(\WAM\W)|(\WAP\W)|(\WBA\W)|(\WCE\W)|(\WDF\W)|(\WES\W)|(\WGO\W)|(\WMA\W)|(\WMG\W)|(\WMS\W)|(\WMT\W)|(\WPA\W)|" +
                        "(\WPB\W)|(\WPE\W)|(\WPI\W)|(\WPR\W)|(\WRJ\W)|(\WRN\W)|(\WRO\W)|(\WRR\W)|(\WRS\W)|(\WSC\W)|(\WSE\W)|(\WSP\W)|(\WTO\W)|" + 
                        "(Acre)|(ACRE)|(acre)|(Alagoas)|(ALAGOAS)|(alagoas)|(Amazonas)|(AMAZONAS)|(amazonas)|(Amapá)|(AMAPÁ)|(amapá)|(Bahia)|(BAHIA)|(bahia)|" + 
                        "(Ceará)|(CEARÁ)|(ceará)|(Distrito Federal)|(DISTRITO FEDERAL)|(distrito federal)|(Espírito Santo)|(ESPÍRITO SANTO)|(espírito santo)|" + 
                        "(Goiás)|(GOIÁS)|(goiás)|(Maranhão)|(MARANHÃO)|(maranhão)|(Minas Gerais)|(MINAS GERAIS)|(minas gerais)|" + 
                        "(Mato Grosso do Sul)|(MATO GROSSO DO SUL)|(mato grosso do sul)|(Mato Grosso)|(MATO GROSSO)|(mato grosso)|(Pará)|(PARÁ)|(pará)|" + 
                        "(Paraíba)|(PARAÍBA)|(paraíba)|(Pernambuco)|(PERNAMBUCO)|(pernambuco)|(Piauí)|(PIAUÍ)|(piauí)|(Paraná)|(PARANÁ)|(paraná)|" + 
                        "(Rio de Janeiro)|(RIO DE JANEIRO)|(rio de janeiro)|(Rio Grande do Norte)|(RIO GRANDE DO NORTE)|(rio grande do norte)|" + 
                        "(Rondônia)|(RONDÔNIA)|(rondônia)|(Roraima)|(RORAIMA)|(roraima)|(Rio Grande do Sul)|(RIO GRANDE DO SUL)|(rio grande do sul)|" + 
                        "(Santa Catarina)|(SANTA CATARINA)|(santa catarina)|(Sergipe)|(SERGIPE)|(sergipe)|(São Paulo)|(SÃO PAULO)|(são paulo)|" + 
                        "(Tocantins)|(TOCANTINS)|(tocantins)" +
                    ")" + 
                ")",
            ],
            "contact_text": ["contato", "Fale Conosco", "Contatos"]
        },
        "china": {
            "phone_phrases": ["电话"],
            "phone_patterns": [],
            "address_patterns": ["地址"],
            "contact_text": ["联系方式", "联系我们"]
        },
        "russia": {
            "phone_phrases": ["Телефон"],
            "phone_patterns": [
                "(?<!\d)(\+?\s?\d?[\-\.\s]*\(?\s?\d{3}[\)\-\.\s]+\d{3}[\-\.\s]*\d{2}[\-\.\s]*\d{2})(?!\d)",
                "(?<!\d)(\+?\s?\d?[\-\.\s]*\(?\s?\d{4}[\)\-\.\s]+\d{3}[\-\.\s]*\d{3})(?!\d)",
                "(?<!\d)(\+?\s?\d?[\-\.\s]*\(?\s?\d{4}[\)\-\.\s]+\d{2}[\-\.\s]*\d{2}[\-\.\s]*\d{2})(?!\d)",
                "(?<!\d)(\+?\s?\d?[\-\.\s]*\(?\d{3}[\)\-\.\s]+\d{3}[\-\.\s]*\d[\-\.\s]*\d{3})(?!\d)",
            ],
            "address_patterns": [
                "(" +
                    "(" +
                        "((?<!\d)\d{6}(?!\d))|" +
                        "((?<!\w)Г\.\s?[\w\-]{3,})|" +
                        "([\w\-]+\sОБЛ[\s\.,]+)|([\w\-]+\sОБЛАСТЬ\W)|" +
                        "([\w\-]+\sРЕСП[\s\.,]+)|([\w\-]+\sРЕСПУБЛИКА\W)|" +
                        "([\w\-]+\sКР[\s\.,]+)|([\w\-]+\sКРАЙ\W)|" +
                        "([\w\-]+\sокр.)" +
                    ")" +
                    "([\w\s:,\|\.\-/–;]{,70})" +
                    "(" +
                        "((офис\s[\w\./]{,15}(\-?\s?[\w\.\-/]{,15})?)|((?<!\w)оф[\s\.]+[\w\./]{,15}(\-?\s?[\w\.\-/]{,15})?))|" +
                        "((кв\.\s?[\w]{,15})|(КВАРТИРА\s[\w]{,15}))|" +
                        "(((?<!\w)дом\s[\w\.\-/]{,15})|((?<!\w)д[\s\.]+[\w\.\-/]{,15}))|" +
                        "(((?<!\w)ком[\s\.]+[\w\./]{,15}(\-?\s?[\w\.\-/]{,15})?)|(КОМНАТА\s[\w\.\-/]{,8})|(КОМН\s?[\w\./]{,15}(\-?\s?[\w\.\-/]{,15})?))|" +
                        "(((?<!\w)пом[\s\.]+[\w\./]{,15}(\-?\s?[\w\.\-/]{,15})?)|(помещение\s[\w\./]{,15}(\-?\s?[\w\.\-/]{,15})?))|" +
                        "((этаж\s[\w\.\-/]{,15})|((?<!\w)эт[\s\.]+[\w\.\-/]{,15}))|" +
                        "((строение\s[\w\.\-/]{,15})|((?<!\w)стр\.\s?[\w\.\-/]{,15}))|" +
                        "(((?<!\w)к[\s\.]+[\w\.\-/]{,15})|((?<!\w)каб[\s\.]+[\w\.\-/]{,15})|(кабинет\s[\w\.\-/]{,15}))|" +
                        "((корп[\s\.]+[\w\.\-/]{,15})|(корпус\s[\w\.\-/]{,15}))|" +
                        "((литера?\s[\w\.\-/]{,15})|((?<!\w)лит[\s\.]+[\w\.\-/]{,15}))|" +
                        "((?<!\w)П[\.\s]+[\w\.\-/]{,15})|" +
                        "(№\s?[\w\.\-]{,15})|" +
                        "(((?<!\w)ул[\s\.]+[\w\./]{,25}(\-?\s?[\w\.\-/]{,25})?)|(улица\s[\w\./]{,25}(\-?\s?[\w\.\-/]{,25})?))|" +
                        "(КО\.\s?[\w\.\-]{,15})|" +
                        "(пос\.\s?[\w\.\-]{,25})|" +
                        "(владение\s[\w\.\-]{,25})|" +
                        "(помещения\s[\w\.\-]{,25})|" +
                        "((?<!\w)г\.\s?[\w\.\-]{,25})|" +
                        "((?<!\w)с\.\s?[\w\.\-]{,25})|" +
                        "((?<!\w)рп\.\s?[\w\.\-]{,25})|" +
                        "((?<!\w)пер\.\s?[\w\.\-]{,25})" +
                    ")" +
                    "(\s?,\s?[\w\.\-/]+)?" +
                ")",
            ],
            "contact_text": ["КОНТАКТЫ", "Контакты", "contact"]
        },
        "india": {
            "phone_phrases": [],
            "phone_patterns": [
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{3}[\s\-\.–]{1,3}\d{8}",
                    "(?<!\d)\(?\+?\d{3}\)?[\s\-\.–]{1,3}\d{8}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{2}[\s\-\.–]{1,3}\d{8}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{2}[\s\-\.–]{1,3}\d{4}[\s\-\.–]{1,3}\d{4}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{10}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{5}[\s\-\.–]{1,3}\d{5}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{4}[\s\-\.–]{1,3}\d{3}[\s\-\.–]{1,3}\d{3}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{3}[\s\-\.–]{1,3}\d{4}[\s\-\.–]{1,3}\d{3}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{3}[\s\-\.–]{1,3}\d{3}[\s\-\.–]{1,3}\d{4}",
                    "(?<!\d)\(?\+?\d{2}\)?[\s\-\.–]{1,3}\d{2}[\s\-\.–]{1,3}\d{7}(?!\d)",
                    "(?<!\d)\(?\+?\d{4}\)?[\s\-\.–]{1,3}\d{7}",
                ],
            "address_patterns": [
                "(" +
                    "(" +
                        "(address(?!\w)\s?:?)|" +
                        "(#\s?\d)|" +
                        "(plot(?!\w))|" +
                        "(([^\n]{2,35}\s?,\s?)?[\w\-]+\s*(\n\s*th\s*\n)?\s*(?<!\w)floor(?!\w))|" +
                        "(office\s?:)|" +
                        "(Centre\s?:)|"
                        "(no\.\s?\d)|" +
                        "([^\n]{2,35}street(?!\w))|" +
                        "([^\n]{2,35}road(?!\w))|" +
                        "([^\n]{2,35}Rd(?!\w))|" +
                        "([^\n]{2,35}highway(?!\w))" +
                    ")" +
                    "([\w\s:,\|\.\-/–\(\)&#'’]{10,140})" +
                    "(" +
                        "(india)|" +
                        "((?<!\d)\d{3}[\s\-\.]?\d{3}(?!\d))|" +
                        "((?<!\w)AP(?!\w))|((?<!\w)AR(?!\w))|((?<!\w)AS(?!\w))|((?<!\w)BR(?!\w))|((?<!\w)CG(?!\w))|((?<!\w)GA(?!\w))|((?<!\w)GJ(?!\w))|" +
                        "((?<!\w)HR(?!\w))|((?<!\w)HP(?!\w))|((?<!\w)JH(?!\w))|((?<!\w)KA(?!\w))|((?<!\w)KL(?!\w))|((?<!\w)MP(?!\w))|((?<!\w)MH(?!\w))|" +
                        "((?<!\w)MN(?!\w))|((?<!\w)ML(?!\w))|((?<!\w)MZ(?!\w))|((?<!\w)NL(?!\w))|((?<!\w)OD(?!\w))|((?<!\w)PB(?!\w))|((?<!\w)RJ(?!\w))|" +
                        "((?<!\w)SK(?!\w))|((?<!\w)TN(?!\w))|((?<!\w)TS(?!\w))|((?<!\w)TR(?!\w))|((?<!\w)UP(?!\w))|((?<!\w)UK(?!\w))|((?<!\w)WB(?!\w))|" +
                        "((?<!\w)AN(?!\w))|((?<!\w)CH(?!\w))|((?<!\w)DD(?!\w))|((?<!\w)DL(?!\w))|((?<!\w)JK(?!\w))|((?<!\w)LA(?!\w))|((?<!\w)LD(?!\w))|" +
                        "((?<!\w)PY(?!\w))|(Andhra Pradesh)|(Arunachal Pradesh)|(Assam)|(Bihar)|(Chhattisgarh)|(Goa)|(Gujarat)|(Haryana)|(Himachal Pradesh)|" +
                        "(Jharkhand)|(Karnataka)|(Kerala)|(Madhya Pradesh)|(Maharashtra)|(Manipur)|(Meghalaya)|(Mizoram)|(Nagaland)|(Odisha)|(Punjab)|" +
                        "(Rajasthan)|(Sikkim)|(Tamil Nadu)|(Telangana)|(Tripura)|(Uttar Pradesh)|(Uttarakhand)|(West Bengal)|(Andaman and Nicobar Islands)|"
                        "(Chandigarh)|(Dadra and Nagar Haveli and Daman and Diu)|(Delhi)|(Jammu and Kashmir)|(Ladakh)|(Lakshadweep)|(Puducherry)"
                    ")" +
                ")",
            ],
            "contact_text": ["contact", "contact us"]
        },
        "poland": {
            "phone_phrases": [],
            "phone_patterns": ["\d{2}[\s\-]\d{3}[\s\-]\d{2}[\s\-]\d{2}"],
            "address_patterns": [],
            "contact_text": ["Skontaktuj", "Skontaktuj się z nami"]
        },
        "spain": {
            "phone_phrases": [],
            "phone_patterns": ["(\d{3}[\s\-]\d{3}[\s\-]\d{3})",
                               "(\+\d{2}[\s\-]\(?\d{2,3}\)[\s\-]\d{3,4}[\s\-]\d{3,4})",
                               "(\+\d{2}[\s\-]\d{3}[\s\-]\d\s?\d\s?\d\s?\d\s?\d\s?\d)"],
            "address_patterns": ["Av[\.]?\s.+"],
            "contact_text": ["contacta"]
        },
        "colombia": {
            "phone_phrases": ["Teléfono"],
            "phone_patterns": ["(\d{3}[\s\-]\d{3}[\s\-]\d{3})", "\(\+?\d+\)\s?\(\d+\)\s\d{3}[\s\-]?\d{,4}"],
            "address_patterns": ["Av[\.]?\s.+","Dirección:\s.+", "Calle[\s].+"],
            "contact_text": ["contactenos"]
        },
        "uae": {
            "phone_phrases": [],
            "phone_patterns": ["\+\d{3}\s\d\s\d{7}", "\d{2,3}[\s\-]\d{7}", "\+\d{3}\s\d\s\d{2}\s\d{2}\s\d{3}", "\+?\d{2,3}[\s\-]\d[\s\-]\d{3,4}[\s\-]\d{3,4}"],
            "address_patterns": ["Av[\.]?\s.+","Dirección:\s.+", "Calle[\s].+"],
            "contact_text": ["contactenos"]
        },
        "vietnam": {
            "phone_phrases": [],
            "phone_patterns": [
                "((?<!\d)\(?\+?\d{2}[\s\.\-]+\d{3}\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\+?\d{2}[\s\.\-]*\(?\d\)?([\s\.\-]*\d){10}(?!\d))",
                "((?<!\d)\(?\+?\d{2}[\s\.\-]+\d\)?([\s\.\-]*\d){10}(?!\d))",
                "((?<!\d)\(?\+?\d{2}\)?([\s\.\-]*\d){11}(?!\d))",
                "((?<!\d)\(?\+?\d{4}\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\(?\+?\d{2}[\s\.\-]+\d{2}\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\(?\+?\d{2}\)?[\s\.\-]+([\s\.\-]*\d){10}(?!\d))",
                "((?<!\d)\(?\+?\d{2}[\s\.\-]+\d{3}\)?([\s\.\-]*\d){7}(?!\d))",
                "((?<!\d)\(?\+?\d{2}[\s\.\-]+\d\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\+?\d[\s\.\-]+\(?\d{3}\)?([\s\.\-]*\d){7}(?!\d))",
                "((?<!\d)\+?\d{2}[\s\.\-]*\(?\d\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\(?\+?\d{2}\)?([\s\.\-]*\d){9}(?!\d))",
                "((?<!\d)\(?\+?\d{3}\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\(?\+?\d{4}\)?([\s\.\-]*\d){7}(?!\d))",
                "((?<!\d)\(?\+?\d{5}\)?([\s\.\-]*\d){6}(?!\d))",
                "((?<!\d)\(?\+?\d{2}\)?([\s\.\-]*\d){8}(?!\d))",
                "((?<!\d)\(?\+?\d{3}\)?([\s\.\-]*\d){7}(?!\d))",
                "((?<!\d)\(?\+?\d{4}\)?([\s\.\-]*\d){6}(?!\d))",
            ],
            "address_patterns": [
                "(" +
                    "(" +
                        "(Địa chỉ\s?:?)|(Điạ chỉ\s?:?)|" +
                        "(Văn phòng\s?:?)|(văn phòng mới\s:?)|(trụ sở\s?:?)|(Trụ sở chính\s?:?)|(xưởng mộc\s?:?)|(xưởng mộc chính\s?:?)|" +
                        "(Tổng kho\s?:?)|(Miền Trung\s?:?)|(VPGD\s?:?)|(VPDD\s?:?)|(Xưởng sản xuất\s?:?)|" +
                        "(Tầng\s)|" +
                        "(Số\s\d)|(Tòa\snhà)|(Toà\snhà)|(Lầu\s)|(Lô\s)|(KCN\s)|((\S+\s)?Đường\s)|((\S+\s)?Trần)|(Ngõ\s)|" +
                        "((?<!\d)\d[\w\s\-/]{1,25}[\s\-,]+Phường\s)|(Km\s?\d+)|(Khu\s)|(phòng\s\d)" +
                    ")" +
                    "(" +
                        "[\w\s\-\.\|\+,/–]{15,90}" +
                    ")" +
                    "(" +
                        "((Việt Nam)|(Vietnam))|" +
                        "((Hồ Chí Minh)|(TP[\.\s]{1,2}Hồ Chí Minh))|" +
                        "(((?<!\w)HCM(?!\w))|(TP[\.\s]{,2}HCM))|" +
                        "((Hà Nội)|(TP[\.\s]{1,2}Hà Nội))|" +
                        "(((?<!\w)HN(?!\w))|(TP[\.\s]{,2}HN))|" +
                        "((Cần Thơ)|(TP[\.\s]{1,2}Cần Thơ))|" +
                        "((Đà Nẵng)|(TP[\.\s]{1,2}Đà Nẵng))|" +
                        "((Hải phòng)|(TP[\.\s]{1,2}Hải phòng))|" +
                        "((An Giang)|(TP[\.\s]{1,2}An Giang))|" +
                        "(((Bà Rịa\s?-?\s?)?Vũng Tàu)|(TP[\.\s]{1,2}(Bà Rịa\s?-?\s?)?Vũng Tàu))|" +
                        "((Bắc Giang)|(TP[\.\s]{1,2}Bắc Giang))|" +
                        "((Bắc Kạn)|(TP[\.\s]{1,2}Bắc Kạn))|" +
                        "((Bạc Liêu)|(TP[\.\s]{1,2}Bạc Liêu))|" +
                        "((Bắc Ninh)|(TP[\.\s]{1,2}Bắc Ninh))|" +
                        "((Bến Tre)|(TP[\.\s]{1,2}Bến Tre))|" +
                        "((Bình Định)|(TP[\.\s]{1,2}Bình Định))|" +
                        "((Bình Dương)|(TP[\.\s]{1,2}Bình Dương)|((?<!\w)BD(?!\w))|(TP[\.\s]{,2}BD))|" +
                        "((Bình Phước)|(TP[\.\s]{1,2}Bình Phước))|" +
                        "((Bình Thuận)|(TP[\.\s]{1,2}Bình Thuận))|" +
                        "((Cà Mau)|(TP[\.\s]{1,2}Cà Mau))|" +
                        "((Cao Bằng)|(TP[\.\s]{1,2}Cao Bằng))|" +
                        "((Đắk Lắk)|(TP[\.\s]{1,2}Đắk Lắk)|(Đăk Lăk)|(TP[\.\s]{1,2}Đăk Lăk))|" +
                        "((Đắk Nông)|(TP[\.\s]{1,2}Đắk Nông))|" +
                        "((Điện Biên)|(TP[\.\s]{1,2}Điện Biên))|" +
                        "((Đồng Nai)|(TP[\.\s]{1,2}Đồng Nai))|" +
                        "((Đồng Tháp)|(TP[\.\s]{1,2}Đồng Tháp))|" +
                        "((Gia Lai)|(TP[\.\s]{1,2}Gia Lai))|" +
                        "((Hà Giang)|(TP[\.\s]{1,2}Hà Giang))|" +
                        "((Hà Nam)|(TP[\.\s]{1,2}Hà Nam))|" +
                        "((Hà Tĩnh)|(TP[\.\s]{1,2}Hà Tĩnh))|" +
                        "((Hải Dương)|(TP[\.\s]{1,2}Hải Dương))|" +
                        "((Hậu Giang)|(TP[\.\s]{1,2}Hậu Giang))|" +
                        "((Hòa Bình)|(TP[\.\s]{1,2}Hòa Bình))|" +
                        "((Hưng Yên)|(TP[\.\s]{1,2}Hưng Yên))|" +
                        "((Khánh Hòa)|(TP[\.\s]{1,2}Khánh Hòa))|" +
                        "((Kiến Giang)|(TP[\.\s]{1,2}Kiến Giang))|" +
                        "((Kon Tum)|(TP[\.\s]{1,2}Kon Tum))|" +
                        "((Lai Châu)|(TP[\.\s]{1,2}Lai Châu))|" +
                        "((Lâm Đồng)|(TP[\.\s]{1,2}Lâm Đồng))|" +
                        "((Lạng Sơn)|(TP[\.\s]{1,2}Lạng Sơn))|" +
                        "((Lào Cai)|(TP[\.\s]{1,2}Lào Cai))|" +
                        "((Long An)|(TP[\.\s]{1,2}Long An))|" +
                        "((Nam Định)|(TP[\.\s]{1,2}Nam Định))|" +
                        "((Nghệ An)|(TP[\.\s]{1,2}Nghệ An))|" +
                        "((Ninh Bình)|(TP[\.\s]{1,2}Ninh Bình))|" +
                        "((Ninh Thuận)|(TP[\.\s]{1,2}Ninh Thuận))|" +
                        "((Phú Thọ)|(TP[\.\s]{1,2}Phú Thọ))|" +
                        "((Phú Yên)|(TP[\.\s]{1,2}Phú Yên))|" +
                        "((Quảng Bình)|(TP[\.\s]{1,2}Quảng Bình))|" +
                        "((Quảng Nam)|(TP[\.\s]{1,2}Quảng Nam))|" +
                        "((Quảng Ngãi)|(TP[\.\s]{1,2}Quảng Ngãi))|" +
                        "((Quảng Ninh)|(TP[\.\s]{1,2}Quảng Ninh))|" +
                        "((Quảng Trị)|(TP[\.\s]{1,2}Quảng Trị))|" +
                        "((Sóc Trăng)|(TP[\.\s]{1,2}Sóc Trăng))|" +
                        "((Sơn La)|(TP[\.\s]{1,2}Sơn La))|" +
                        "((Tây Ninh)|(TP[\.\s]{1,2}Tây Ninh))|" +
                        "((Thái Bình)|(TP[\.\s]{1,2}Thái Bình))|" +
                        "((Thái Nguyên)|(TP[\.\s]{1,2}Thái Nguyên))|" +
                        "((Thanh Hóa)|(TP[\.\s]{1,2}Thanh Hóa))|" +
                        "((Thừa Thiên-Huế)|(TP[\.\s]{1,2}Thừa Thiên-Huế))|" +
                        "((Tiền Giang)|(TP[\.\s]{1,2}Tiền Giang))|" +
                        "((Trà Vinh)|(TP[\.\s]{1,2}Trà Vinh))|" +
                        "((Tuyên Quang)|(TP[\.\s]{1,2}Tuyên Quang))|" +
                        "((Vĩnh Long)|(TP[\.\s]{1,2}Vĩnh Long))|" +
                        "((Vĩnh Phúc)|(TP[\.\s]{1,2}Vĩnh Phúc))|" +
                        "((Yên Bái)|(TP[\.\s]{1,2}Yên Bái))|" +
                        "((Quận\s(\w+\s?){1,2})|(Huyện\s(\w+\s?){1,2})|(Q[\.\s]+(\w+\s?){1,2}))" +
                    ")" +
                ")"
            ],
            "contact_text": ["Liên hệ", "CONTACT US", "contact"]
        },
        "mexico": {
            "phone_phrases": [],
            "phone_patterns": [
                "(\+?\d{2}\s?[\.\-]?\s?\(?\d{2}\)?\s?[\.\-]?\s?\d{4}\s?[\.\-]?\s?\d{4})",
                "(\+?\d{2}\s?[\.\-]?\s?\(?\d{3}\)?\s?[\.\-]?\s?\d{3}\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{2})",
                "(\+?\d{2}\s?[\.\-]?\s?\(?\d{3}\)?\s?[\.\-]?\s?\d{3}\s?[\.\-]?\s?\d{4})",
                "(\+?\d{2}\s?[\.\-]?\s?\(?\d{1}\)?\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{4}\s?[\.\-]?\s?\d{4})",
                "(\+?\d{2}\s?[\.\-]?\s?\(?\d{3}\)?\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{3}\s?[\.\-]?\s?\d{2})",
                "(\+?\d{2}\s?[\.\-]?\s?\d{10})",
                "(\(?\d{3}\)?\s?[\.\-]?\s?\d{3}\s?[\.\-]?\s?\d{4})",
                "(\(?\d{3}\)?\s?[\.\-]?\s?\d{3}\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{2})",
                "(\(?\d{3}\)?\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{3})",
                "(\(?\d{2}\)?\s?[\.\-]?\s?\d{4}\s?[\.\-]?\s?\d{4})",
                "(\(?\d{2}\)?\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{2}\s?[\.\-]?\s?\d{2})"
            ],
            "address_patterns": [
                "(" + 
                    "(" + 
                        "(Blvd\.)|(Blvrd\.)|(Calle)|(Av\.?(?!\w))|(AVENIDA)|" + 
                        "(Avda\.)|(Cuarta)|((?<!\w)\w[ #\w\.\-,]{,25}Col\.)|" + 
                        "(Calz\.)|([^\n]{,30}s/n)|(Piso)|(Cd\.)|" + 
                        "(DIRECCIÓN\s?:?)|(address\s?:)|(Oficina\s?:?)" +
                    ")" + 
                    "(" + 
                        "[/,;\w\s\-\|\.]{5,120}" + 
                    ")" + 
                    "(" + 
                        "(México)|(Mexico)|" + 
                        "(c\.p\.\s?\d{5})|(cp\.\s?\d{5})|((?<!\w)\d{5}(?!\w))|" + 
                        "(Ags\.)|(Aguascalientes)|(B\.C\.)|(BC\.)|(Baja California)|(B\.C\.S\.)|(BCS\.)|(Baja California Sur)|(Camp\.)|(Campeche)|(Chis\.)|(Chiapas)|" + 
                        "(Chih\.)|(Chihuahua)|(Coah\.)|(Coahuila)|(Col\.)|(Colima)|(CDMX)|(Mexico City)|(Dgo\.)|(Durango)|(Gto\.)|(Guanajuato)|(Gro\.)|(Guerrero)|" + 
                        "(Jal\.)|(Jalisco)|(Hgo\.)|(Hidalgo)|(Méx\.)|(Mich\.)|(Michoacán)|(Mor\.)|(Morelos)|(Nay\.)|(Nayarit)|(N\.L\.)|(NL\.)|(Nuevo León)|(Oax\.)|(Oaxaca)" + 
                        "(Pue\.)|(Puebla)|(Qro\.)|(Querétaro)|(Q\.R\.)|(QR\.)|(Quintana Roo)|(S\.L\.P\.)|(SLP\.)|(San Luis Potosí)|(Sin\.)|(Sinaloa)|(Son\.)|(Sonora)|" + 
                        "(Tab\.)|(Tabasco)|(Tamps\.)|(Tamaulipas)|(Tlax\.)|(Tlaxcala)|(Ver\.)|(Veracruz)|(Yuc\.)|(Yucatán)|(Zac\.)|(Zacatecas)" + 
                    ")" + 
                ")"
            ],
            "contact_text": ["Contacto", "Contactanos", "CONTACT"]
        }
    }
}

country_dial_codes = {
    "israel": "972",
    "afghanistan": "93",
    "albania": "355",
    "algeria": "213",
    "americansamoa": "1684",
    "andorra": "376",
    "angola": "244",
    "anguilla": "1264",
    "antigua and barbuda": "1268",
    "argentina": "54",
    "armenia": "374",
    "aruba": "297",
    "australia": "61",
    "austria": "43",
    "azerbaijan": "994",
    "bahamas": "1242",
    "bahrain": "973",
    "bangladesh": "880",
    "barbados": "1246",
    "belarus": "375",
    "belgium": "32",
    "belize": "501",
    "benin": "229",
    "bermuda": "1441",
    "bhutan": "975",
    "bosnia and herzegovina": "387",
    "botswana": "267",
    "brazil": "55",
    "british indian ocean territory": "246",
    "bulgaria": "359",
    "burkina faso": "226",
    "burundi": "257",
    "cambodia": "855",
    "cameroon": "237",
    "canada": "1",
    "cape verde": "238",
    "cayman islands": "345",
    "central african republic": "236",
    "chad": "235",
    "chile": "56",
    "china": "86",
    "christmas island": "61",
    "colombia": "57",
    "comoros": "269",
    "congo": "242",
    "cook islands": "682",
    "costa rica": "506",
    "croatia": "385",
    "cuba": "53",
    "cyprus": "537",
    "czech republic": "420",
    "denmark": "45",
    "djibouti": "253",
    "dominica": "1767",
    "dominican republic": "1849",
    "ecuador": "593",
    "egypt": "20",
    "el salvador": "503",
    "equatorial guinea": "240",
    "eritrea": "291",
    "estonia": "372",
    "ethiopia": "251",
    "faroe islands": "298",
    "fiji": "679",
    "finland": "358",
    "france": "33",
    "french guiana": "594",
    "french polynesia": "689",
    "gabon": "241",
    "gambia": "220",
    "georgia": "995",
    "germany": "49",
    "ghana": "233",
    "gibraltar": "350",
    "greece": "30",
    "greenland": "299",
    "grenada": "1473",
    "guadeloupe": "590",
    "guam": "1671",
    "guatemala": "502",
    "guinea": "224",
    "guinea-bissau": "245",
    "guyana": "595",
    "haiti": "509",
    "honduras": "504",
    "hungary": "36",
    "iceland": "354",
    "india": "91",
    "indonesia": "62",
    "iraq": "964",
    "ireland": "353",
    "italy": "39",
    "jamaica": "1876",
    "japan": "81",
    "jordan": "962",
    "kazakhstan": "77",
    "kenya": "254",
    "kiribati": "686",
    "kuwait": "965",
    "kyrgyzstan": "996",
    "latvia": "371",
    "lebanon": "961",
    "lesotho": "266",
    "liberia": "231",
    "liechtenstein": "423",
    "lithuania": "370",
    "luxembourg": "352",
    "madagascar": "261",
    "malawi": "265",
    "malaysia": "60",
    "maldives": "960",
    "mali": "223",
    "malta": "356",
    "marshall islands": "692",
    "martinique": "596",
    "mauritania": "222",
    "mauritius": "230",
    "mayotte": "262",
    "mexico": "52",
    "monaco": "377",
    "mongolia": "976",
    "montenegro": "382",
    "montserrat": "1664",
    "morocco": "212",
    "myanmar": "95",
    "namibia": "264",
    "nauru": "674",
    "nepal": "977",
    "netherlands": "31",
    "netherlands antilles": "599",
    "new caledonia": "687",
    "new zealand": "64",
    "nicaragua": "505",
    "niger": "227",
    "nigeria": "234",
    "niue": "683",
    "norfolk island": "672",
    "northern mariana islands": "1670",
    "norway": "47",
    "oman": "968",
    "pakistan": "92",
    "palau": "680",
    "panama": "507",
    "papua new guinea": "675",
    "paraguay": "595",
    "peru": "51",
    "philippines": "63",
    "poland": "48",
    "portugal": "351",
    "puerto rico": "1939",
    "qatar": "974",
    "romania": "40",
    "rwanda": "250",
    "samoa": "685",
    "san marino": "378",
    "saudi arabia": "966",
    "senegal": "221",
    "serbia": "381",
    "seychelles": "248",
    "sierra leone": "232",
    "singapore": "65",
    "slovakia": "421",
    "slovenia": "386",
    "solomon islands": "677",
    "south africa": "27",
    "south georgia and the south sandwich islands": "500",
    "spain": "34",
    "sri lanka": "94",
    "sudan": "249",
    "suriname": "597",
    "swaziland": "268",
    "sweden": "46",
    "switzerland": "41",
    "tajikistan": "992",
    "thailand": "66",
    "togo": "228",
    "tokelau": "690",
    "tonga": "676",
    "trinidad and tobago": "1868",
    "tunisia": "216",
    "turkey": "90",
    "turkmenistan": "993",
    "turks and caicos islands": "1649",
    "tuvalu": "688",
    "uganda": "256",
    "ukraine": "380",
    "united arab emirates": "971",
    "united kingdom": "44",
    "united states": "1",
    "uruguay": "598",
    "uzbekistan": "998",
    "vanuatu": "678",
    "wallis and futuna": "681",
    "yemen": "967",
    "zambia": "260",
    "zimbabwe": "263",
    "land islands": "",
    "antarctica": "",
    "bolivia, plurinational state of": "591",
    "brunei darussalam": "673",
    "cocos (keeling) islands": "61",
    "congo, the democratic republic of the": "243",
    "cote d'ivoire": "225",
    "falkland islands (malvinas)": "500",
    "guernsey": "44",
    "holy see (vatican city state)": "379",
    "hong kong": "852",
    "iran, islamic republic of": "98",
    "isle of man": "44",
    "jersey": "44",
    "korea, democratic people's republic of": "850",
    "korea, republic of": "82",
    "lao people's democratic republic": "856",
    "libyan arab jamahiriya": "218",
    "macao": "853",
    "macedonia, the former yugoslav republic of": "389",
    "micronesia, federated states of": "691",
    "moldova, republic of": "373",
    "mozambique": "258",
    "palestinian territory, occupied": "970",
    "pitcairn": "872",
    "réunion": "262",
    "russia": "7",
    "saint barthélemy": "590",
    "saint helena, ascension and tristan da cunha": "290",
    "saint kitts and nevis": "1869",
    "saint lucia": "1758",
    "saint martin": "590",
    "saint pierre and miquelon": "508",
    "saint vincent and the grenadines": "1784",
    "sao tome and principe": "239",
    "somalia": "252",
    "svalbard and jan mayen": "47",
    "syrian arab republic": "963",
    "taiwan, province of china": "886",
    "tanzania, united republic of": "255",
    "timor-leste": "670",
    "venezuela, bolivarian republic of": "58",
    "viet nam": "84",
    "virgin islands, british": "1284",
    "virgin islands, u.s.": "1340"
}

# FUNCTIONS
def getHtmlResponse(url, cookies={}, use_proxy=False):
    headers = {
        'User-Agent':ua.random,
    }
    if(use_proxy):
        payload = {'api_key': proxy_api_key, 'url': url, }
        try:
            return requests.get('http://api.scraperapi.com', params=payload, timeout=25, headers=headers)
        except Exception as e:
            print("Error in getHtmlResponse() for url >>>", url, "<<<")
            print(str(e))
            return None
    else:
        try:
            return requests.get(url, timeout=25, headers=headers, cookies=cookies)
        except Exception as e:
            print("Error in getHtmlResponse() for url >>>", url, "<<<")
            print(str(e))
            return None

def getSoup(response):
    try:
        return bs(response.content, 'html.parser')
    except Exception as e:
        print("Error in getSoup() >>> Msg: ", str(e))
        return None

def make_soup(url, cookies={}, use_proxy=False):
    soup = ''
    response = getHtmlResponse(url, cookies={}, use_proxy=use_proxy)
    if(response):
        soup = getSoup(response)
        if(soup):
            return soup
    return soup

def save_logo(url, domain):
    return ''

def getDomainName(url, TLD=True):
    match = re.search('(https?://)?(www\\.)?([A-Za-z_0-9-]+)((\\.[A-Za-z]+)+)', url)
    if match:
        if(TLD):   # return compelete DomainName
            return match.group(3) + match.group(5)
        else:   # return DomainName without TLD(Top Level Domain)
            return match.group(3)
    else:   # invalid url
        return None

def clean_title(title_text, to_be_deleted_list):
    t2 = re.sub("[\"\'«»&—,:0123456789|!()./\\\]", '', title_text)
    t2 = t2.replace("-", " ")
    t3 = ' '.join(c for c in t2.split(" ") if c not in to_be_deleted_list)
    t3 = ' '.join(c for c in t3.split())
    return t3

def fixed_title(main_page_soup, domain):
    to_b_deleted = ['Home', 'Facebook', 'Index', 'index', 'Error', '404', 'Not', 'Found', '403', 'Forbidden', 'HOME',
    'INDEX', 'www']

    tag = main_page_soup.find('title')
    title_text = ''
    new_title = None
    if tag:
        title_text = tag.text
    if len(title_text.strip()) > 3:
        title_text = title_text.replace(domain, '') # removes domain from title if exists
        t3 = clean_title(title_text, to_b_deleted)
        new_title = t3[:80]
    return new_title

def getDomainTitle(domain):
    domain_title = None
    try:
        new_domain = "http://" + domain
        res = getHtmlResponse(new_domain, use_proxy=False)
        if(res):
            soup = getSoup(res)
            if(soup):
                domain_title = fixed_title(soup, domain)
        return domain_title
    except Exception as e:
        print("Error in getDomainTitle() for url >>>", domain, "<<<")
        return domain_title


def getGoogleDetails(p_id, language):
    try:
        url = place_search_by_place_id.format(p_id, "address_component,name,formatted_address,international_phone_number,website", place_api_key, language)
        res = getHtmlResponse(url, use_proxy=False)
        soup = getSoup(res)
        return json.loads(soup.text)["result"]
    except Exception as e:
        print("Error in getGoogleDetails() >>> Msg: ", str(e))
        return None

def get_google_address_component(component):
    street_keys = ["subpremise", "premise", "street_number", "route", "neighborhood", "sublocality_level_4", "sublocality_level_3", "sublocality_level_2", "sublocality_level_1", "administrative_area_level_4", "administrative_area_level_3"] # in order if present
    city_keys = ["locality", "postal_town", "administrative_area_level_2"] # first occuring
    state_key = "administrative_area_level_1"
    country_key = "country"
    postal_code_key = "postal_code"
    result = {
        "country":"",
        "state":"",
        "city":"",
        "street-address":"",
        "postal-code":""
    }

    str_add = ""
    for k in street_keys:
        for dic in component:
            if(k in dic["types"]):
                str_add += dic["long_name"] + ", "
    result["street-address"] = str_add.rstrip(", ")

    for k in city_keys:
        if(not result["city"]):
            for dic in component:
                if(k in dic["types"]):
                    result["city"] = dic["long_name"]
                    break

    for dic in component:
        if(state_key in dic["types"]):
            result["state"] = dic["long_name"]
            break
    
    for dic in component:
        if(country_key in dic["types"]):
            result["country"] = dic["long_name"]
            break

    for dic in component:
        if(postal_code_key in dic["types"]):
            result["postal-code"] = dic["long_name"]
            break
    return result

def getGooglePlaceData(query, domain_tld, language):
    google_data = None
    url = place_search_by_query.format(query, "place_id", place_api_key, language)
    try:
        res = getHtmlResponse(url, use_proxy=False)
        soup = getSoup(res)
        req_data = json.loads(soup.text)
        if(req_data["status"] == "OK"): 
            place_IDs = []
            for case in req_data["candidates"]:
                place_IDs.append(case["place_id"])
            for place_ID in place_IDs:
                data_details = getGoogleDetails(place_ID, language)
                if(data_details):
                    if("website" in data_details.keys()):
                        if(domain_tld in data_details["website"]):
                            data_details["address_components"] = get_google_address_component(data_details["address_components"])
                            google_data = data_details
                            break
    except Exception as e:
        print("Error in getGooglePlaceData() >>> Msg: ", str(e))
    finally:
        return google_data

def getGoogleMatchedData(org_name, domain, language):
    result = None
    if(domain):
        # trying refined org_name
        refined_name = org_name.replace(" ", "+").replace("&", "and")
        result = getGooglePlaceData(refined_name, domain, language)
        if(not result):
            # trying refined domain title
            domain_title = getDomainTitle(domain)
            if(domain_title):
                domain_title = domain_title.replace(" ", "+").replace("&", "and")
                result = getGooglePlaceData(domain_title, domain, language)

    return result


def getGoogleSourceInfo(sources, url):
    gm_kw_regex = re.compile(r'!2s.*!5e0')
    data = []
    for src in sources:
        try:
            if(src.startswith("https://maps.google.com/maps?q=")):
                keywords = src.split("?q=")[1]
                data.append({'keywords':keywords, 'lat':'', 'lng':''})
            else:
                lng, lat = ((src.split('!2d')[1]).split('!2m')[0]).split('!3d')
                keywords = (gm_kw_regex.search(src))
                if(keywords):
                    keywords = keywords.group()[3:-4]
                else:
                    #using domain name as keywords
                    keywords = getDomainName(url)
                data.append({'keywords':keywords, 'lat':lat, 'lng':lng})
            
        except Exception as e:
            print("Error in getGoogleSourceInfo() >>> Msg: ", str(e))
            continue
    return data

def get_google_address_by_geo_info(query, lat, lng, language):
    address = None
    if(lat == ''):
        url = geocoding_search_url.format(query.replace(' ', '+'), geocoding_api_key, language)
    else:
        url = place_search_by_geo_info.format(query, 2000, lat, lng, place_api_key, language)
    #print(url)
    response = getHtmlResponse(url)
    if(response):
        soup = getSoup(response)
        if(soup):
            s_text = soup.text
            address = re.findall('"formatted_address"\\s:\\s"(.+)"', s_text)
    return address

def get_google_pin_address(soup_obj, url, language):
    addresses = []
    if(soup_obj):
        iframes = soup_obj.find_all('iframe')
        if(iframes != None):
            google_srcs = set()
            for iframe in iframes:
                try:
                    src = iframe['src']
                    if(src.startswith("https://maps.google.com/") or src.startswith("https://www.google.com/maps/")):
                        google_srcs.add(src)
                except Exception as e:
                    print("Error in get_google_pin_address() >>> Msg: Source not found",)
                    continue
            if(google_srcs):
                data = getGoogleSourceInfo(google_srcs, url)
                if(data):
                    for dic in data:
                        add = get_google_address_by_geo_info(dic['keywords'], dic['lat'], dic['lng'], language)
                        if(add):
                            addresses.extend(add)

    return addresses


def get_google_formatted_address_using_address(address, language):
    search_url = geocoding_search_url.format(address, geocoding_api_key, language)
    google_data = json.loads(getHtmlResponse(search_url).text)
    if(google_data):
        if(google_data["status"] == "OK"):
            if(len(google_data["results"]) == 1):
                result = google_data["results"][0]
                if(result.get("address_components")):
                    dic_data = {"address": result["formatted_address"], "components": get_google_address_component(result["address_components"])}
                    return dic_data
    return None


def load_country_context(country="global", add_with_global_setting=True):
    country_context = COUNTRY_CONTEXTS.get('countries').get(country)
    if not country_context:
        country_context = {}
    if country != "global" and add_with_global_setting:
        global_context = COUNTRY_CONTEXTS.get('countries').get("global")
        for field in global_context:
            if country_context.get(field):
                country_context[field] += global_context[field]
            else:
                country_context[field] = global_context[field]
    return country_context


def find_emails(text):
    emails = []
    email_regex = '([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9-\.\-_]+\.[a-zA-Z]+)'
    items = re.findall(email_regex, text)
    for item in items:
        emails.append(item)
    return list(set(emails))

def purify_emails(original_email_list, composite_mode=False):
    '''
    This function takes a list of emails as input, extracts all unique emails from 
    input list and finally return a list of unique emails.
    '''
    if(len(original_email_list) > 1):
        original_unique_emails = []
        filtered_unique_emails = []
        filtered_emails = []
        # adding email to 'filtered_emails'
        if(composite_mode):
            for dic in original_email_list:
                filtered_emails.append(dic["email"].lower().strip())
        else:
            for email in original_email_list:
                filtered_emails.append(email.lower().strip())

        for index, email in enumerate(filtered_emails):
            if(not email in filtered_unique_emails):
                filtered_unique_emails.append(email)
                original_unique_emails.append(original_email_list[index])

        return original_unique_emails
    
    else:
        return original_email_list

def get_unique_social_media_links(original_social_links_list, composite_mode=True):
    if(len(original_social_links_list) > 1):
        original_unique_socials = []
        filtered_unique_socials = []
        filtered_socials = []
        # adding url to 'filtered_socials'
        if(composite_mode):
            for dic in original_social_links_list:
                filtered_socials.append(dic["url"].strip("/").split(".com")[1].strip())
        else:
            for url in original_social_links_list:
                filtered_socials.append(url.strip("/").split(".com")[1].strip())

        for index, url in enumerate(filtered_socials):
            if(not url in filtered_unique_socials):
                filtered_unique_socials.append(url)
                original_unique_socials.append(original_social_links_list[index])

        return original_unique_socials
        
    else:
        return original_social_links_list


def get_unique_addresses_for_composite_data(original_address_list, country):
    if(country == "russia"):
        from root.country_tools.russia.tools import get_russian_unique_addresses
        unique_function = get_russian_unique_addresses

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
                    if(unique_add["source"] != "country-module"):
                        if(original_add["source"] == "country-module"):
                            uniques[j] = original_add
                        elif(original_add["source"] == "company-website" and unique_add["source"] != "company-website"):
                            uniques[j] = original_add
                    break
            if(is_unique):
                uniques.append(original_add)
        return uniques

    else:
        return original_address_list 

def get_unique_phones_for_composite_data(original_phone_list, country):
    if(country == "russia"):
        from root.country_tools.russia.tools import purify_russian_phones
        unique_function = purify_russian_phones

    if(len(original_phone_list) >= 2):
        uniques = []
        uniques.append(original_phone_list[0])
        original_phone_list = original_phone_list[1:]

        for i, original_phone in enumerate(original_phone_list):
            is_unique = True
            for j, unique_phone in enumerate(uniques):
                result = unique_function([original_phone, unique_phone], composite_mode=True)
                if(len(result) == 1):
                    is_unique = False
                    if(unique_phone["source"] != "country-module"):
                        if(original_phone["source"] == "country-module"):
                            uniques[j] = original_phone
                        elif(original_phone["source"] == "company-website" and unique_phone["source"] != "company-website"):
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


def json2composite(json_obj, country):
    all_addresses = []
    all_phones = []
    all_emails = []
    all_facebook_links = []
    all_instagram_links = []
    all_linkedin_links = []
    all_twitter_links = []
    all_youtube_links = []

    out_json = { 
        "composite": {
            "website-title": "",
            "addresses": [],
            "emails": [],
            "telephones": [],
            "social_media_links": {},
            "company-description": [],
            "company-name": [],
            "logo": []
        },
        "input_data": json_obj["input_data"],
        "matched_data": []
    }

    # getting website data
    if(json_obj.get("website_data")):
        web_data = json_obj["website_data"]["result"]
        out_json["matched_data"].append({"company-website": web_data})
        if(web_data.get("web_title")):
            
            out_json["composite"]["website-title"] = {"source":"company-website", "data": web_data["web_title"]}
        
        if(web_data.get("phones")):
            for phone in web_data["phones"]:
                all_phones.append({"source": "company-website", "phone": phone})
        
        if(web_data.get("emails")):
            for email in web_data["emails"]:
                all_emails.append({"source": "company-website", "email": email})

        if(web_data.get("addresses")):
            for dic_address in web_data["addresses"]:
                all_addresses.append(dic_address)

        if(web_data.get("social_pages")):
            social_pages = web_data["social_pages"]

            if(social_pages.get("facebook")):
                all_facebook_links.append({"source":"company-website", "url": social_pages["facebook"]})

            if(social_pages.get("instagram")):
                all_instagram_links.append({"source":"company-website", "url": social_pages["instagram"]})

            if(social_pages.get("linkedin")):
                all_linkedin_links.append({"source":"company-website", "url": social_pages["linkedin"]})

            if(social_pages.get("twitter")):
                all_twitter_links.append({"source":"company-website", "url": social_pages["twitter"]})
            
            if(social_pages.get("youtube")):
                all_youtube_links.append({"source":"company-website", "url": social_pages["youtube"]})

        if(web_data.get("logo_url")):
            out_json["composite"]["logo"].append({"source": "company-website", "data": {"url": web_data["logo_url"], "path": None}})

    # getting google data
    if(json_obj.get("google_data")):
        google_data = json_obj["google_data"]
        out_json["matched_data"].append({"google": google_data})

        if(google_data.get("emails")):
            for email in google_data["emails"]:
                all_emails.append({"source": "google", "email": email})

        if(google_data.get("social_pages")):
            social_pages = google_data["social_pages"]

            if(social_pages.get("facebook")):
                all_facebook_links.append({"source":"google", "url": social_pages["facebook"]})

            if(social_pages.get("instagram")):
                for item in social_pages["instagram"]:
                    all_instagram_links.append({"source":"google", "url": item})

            if(social_pages.get("linkedin")):
                for item in social_pages["linkedin"]:
                    all_linkedin_links.append({"source":"google", "url": item})

            if(social_pages.get("twitter")):
                for item in social_pages["twitter"]:
                    all_twitter_links.append({"source":"google", "url": item})
            
            if(social_pages.get("youtube")):
                for item in social_pages["youtube"]:
                    all_youtube_links.append({"source":"google", "url": item})

        if(google_data["google_map_address"].get("address")):
            for address in google_data["google_map_address"]["address"]:
                all_addresses.append({"source":"google", "address": address})

    # getting facebook data
    if(json_obj.get("facebook_data")):
        facebook_data = json_obj["facebook_data"]
        out_json["matched_data"].append({"facebook": facebook_data})

        for dic in facebook_data:
            if(dic.get("address")):
                all_addresses.append({"source":"facebook", "address": dic["address"]})

            if(dic.get("phone")):
                all_phones.append({"source":"facebook", "phone": dic["phone"]})

            if(dic.get("email")):
                for email in dic["email"]:
                    all_emails.append({"source":"facebook", "email": email})
            
            if(dic.get("saved_logo")):
                out_json["composite"]["logo"].append({"source":"facebook", "data": {"url": dic["saved_logo"], "path": None}})

            
            if(dic.get("more_info")):
                out_json["composite"]["company-description"].append({"source":"facebook", "data": dic["more_info"]})

    # getting whois data
    if(json_obj.get("whois")):
        whois_data = json_obj["whois"]
        out_json["matched_data"].append({"whois": whois_data})

        if(whois_data.get("organization")):
            out_json["composite"]["company-name"].append({"source": "whois", "data": whois_data["organization"]})

        if(whois_data.get("email")):
            all_emails.append({"source": "whois", "email": whois_data["email"]})
    
    # getting info-box data
    if(json_obj.get("infobox_info")):
        info_box_data = json_obj["infobox_info"]
        out_json["matched_data"].append({"info-box": info_box_data})
        
        if(info_box_data.get("address")):
            all_addresses.append({"source": "info-box", "address": info_box_data["address"]})

        if(info_box_data.get("phone")):
            all_phones.append({"source": "info-box", "phone": info_box_data["phone"]})

    # getting country_module data
    if(json_obj["country_module"].get("result")):
        country_module_data = json_obj["country_module"]["result"]

        if(country == "russia"):
            out_json["matched_data"].append({"country-module": country_module_data})
            from root.country_tools.russia.tools import get_russian_country_module_composite_data
            composite_data_extention = get_russian_country_module_composite_data(country_module_data)
            if(composite_data_extention):
                for key in composite_data_extention.keys():
                    if(key == "company-description"):
                        out_json["composite"]["company-description"].append(composite_data_extention["company-description"])

                    elif(key == "company-name"):
                        out_json["composite"]["company-name"].append(composite_data_extention["company-name"])

                    elif(key == "addresses"):
                        all_addresses.extend(composite_data_extention["addresses"])

                    elif(key == "telephones"):
                        all_phones.extend(composite_data_extention["telephones"])

                    elif(key == "emails"):
                        all_emails.extend(composite_data_extention["emails"])
        
        elif(country == "china"):
            from root.country_tools.china.tools import select_dictionary_for_composite_data, get_chinese_country_module_composite_data
            
            domain = json_obj["input_data"]["domain"]
            selected_country_module_data = select_dictionary_for_composite_data(country_module_data, domain)

            composite_data_extention = get_chinese_country_module_composite_data(selected_country_module_data)
            if(composite_data_extention):
                for key in composite_data_extention.keys():
                    if(key == "company-description"):
                        out_json["composite"]["company-description"].append(composite_data_extention["company-description"])

                    elif(key == "logo"):
                        out_json["composite"]["logo"].append(composite_data_extention["logo"])

                    elif(key == "company-name"):
                        out_json["composite"]["company-name"].extend(composite_data_extention["company-name"])

                    elif(key == "addresses"):
                        all_addresses.extend(composite_data_extention["addresses"])

                    elif(key == "telephones"):
                        all_phones.extend(composite_data_extention["telephones"])

                    elif(key == "emails"):
                        all_emails.extend(composite_data_extention["emails"])
                        
    # getting unique data from sorted data and finding vk_link
    if(country == "russia"):
        from root.country_tools.russia.tools import get_russian_address_parts

        # translating addresses to russian
        for index, dic in enumerate(all_addresses):
            if(dic["source"] in ["google", "facebook", "info-box"]):
                try:
                    translated = translator.translate(dic["address"], src="en", dest="ru").text
                    all_addresses[index]["address"] = translated
                except:
                    pass

        unique_addresses = get_unique_addresses_for_composite_data(all_addresses, country)

        # getting components of addresses that do not have this part (addresses from 'google', 'facebook', and 'info-box')
        for index, dic in enumerate(unique_addresses):
            if(not dic.get("components")):
                unique_addresses[index] = get_russian_address_parts(dic["address"], dic["source"], language="ru")

        unique_phones = get_unique_phones_for_composite_data(all_phones, country)

        # finding vk_link
        from root.country_tools.russia.tools import find_VK_link
        vk_kink = find_VK_link(json_obj["input_data"]["domain"])
        if(vk_kink):
            out_json["composite"]["social_media_links"]["VK"] = [{"source": "google", "url":vk_kink}]
        else:
            out_json["composite"]["social_media_links"]["VK"] = []

    else:
        unique_addresses = all_addresses
        unique_phones = all_phones
    
    unique_emails = get_unique_emails_for_composite_data(all_emails)

    unique_facebook_links = get_unique_social_media_links(all_facebook_links, composite_mode=True)
    unique_instagram_links = get_unique_social_media_links(all_instagram_links, composite_mode=True)
    unique_linkedin_links = get_unique_social_media_links(all_linkedin_links, composite_mode=True)
    unique_twitter_links = get_unique_social_media_links(all_twitter_links, composite_mode=True)
    unique_youtube_links = get_unique_social_media_links(all_youtube_links, composite_mode=True)

    if(len(unique_addresses) > MAX_COMPOSITE_ADDRESSES):
        selected = [item for item in unique_addresses if item["source"]=="country-module"]
        for item in unique_addresses:
            if(item["source"] == "company-website"):
                selected.append(item)
        if(len(selected) < MAX_COMPOSITE_ADDRESSES):
            for item in unique_addresses:
                if(not item["source"] in ["company-website", "country-module"]):
                    selected.append(item)
        
        out_json["composite"]["addresses"] = selected[:MAX_COMPOSITE_ADDRESSES]
    else:
        out_json["composite"]["addresses"] = unique_addresses[:MAX_COMPOSITE_ADDRESSES]
    
    if(len(unique_emails) > MAX_COMPOSITE_EMAILS):
        selected = [item for item in unique_emails if item["source"]=="country-module"]
        for item in unique_emails:
            if(item["source"] == "company-website"):
                selected.append(item)
        if(len(selected) < MAX_COMPOSITE_EMAILS):
            for item in unique_emails:
                if(not item["source"] in ["company-website", "country-module"]):
                    selected.append(item)
        
        out_json["composite"]["emails"] = selected[:MAX_COMPOSITE_EMAILS]
    else:
        out_json["composite"]["emails"] = unique_emails[:MAX_COMPOSITE_EMAILS]
    
    if(len(unique_phones) > MAX_COMPOSITE_PHONES):
        selected = [item for item in unique_phones if item["source"]=="country-module"]
        for item in unique_phones:
            if(item["source"] == "company-website"):
                selected.append(item)
        if(len(selected) < MAX_COMPOSITE_PHONES):
            for item in unique_phones:
                if(not item["source"] in ["company-website", "country-module"]):
                    selected.append(item)
        
        out_json["composite"]["telephones"] = selected[:MAX_COMPOSITE_PHONES]
    else:
        out_json["composite"]["telephones"] = unique_phones[:MAX_COMPOSITE_PHONES]
    
    out_json["composite"]["social_media_links"]["facebook"] = unique_facebook_links[:MAX_COMPOSITE_FACEBOOK_LINKS]
    out_json["composite"]["social_media_links"]["instagram"] = unique_instagram_links[:MAX_COMPOSITE_INSTAGRAM_LINKS]
    out_json["composite"]["social_media_links"]["linkedin"] = unique_linkedin_links[:MAX_COMPOSITE_LINKEDIN_LINKS]
    out_json["composite"]["social_media_links"]["twitter"] = unique_twitter_links[:MAX_COMPOSITE_TWITTER_LINKS]
    out_json["composite"]["social_media_links"]["youtube"] = unique_youtube_links[:MAX_COMPOSITE_YOUTUBE_LINKS]

    return {"result": out_json}


def find_addresses(text, patterns, country, is_contact_page=False):
    addresses = []
    if(country == "brazil"):
        from root.country_tools.brazil.tools import find_brazilian_addresses
        addresses = find_brazilian_addresses(text, patterns)
    
    elif(country == "russia"):
        from root.country_tools.russia.tools import find_russian_addresses
        addresses = find_russian_addresses(text, patterns)

    elif(country == "vietnam"):
        from root.country_tools.vietnam.tools import find_vietnamese_addresses
        addresses = find_vietnamese_addresses(text, patterns)
    
    elif(country == "mexico"):
        from root.country_tools.mexico.tools import find_mexican_addresses
        addresses = find_mexican_addresses(text, patterns)
    
    elif(country == "india"):
        from root.country_tools.india.tools import find_indian_addresses
        addresses = find_indian_addresses(text, patterns, is_contact_page)
    
    return addresses

def purify_addresses(address_list, country, original_source):
    purified_addresses = []
    if(country == "brazil"):
        from root.country_tools.brazil.tools import purify_brazilian_addresses
        purified_addresses = purify_brazilian_addresses(address_list)
    
    elif(country == "russia"):
        from root.country_tools.russia.tools import purify_russian_addresses
        purified_addresses = purify_russian_addresses(address_list, original_source)

    elif(country == "vietnam"):
        from root.country_tools.vietnam.tools import purify_vietnamese_addresses
        purified_addresses = purify_vietnamese_addresses(address_list)
    
    elif(country == "mexico"):
        from root.country_tools.mexico.tools import purify_mexican_addresses
        purified_addresses = purify_mexican_addresses(address_list)
    
    elif(country == "india"):
        from root.country_tools.india.tools import purify_indian_addresses
        purified_addresses = purify_indian_addresses(address_list)
    
    return purified_addresses


def find_phones(text, patterns, country):
    phones = []
    if(country == "brazil"):
        from root.country_tools.brazil.tools import find_brazilian_phones
        phones = find_brazilian_phones(text, patterns)
    
    elif(country == "russia"):
        from root.country_tools.russia.tools import find_russian_phones
        phones = find_russian_phones(text, patterns)

    elif(country == "vietnam"):
        from root.country_tools.vietnam.tools import find_vietnamese_phones
        phones = find_vietnamese_phones(text, patterns)
    
    elif(country == "mexico"):
        from root.country_tools.mexico.tools import find_mexican_phones
        phones = find_mexican_phones(text, patterns)
    
    elif(country == "india"):
        from root.country_tools.india.tools import find_indian_phones
        phones = find_indian_phones(text, patterns)
    
    return phones

def purify_phones(phone_list, country):
    purified_phones = []
    if(country == "brazil"):
        from root.country_tools.brazil.tools import purify_brazilian_phones
        purified_phones = purify_brazilian_phones(phone_list)
    
    elif(country == "russia"):
        from root.country_tools.russia.tools import purify_russian_phones
        purified_phones = purify_russian_phones(phone_list)

    elif(country == "vietnam"):
        from root.country_tools.vietnam.tools import purify_vietnamese_phones
        purified_phones = purify_vietnamese_phones(phone_list)
    
    elif(country == "mexico"):
        from root.country_tools.mexico.tools import purify_mexican_phones
        purified_phones = purify_mexican_phones(phone_list)
    
    elif(country == "india"):
        from root.country_tools.india.tools import purify_indian_phones
        purified_phones = purify_indian_phones(phone_list)

    return purified_phones
