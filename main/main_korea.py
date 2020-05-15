import openpyxl
import json
import re
import os
from root.general_tools.tools import load_country_context

dir_path = os.path.dirname(os.path.abspath(__file__))

phones = []
phone_patterns = None
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

addresses = [
    "전라북도 전주시 덕진구 구렛들1길 20번지| ㆍ대표번호",
    "경기도 용인시 수지구 광교중앙로 338 C동 9층\n(광교우미뉴브)",
    "16914 경기도 용인시 기흥구 구성로 357(청덕동) 용인테크노밸리 B동 513호",
    "주소 : 서울 금천구 가산디지털2로 98 (it 캐슬 1동 609-2호)",
    "주소 : 대전 유성구 엑스포로339번길 10-6",
    "주소 : 서울시 광진구 동일로 118 (화양동, 제이엠빌딩2,3층), 우편번호 : 143-917",
    "51568 경남 창원시 성산구 공단로 166번길 27-7(신촌동)",
    "731418 충남 아산시 음봉면 산동로 145-7",
    "18469 경기도 화성시 동탄기흥로602, 더퍼스트타워3차 501호",
    "대구광역시 달성군 다사읍 세천로 8길 40 (세천리) 성서5차산업단지 내",
    "서울특별시 송파구 법원로 128, SK V1 GL메트로시티 A동 1109~1110호 (주)에이포웰",
    "솔웍스(주) 경기도 용인시 기흥구 동백중앙로 16번길 16-4 에이스동백타워 1411~1413호 대표이사",
    "주소 : 경기도 시흥시 공단2대로 139번길 6 (정왕동)",
    "ADDRESS: 45, DONGTANSANDAN 10-GIL, HWASEONG-SI, GYEONGGI-DO, REPUBLIC OF KOREA",
    "경기도 안양시 동안구 시민대로 361 (관양동 883)",
    "(주)가온코리아 I 광주광역시 광산구 월봉반월길 236",
    "경기도 성남시 중원구 갈마치로 288번길 14, A동 13층 03호(상대원동, 성남SK V1타워)",
    "경기도 성남시 중원구 사기막골로 52(상대원동) 선텍시티Ⅱ 801-805호",
    "935-8, Seobong-ro, Jeongnam-myeon, Hwaseong-si, Gyeonggi-do, Republic of Korea 18522",
    "16-39, LS-ro91 beon-gil\nDongan-gu, Anyang-si, Gyeonggi-do\nKorea",
    "13, Eonju-ro 174-gil, Gangnam-gu, Seoul, Republic of Korea 06017",
    "경기도 광주시 도척면 국사봉로 159",
    "202, Musil-ro, Wonju-si, Gangwon-do",
    "강원도 원주시 단계동 802-5 강원도 원주시 무실로 170 2층",
    "강원도 원주시 무실로 170번지 202호",
    "서울특별시 강남구 영동대로 702",
    "153 Jeongdong-ro, Seongsan-gu, Changwon, Gyeongnam",
    "23, Cheomdan-ro 181beon-gil, Danwon-gu, Ansan, Gyeonggi, Korea",
    "189, Sinwon-ro, Danwon-gu, Ansan, Gyeonggi, Korea",
    "17TH FLOOR IT MIRAE TOWER 60-21, GASAN-DONG GEUMCHEONG-GU SEOUL, KOREA",
    "12F Gangdong Tower, 39, Sangil-ro 6-gil, Gangdong-gu, Seoul 05288, Korea",
    "서울시 강남구 역삼동 727-5 대일테크 빌딩/서울시 강남구 역삼로 25길 23",
    "주소 : 서울특별시 강남구 테헤란로 311, 5층",
    "04524 서울특별시 중구 세종대로 110",
    "주소 : 서울특별시 구로구 디지털로 34길 55 1층 (구로동, 코오롱싸이언스밸리 2차)",
    "서울시 송파구 위례성대로 10, 7층",
    "서울시 성북구 안암로 145 고려대학교 산학관 525호",
    "서울 중구 청계천로 시그니처타워 1022호",
]


'''
address_patterns = load_country_context("korea", add_with_global_setting=False)["address_patterns"]

for add in addresses:
    m = re.search(address_patterns[0], add, flags=re.IGNORECASE)
    if(not m):
        print(add.replace("\n", " "), " >>> ", len(add))
        print(50 * "*")
    elif(add != m.group(0)):
        print(add.replace("\n", " "), " >>> ", len(add))
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

data = csv2json(os.path.join("samples", "korea", "200 korean Samples.csv"))
with open(os.path.join("samples", "korea", "domain_only.json"), mode="w", encoding="utf-8") as outfile:
    outfile.write(json.dumps(data, indent=4, ensure_ascii=False))
'''


from root.website_tools.company_website import website_info
samples = json.loads(open(os.path.join("samples", "korea", "samples.json"), "r", encoding="utf-8").read())

for dic in samples[150:160]:
    if(dic["Website"] != "-"):
        data = website_info(dic["Website"], dic["Organization Name"], "korea")
        if(data["result"].get("addresses")):
            print(json.dumps(data["result"]["addresses"], indent=4, ensure_ascii=False))
        else:
            print("No address Found")
        print(50 * "*", "\n")

