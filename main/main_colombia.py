import openpyxl
import json
import re
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

addresses = [
    "Carrera 46 #52-36 Ed. Vicente Uribe Rendón. Medellín, Colombia",
    "Carrera 7 No. 75-51 Oficina 302\nBogotá DC, Colombia",
    "Km. 14 vía Pereira - Cerritos\nPereira, Risaralda, Colombia",
    "Calle 105 #49e 29  – Villa Santos\nBarranquilla – Colombia",
    "Carrera 43A 15 sur-15\nEdificio Xerox - Of 501.\nMedellín - Antioquia",
    "Dirección: Calle 72 No. 12-77 Bogotá, Colombia",
    "Calle 20 sur #27 – 55\nLocal 9630 Sótano 4. San Lucas Plaza",
    "Calle 147 A No. 54-32\nBogotá Colombia",
    "Dirección: Carrera 33 N° 38-45 Plaza Libertadores - Centro, Ed Gobernación\nVillavicencio, Colombia",
    "Dirección: Carrera 51 C # 12 B Sur -168\nMedellín – Colombia",
    "Dirección: Carrera 6 Calle 17 Esquina CAM - Montenegro Quindío",
    "Tierra Firme Complex(17 Floor) Carrera 9 N° 115-06/30Bogota, Colombia",
    "Dirc: Cra 16A No 80-06 Of 201. Bogotá, Colombia",
    "Calle 49 No. 27A – 34 Bucaramanga - Colombia",
    "Bogotá - Colombia Calle 36 # 16 - 57",
    "Cra 16A No 80-06 Of 201. Bogotá, Colombia",
    "Bogotá\nCr 20 # 37 – 33",
    "Bogotá\nAutop. Norte Av. 45 # 103-40",
    "Carrera 7 # 18 – 21 Of. 411"
]

phones = [
    "(+574) 511 54 00",
    "(574) 313 3096",
    "(+507) 387-3964",
    "(571) 5159581",
    "(571) 3200066",
    "(+57 4) 607 1444",
    "57+1 8052194",
    "(57-4) 444 78 00",
    "(+57) 4 520 4060",
    "57 (6) 7535262",
    "+57 (1) 530 7 555",
    "+57 (7) 6435677",
    "(+57) 8 681 85 00",
    "+57 1  530 7 555",
    "+57 (6) 314 8181"
]

address_patterns = [
    "(" + 
        "(" +
            "((Dirección)|(Carrera)|(Calle)|(Dirc\W)|(Cra\W))" +
        ")" +
        "(" +
            "[\w\W]{3,70}" +
        ")" +
        "(" +
            "((Colombia)|(#\s?\d[^\n]{,25}))" +
        ")"
    ")",
]

phone_patterns = [
    "(\(?\+?\d{2}[\s\.\-\+]?\d\)?[\s\.\-]+\d{7})",
    "(\(?\+?\d{2}[\s\.\-\+]?\d\)?[\s\.\-]+\d{3}[\s\.\-]+\d{4})",
    "(\(?\+?\d{2}[\s\.\-\+]?\d\)?[\s\.\-]+\d{3}[\s\.\-]+\d{2}[\s\.\-]+\d{2})",
    "(\(?\+?\d{2}[\s\.\-\+]?\d\)?[\s\.\-]+\d{3}[\s\.\-]+\d[\s\.\-]+\d{3})",
    "(\(?\+?\d{2}\)?[\s\.\-]+\(?\d\)?[\s\.\-]+\d{7})",
    "(\(?\+?\d{2}\)?[\s\.\-]+\(?\d\)?[\s\.\-]+\d{3}[\s\.\-]+\d{4})",
    "(\(?\+?\d{2}\)?[\s\.\-]+\(?\d\)?[\s\.\-]+\d{3}[\s\.\-]+\d{2}[\s\.\-]+\d{2})",
    "(\(?\+?\d{2}\)?[\s\.\-]+\(?\d\)?[\s\.\-]+\d{3}[\s\.\-]+\d[\s\.\-]+\d{3})"
]

'''
for add in addresses:
    print(add.replace("\n", " "), " >>> ", len(add))
    m = re.search(address_patterns[0], add, flags=re.IGNORECASE)
    if(m):
        print(m.group(0).replace("\n", " "))
    print(50 * "*")
'''

'''
for p in phones:
    print(p)
    m = re.search(phone_patterns[0], p)
    if(m):
        print("1 > ", m.group(0))
    else:
        m = re.search(phone_patterns[1], p)
        if(m):
            print("2 > ", m.group(0))
        else:
            m = re.search(phone_patterns[2], p)
            if(m):
                print("3 > ", m.group(0))
            else:
                m = re.search(phone_patterns[3], p)
                if(m):
                    print("4 > ", m.group(0))
                else:
                    m = re.search(phone_patterns[4], p)
                    if(m):
                        print("5 > ", m.group(0))
                    else:
                        m = re.search(phone_patterns[5], p)
                        if(m):
                            print("6 > ", m.group(0))
                        else:
                            m = re.search(phone_patterns[6], p)
                            if(m):
                                print("7 > ", m.group(0))
                            else:
                                m = re.search(phone_patterns[7], p)
                                if(m):
                                    print("8 > ", m.group(0))
    print(50 * "*")
'''
'''
from root.country_tools.colombia.tools import recheck_Colombian_address
for add in addresses:
    print(re.sub("\n", " ", add))
    print(re.sub("\n", " ", recheck_Colombian_address(add)))
    print(50 * "*")

'''

'''
def csv2json(csv_file_path):
    json_data = []
    infile = open(csv_file_path, mode='r', encoding='utf-8')
    lines = [line for line in infile]
    #titles = lines[0].split(',')
    #titles = [title.rstrip('\n') for title in titles]
    titles = ["Organization Name", "Website"]
    for line in lines[:]:
        dic = {}
        line = line.rstrip('\n')
        info = line.split(',')
        if(len(info) >= len(titles)):
            #info = []
            m = re.search('(.*),([^,]*)', line)
            #info.append(m.group(1))
            #info.append(m.group(2))
            if(m.group(2) != "-"):
                json_data.append("http://" + m.group(2))
        #for i, data in enumerate(info):
        #    dic[titles[i]] = data
        #json_data.append(dic)
    return json_data

data = csv2json(os.path.join("samples", "colombia", "200 Colombia Samples.csv"))
with open(os.path.join("samples", "colombia", "domain_only.json"), mode="w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
'''

from root.website_tools.company_website import website_info

domain = "www.ingesertec.com"
org_name = ""
language = "es"
country = "colombia"
data = website_info(domain, org_name, language, country=country)

with open(os.path.join("temp.json"), encoding="utf-8", mode="a") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))