import json
import re
import os
from root.general_tools.tools import load_country_context
from csv_excel_tools import get_csv_outputs



addresses = [
    "Hinterstraße 15 65620 Waldbrunn",
    "Hinterstraße 15\n65620 Waldbrunn\nDeutschland",
    "Endress+Hauser Messtechnik GmbH+Co. KG\nGermany",
    "Adi-Dassler-Strasse 1\n91074 Herzogenaurach\nGermany",
    "GSI Helmholtzzentrum für Schwerionenforschung GmbH\nPlanckstraße 1\n64291 Darmstadt",
    "DFN-Verein e. V.\nAlexanderplatz 1\nD - 10178 Berlin",
    "Niederlassung Stuttgart\nDFN-Verein e. V.\nLindenspürstr. 32\nD - 70176 Stuttgart",
    "Miele & Cie. KG\nVertriebsgesellschaft Deutschland\nCarl-Miele-Straße 29\nPostfach\n33325 Gütersloh",
    "Nortkirchenstraße 100\n44263 Dortmund\nDeutschland",
    "93179 Brennberg Pfaffenthanner Weg 5",
    "Löwentaler Straße 20\nZF Forum\n88046 Friedrichshafen\nGermany",
    "Felix-Wankel-Strasse 2\n73760 Ostfildern\nGermany",
    "Felix-Wankel-Straße 2\n73760 Ostfildern\nDeutschland",
    "Trompeterallee 110\nD-41189 Moenchengladbach\nGermany",
    "Mercedesstraße 120\n70372 Stuttgart\nGermany",
    "Neuenhofstraße 181\n52078 Aachen, Germany",
    "Löwentaler Straße 20\nZF Forum\n88046 Friedrichshafen\nGermany",
    "Delivery address\nGraf-von-Soden-Platz 1\nResearch & Development\n88046 Friedrichshafen\nGermany",
    "Nobelstraße 12\n70569 Stuttgart\nDeutschland",
    "adresse\nNobelstr. 12\n70569 Stuttgart",
    "Carl-Zeiss-Straße 22\n73446 Oberkochen",
    "Konrad GmbH\nFritz-Reichle-Ring 12\nD-78315 Radolfzell",
    "Fritz-Reichle-Ring 12\nD-78315 Radolfzell",
    "Mülheimer Strasse 753840 Troisdorf",
    "Knorr-Bremse AG\nMoosacher Str. 80\nD-80809 München",
    "SET GmbH\nAugust-Braun-Str. 1\n88239 Wangen im Allgäu",
    "August-Braun-Str. 1\n88239 Wangen im Allgäu",
    "ProNES Automation GmbH\nMarie-Curie-Straße 5a\n76829 Landau",
    "Marie-Curie-Straße 5a\n76829 Landau",
    "Großer Kolonnenweg 18 E\n30163 Hanover\nGermany",
    "thyssenkrupp Allee 1\n45143 Essen",
    "Besucheradresse:\nthyssenkrupp Allee 1\n45143 Essen",
    "Schreiberhauer Str. 5\n90475 Nuremberg",
    "Mayor-Wegele-Strasse 6\n86167 Augsburg",
    "At Karlskuppe 26\n99817 Eisenach",
    "Friedrich-Bosse-Str. 6c\n04159 Leipzig",
    "Schreiberhauer Strasse 5\n90475 Nuremberg",
    "Erich-Schlesinger-Str. 37\n18059 Rostock",
    "Mr. Richard Schoenmaker\nSchuurblok 15 B, 2910 Essen",
    "Tec Center\n31162 Bad Salzdetfurth\nGermany",
]


'''
address_patterns = load_country_context("germany", add_with_global_setting=False)["address_patterns"]
counter = 0
for add in addresses:
    m = re.search(address_patterns[0], add, flags=re.IGNORECASE)
    if(not m):
        print(add.replace("\n", " "), " >>> ", len(add))
        print(50 * "*")
    elif(add != m.group(0)):
        print(add.replace("\n", " "), " >>> ", len(add))
        print(m.group(0).replace("\n", " "))
        print(50 * "*")
    else:
        counter += 1

print(len(addresses), " >>> ", counter)
'''

'''
from root.website_tools.company_website import website_info
samples = json.loads(open(os.path.join("samples", "germany", "samples.json"), "r", encoding="utf-8").read())

for dic in samples[150:160]:
    if(dic["Website"] != "-"):
        data = website_info(dic["Website"], dic["Organization Name"], "germany")
        if(data["result"].get("addresses")):
            print(json.dumps(data["result"]["addresses"], indent=4, ensure_ascii=False))
        else:
            print("No address Found")
        print(50 * "*", "\n")

'''

#get_csv_outputs("200 Germany Samples.csv", "germany")