import openpyxl
import json
import re
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

addresses = [
    "Calle Marquesado de Sta. Marta, 3, 28027",
    "Avenida Pearson 21 08034 Barcelona España",
    "Pº de Manuel Lardizabal 13. 20018 Donostia-San Sebastián España",
    "Camino del Cerro Águila 3 28023 Madrid España",
    "Avda. Complutense, 40 - 28040 Madrid",
    "Pº. J. M.ª Arizmendiarrieta, 2\n20500 Arrasate-Mondragón\nGipuzkoa",
    "C/ Goiru, 9\n20500 Arrasate-Mondragón\nGipuzkoa",
    "Orona IDeO-Innovation City,\nPol. Industrial Galarreta, Parcela 10.5, Edificio A3,\n20120 Hernani,\nGipuzkoa",
    "Avinguda d'Alacant, 125\n46702 - Gandia\nValencia (España)",
    "Fundación Tekniker,\nC/ Iñaki Goenaga, 5\n20600 Eibar\nGipuzkoa - Spain",
    "Parke Teknologikoa\nC/ Iñaki Goenaga, 5\n20600 Eibar (Gipuzkoa)",
    "Avda. Camino de Santiago, 40 28050, Madrid",
    "Balmes, 36. 08007, Barcelona",
    "Avda. Camino de Santiago, 40 Edificio 2 –Planta 2, 28050 Madrid",
    "Parque Tecnológico de San Sebastián\nPso. Mikeletegi, 58 - 2º\n20009 San Sebastián • Spain",
    "General Díaz Porlier 49\n28001 Madrid\nEspaña",
    "Centro Nacional de Energías Renovables (CENER) · Ciudad de la Innovación, nº 7 · 31621 Sarriguren (Navarra) · España",
    "Ctra. de Valdepeñas, Km 1,5\nP.I. San Jorge, C/ Pitágoras, 1\n13270 - Almagro\nCiudad Real - España",
    "Avenida del Euro, nº 7 Edificio B\n2ª Planta, Oficina 206\n47009, Valladolid",
    "Dirección:\nPlaza Navarro Rodrigo 11, Alicante",
    "C/ Juan Fermín Gilisagasti 4, 2ªplanta\n20018  San Sebastián (Gipuzkoa) España",
    "Avda. de la Industria, 51\n28108 Alcobendas (Madrid) España",
    "652 Vivero de Empresas Oficina 3.0\n33203, Gijón (Asturias)\nEspaña",
    "Antoni Forrellad, 2 - 08192\nSant Quirze del Vallés\nBarcelona - Spain",
    "C/ Trinchera nº 4 – nave 1 - Gijón 33211",
    "C/ Trinchera nº 4 – nave 1,\nPol. Ind. Los Campones\n33211, Gijón\nAsturias",
    "Infranea Nederland\nGraaf Engelbertlaan 75\n4837 DS Breda",
    "C/Bailén 95-97 Pral. 1a. 08009 Barcelona",
    "Pº Barón de Eroles, 27, 1ºA\n22400 Monzón (Huesca)"
]

phones = [
    "+34 91 211 30 00",
    "+34 93 253 42 00",
    "+34 943 21 98 77",
    "+34 948 42 56 00",
    "91 346 60 00",
    "+34 943 712 400",
    "+34 943 710 212",
    "+34 943 712 400",
    "+34 962 96 58 00",
    "(+34) 962 96 58 00",
    "+ 34-943.20.67.44",
    "+ 34-943.25.69.00",
    "+34 934 964 900",
    "+34 913 595 400",
    "+34 943 309 251",
    "(+34) 91 121 17 00",
    "+ 34 948 25 28 00",
    "(+34) 918 707 193",
    "+34 91 309 86 00",
    "+34 983 319 603",
    "615 38 38 61",
    "+34 91 789 27 50",
    "+34 943 80 55 75",
    "+34 93 710 60 08",
    "+31 (0)76 531 53 57",
    "(+34) 93 457 31 32"
]
phone_patterns = []
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
    print(50 * "*")
'''

address_patterns = [
    "(" + 
        "(" +
            "((address)|(Dirección)|(Calle)|(Avenida)|(C\/)|(Pº)|(Avda\.)|(Avinguda))" +
        ")" +
        "(" +
            "[\w\W]{5,70}" +
        ")" +
        "(" +
            "(" + 
                "(Spain)|(España)|(Barcelona)|(Asturias)|(Madrid)|(Gipuzkoa)|(Valencia)|" + 
                "(Sebastián)|(Alicante)|(Valladolid)|(\D\d{5}(?!\d))" +
            ")" +
        ")"
    ")"
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
            info = []
            m = re.search('(.*),([^,]*)', line)
            info.append(m.group(1))
            info.append(m.group(2))
            #if(m.group(2) != "-"):
            #    json_data.append("http://" + m.group(2))
        for i, data in enumerate(info):
            dic[titles[i]] = data
        json_data.append(dic)
    return json_data

data = csv2json(os.path.join("samples", "spain", "200 Spain Samples.csv"))
with open(os.path.join("samples", "spain", "samples.json"), mode="w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
'''

from root.website_tools.company_website import website_info

domain = "www.ikerlan.es"
org_name = ""
language = "es"
country = "spain"
data = website_info(domain, org_name, language, country=country)

with open(os.path.join("temp.json"), encoding="utf-8", mode="a") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))