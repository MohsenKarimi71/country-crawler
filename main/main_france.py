import openpyxl
import json
import re
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

addresses = [
    "142, rue de la Forêt\n74130 Contamine-sur-Arve\nFrance",
    "45 rue d'Ulm\nF-75230 Paris cedex 05",
    "Les Miroirs\n18, avenue d'Alsace\n92400 Courbevoie\nFRANCE",
    "1 Rue Léonard de Vinci\n91220 Le Plessis-Pâté",
    "86 Rue Paul Bert\n69003 Lyon",
    "22, rue de la Rigourdière\n35510 Cesson-Sevigné",
    "388, Boulevard J.J. BOSC\n33130 Bègles",
    "Parc du Pommarin - Bâtiment C\n137, rue de Mayoussard\n38430 MOIRANS France",
    "3 rue Joliot-Curie\nF-91192 Gif-sur-Yvette Cedex",
    "3 rue des Rouges Terres, 51110 Pomacle",
    "Avenue de la Boulaie\nC.S. 47601\nF-35576 Cesson-Sévigné Cedex",
    "2 rue Edouard Belin  -  Metz Technopôle  -  57070 METZ",
    "31 rue Victor Micholet\n83000 Toulon",
    "82 Av. Jean Jaures\n69007 Lyon",
    "2 Rue Marceau Delorme\n92600 Asnières Sur Seine",
    "Route de Chêne, 5\nCase Postale 6298\n1211 Genève 6",
    "36 Rue de Bellevue 92100 Boulogne-Billancourt",
    "54-56 rue d'Arcueil 94598 Rungis Cedex",
    "36 Rue de l Hôpital Militaire 59800 Lille",
    "62 boulevard Niels Bohr\nCS52132\n69603 VILLEURBANNE Cedex",
    "135 Chemin des bassins\n94000 CRETEIL",
    "135 Chemin des bassins\n94000 CRETEIL\nFrance"
]

phones = [
    "+33 (0) 1 44 32 30 00",
    "+33 (0)3 87 76 47 47",
    "+33 (0)1 75 31 60 00",
    "+33 (0)2 99 84 45 00",
    "+33 (0) 4 27 50 21 50",
    "+33 (0) 4 72 43 99 65",
    "+33 (0)1 43 39 44 41",
    "+33 1 69 88 85 29",
    "33 1 60 14 46 90",
    "+33 970 821 680",
    "04.76.35.20.17",
    "04 27 50 21 50",
    "04 27 50 21 50",
    "04 27 50 21 50",
    "01 55 19 47 27",
    "01 41 73 08 20",
    "03 20 74 81 96",
    "04 72 43 99 65"
]

address_patterns = [
    "(" + 
        "(" +
            "(((?<!\n).{,10}rue)|((?<!\n).{,10}boulevard)|((?<!\n).{,10}Av\.))" +
        ")" +
        "(" +
            "[\w\W]{5,100}" +
        ")" +
        "(" +
            "((france)|((?<!\w)\d{5}(?!\w)[^\n]{,30}))" +
        ")"
    ")",
]

phone_patterns = [
    "(\d{2}[\s\.\-]+\(0\)[\s\.\-]*\d[\s\.\-]+\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2})",
    "(\d{2}[\s\.\-]+\d[\s\.\-]+\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2})",
    "(\d{2}[\s\.\-]+\d{3}[\s\.\-]+\d{3}[\s\.\-]+\d{3})",
    "(\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2}[\s\.\-]+\d{2})"
]

'''
for add in addresses:
    print(add.replace("\n", " "), " >>> ", len(add))
    m = re.search(address_patterns[0], add, flags=re.IGNORECASE)
    if(m):
        print(m.group(0).replace("\n", " "))
    print(50 * "*")
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
