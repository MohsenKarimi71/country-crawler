import openpyxl
import json
import re
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

addresses = [
    "Graha Chantia L3\nJl Bangka Raya No. 6\nJakarta Selatan 12720",
    "Jl. P. Jayakarta 117 Blok B 52-54 Jakarta 10730 INDONESIA",
    "Jl. Cijerah No. 19 Bandung 40213",
    "Kompleks Rungkut Megah Raya Blok D-18 Jl. Raya Kalirungkut No 5 Surabaya 60293",
    "Menara MTH Lantai 15\nJl. M.T. Haryono Kav. 23\nJakarta – 12820",
    "Jl. Lingkar Luar Barat Kav. 35-36, Cengkareng Jakarta Barat, 11740, Indonesia",
    "Jl. Jati Raya Blok J1 No 11,J 10 No 1E ,J10 No 1D Newton Techno Park Lippo Cikarang",
    "Blok B No. 120-121 Jl. Majapahit No. 18-22, Jakarta 10160",
    "Blok A No. 8\nJln. Pangeran Tubagus Angke\nJelambar - Jakarta Barat\nIndonesia 11460",
    "100 Tras Street\n#16-01 ; 100AM\nSingapore (079027)",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]

phones = [
    "+6221 719 0011",
    "(62-21) 600 9087",
    "(62-22) 6031235",
    "(62-21) 6009087",
    "+62-21-5839-7777",
    "66527513",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
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

data = csv2json(os.path.join("samples", "indonesia", "200 Indonesia Samples.csv"))
with open(os.path.join("samples", "indonesia", "domain_only.json"), mode="w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
'''