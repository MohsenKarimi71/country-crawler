import openpyxl
import json
import re
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

addresses = [
    "53 หมู่ 2 ถ.จรัญสนิทวงศ์ ต.บางกรวย อ.บางกรวย จ.นนทบุรี 11130",
    "142 หมู่ที่ 5 ถนน ติวานนท์ Bang Kadi, อำเภอ เมืองปทุมธานี Pathum Thani 12000",
    "เลขที่ 300 ถนนร่มเกล้า แขวงคลองสามประเวศ,เขตลาดกระบัง, กรุงเทพมหานคร 10520",
    "1051/3 Soi Pridi Banomyong 45 (Yaowaraj),Sukhumvit 71, Klongton Nua, WattanaBangkok 10110",
    "55 Soi Ramkhamheang 18 (Maen Khian 3) Huamark, Bangkapi, Bangkok 10240",
    "28/1 อาคารประภาวิทย์ ชั้น 2-3 ถนนสุรศักดิ์ แขวงสีลม เขตบางรัก กรุงเทพฯ 10500",
    "9 หมู่ 7 ตำบลแม่รำพึง อำเภอบางสะพาน ประจวบคีรีขันธ์ 77140",
    "Level 7th, 567 Building,Rama IX Soi 51 ,Suan Luang ,Suan Luang ,Bangkok ,Thailand 10250",
    "11th Fl., Nantawan Building, 161 Ratchadamri Road, Lumpinee, Pathumwan, Bangkok 10330. Thailand",
    "ชั้น 11 อาคารนันทวัน 161 ถนนราชดำริ\nแขวงลุมพินี เขตปทุมวัน กรุงเทพมหานคร 10330",
    "เลขที่ 9 ซอยเฉลิมพระเกียรติ ร.9 ซอย 48 แยก 12پدแขวงดอกไม้ เขตประเวศ กรุงเทพฯ 10250",
    "155 Moo 5, Tambol Chae Chang\nA. San Kamphaeng, Chiang Mai,\nThailand 50130",
    "117 Phra Phutthabat Rd, Nai Mueang, Mueang Phetchabun District, Phetchabun 67000",
    "333 Soi Prachasanti ( Ratchadaphisek 10 ), Ratchadaphisek Road, Huai Khwang ,Bangkok 10310",
    "เลขที่ 65 หมู่ 4 ต.บ้านกลาง อ.เมืองลำพูน จ.ลำพูน 51000",
    "121/91 RS Tower, 32nd Floor\nRatchadaphisek Road, Din Daeng\nBangkok 10400",
    "INC1 Building Room 301D, Thailand Science Park 131 Paholyothin Rd,\nKlong Neung Klong Luang Pathumthani 12120 Thailand",
    "699/37 wongsawang 29\nwongsawang rd\nbangsue 10800\nThailand",
    "ที่ตั้ง :	 113/37 Moo 15  Klongnueng Klongluang\nจังหวัด :	 Pathumthani\nรหัสไปรษณีย์ :	 12120\nประเทศ :	 Thailand",
    "606 Luang Road, Pomprab, Bangkok 10100, Thailand",
    "53 หมู่ 2 ถ.จรัญสนิทวงศ์ ต.บางกรวย อ.บางกรวย จ.นนทบุรี 11130",
    "99/99-2 หมู่ 7 อาคาร เดอะทรี อเวนิว ห้อง 216\nตำบลบางคูวัด อำเภอเมืองปทุมธานี\nจังหวัดปทุมธานี 12000",
    "44 ซ.บรมราชชนนี 70 ถ.บรมราชชนนี ศาลาธรรมสพน์ ทวีวัฒนา กทม. 10170",
    "89/30 หมู่ 4 ซอยจันทร์ทองเอี่ยม ถนนกาญจนาภิเษก \nตำบลบางรักพัฒนา อำเภอบางบัวทอง จังหวัดนนทบุรี 11110",
    "127 อาคารเกษรทาวเวอร์ ชั้นที่ 28, 29 ถนนราชดำริ แขวงลุมพินี เขตปทุมวัน กรุงเทพมหานคร 10330",
    "ชั้น 17 ซ.สุขุมวิท 13 แขวงคลองเตยเหนือ เขตวัฒนา กทม. 10110",
    "79/121 หมู่ 4 ซ.เอกวานิช 2 ถ.เอกวานิช ต.วิชิต อ.เมืองภูเก็ต จ.ภูเก็ต 83000",
    "เลขที่ 44 อาคารศรีจุลทรัพย์ ชั้น 20 ถนนพระรามที่ 1\nแขวงรองเมือง เขตปทุมวัน กรุงเทพฯ 10330"
]

phones = [
    "(662) 238-3063-82",
    "(66)2 300-1320",
    "(66)81 755-0032",
    "02 252-5200",
    "080 807 8078",
    "080 808 8780",
    "+66 53 371 000",
    "+66 53 371 099",
    "056-712341-44",
    "66-2645-4588",
    "(+66) 53 581 036",
    "(+66) 53 554 608",
    "(+66) 53 554 608",
    "662 642 2450",
    "+6665-941-9652",
    "+66 2613 8500"
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
            "((ที่ตั้ง\W)|(เลขที่\W+\d+)|(ชั้น\W+\d+)|([\d\/\-]+\W+หมู่)|(\d+\/\d+)|(\d+\W+Soi)|(\d+th)|(\d+[\w\s]{2,15},)|(\d+\sซ\.))" +
        ")" +
        "(" +
            "[\w\W]{5,120}" +
        ")" +
        "(" +
            "((\D\d{5}(?!\W))|(Thailand))" +
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

data = csv2json(os.path.join("samples", "thailand", "200 Thailand Samples.csv"))
with open(os.path.join("samples", "thailand", "domain_only.json"), mode="w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
'''

from root.website_tools.company_website import website_info

domain = "www.we-inter.com"
org_name = ""
language = "th"
country = "thailand"
data = website_info(domain, org_name, language, country=country)

with open(os.path.join("temp.json"), encoding="utf-8", mode="a") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))