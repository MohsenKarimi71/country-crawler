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
    "Jalan Gatot Subroto, Kav. 40-42, Jakarta 12190",
    "Jl. Malioboro No.16, Suryatmajan, Kec. Danurejan, Kota Yogyakarta, Daerah Istimewa Yogyakarta 55213",
    "Komplek Kepatihan, Danurejan Yogyakarta",
    "Jl. Pantai Indah Kapuk, Boulevard Kamal Muara Penjaringan Jakarta Utara 14470",
    "Jl. Pantai Indah Barat\nJakarta Utara 1445",
    "Jl. Raya Boulevard Barat\nKelapa Gading, Jakarta Utara",
    "Jl. Kamal Raya Outer Ring Road\nCengkareng, Jakarta Barat",
    "Jl. Letda Natsir No. 8\nCikeas Nagrak Cibubur",
    "Jl. Patal Senayan 1/5\nJakarta Selatan 12210",
    "Jl. Kemang Raya No. 3 – 5\nJakarta Selatan",
    "Jl. Fachrudin Raya No. 5\nJakarta Pusat",
    "Jl. Daan Mogot Raya\nJakarta Barat",
    "Jl. Pasir Putih II\n(Depan Gedung Jan Hidros MABES AL)\nAncol Timur Jakarta Utara 14430",
    "Jl. Senopati Raya No.8B\nJakarta Selatan",
    "Ruko Golden Boulevard\nBlok V No. 10-11 BSD City",
    "Jl. Kresek Raya, Duri Kosambi\nJakarta Barat",
    "Office :\nJl. Pantai Indah Barat No.1\nPantai Indah Kapuk Jakarta Utara",
    "Office :\nJl. Pantai Indah Barat No.1\nPantai Indah Kapuk Jakarta Utara",
    "Jl. Lebak Bulus P&K No. 12\nJakarta Selatan",
    "Office :\nMall of Indonesia\nLt. GF, No.A.02\nKelapa Gading – Jakarta Utara",
    "Jl. Puri Kembangan\nJakarta Barat",
    "Jl. Patal Senayan 1/5\nJakarta Selatan 12210",
    "Jl. Medan Merdeka Selatan No. 18\nJakarta Pusat 10110",
    "Jl. Kokas No.2 Duren Tiga, Pancoran - Kota Jakarta Selatan",
    "Jl. Kokas No.2, RT.11/RW.1, Duren Tiga, Kec. Pancoran, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12760",
    "Jl. Harsono RM. No. 3, Ragunan\nJakarta 12550, Indonesia",
    "Jl. Jenderal Gatot Subroto Kav. 31\nJakarta Pusat 10210",
    "Jl. Boulevard Epicentrum Selatan – Kawasan Rasuna Epicentrum Kuningan\nJakarta Selatan, DKI Jakarta 12960 – Indonesia",
    "Jl. Letjen M.T Haryono Kav 8, Cawang. Jakarta Timur 13340",
    "HK Tower, Jl. Letjen M.T. Haryono No.Kav 8, RT.12/RW.11, Cawang, Kecamatan Jatinegara, Kota Jakarta Timur, Daerah Khusus Ibukota Jakarta 13340, Indonesia",
    "Address: Jl. Medan Merdeka Timur 1A, Jakarta 10110",
    "Office:\nJln. Wibawa Mukti No. 89",
    "Workshop:\nJl. Wibawa Mukti No. 34",
    "Jl. Medan Merdeka Tim. No.1A, RT.2/RW.1, Gambir, Kecamatan Gambir, Kota Jakarta Pusat, Daerah Khusus Ibukota Jakarta 10110",
    "Address: PT Pertamina (persero)\nJl. Medan Merdeka Timur 1A\nJakarta 10110 Indonesia",
    "Jl. Pattimura No. 20 Kebayoran Baru\nJakarta Selatan 12110",
    "Jl. Pattimura 20, Kebayoran Baru Jakarta Selatan 12110",
    "Jalan Raya Veteran III Banjasari, RT.001/RW.004, Ciawi, Bogor, West Java 16760",
    "Jl Subak Sari, No. 8 Banjar Tegal Gundul\nDesa Tibubeneng Kuta Badung 80361",
    "Jl. Rungkut Menanggal Harapan blok X No.19\nSurabaya | 60293\nIndonesia",
    "Jl. Rungkut Menanggal Harapan No.X /19, Rungkut Menanggal, Kec. Gn. Anyar, Kota SBY, Jawa Timur 60293",
    "Jl. BSD Grand Boulevard Maxwell Raya No.1, Pagedangan, Kec. Pagedangan, Tangerang, Banten 15339, Indonesia",
    "Jl. Dewi Sartika No. 4A, RT 002 /RW 007, Kel. Cililitan, Kec. Keramat Jati, Jakarta Timur",
    "Jl. Siaga 2 , No. 25, Pejaten Barat, Pasar Minggu , Jakarta Selatan - Indonesia",
    "Jl. Medan Merdeka Selatan No. 13 Jakarta 10110 Indonesia",
    "Jl. Raya Bawu-Batealit Rt.42/08,\nBawu, Batealit, Jepara,\nCentral Java Indonesia",
    "Office : Ruko Bukit Cimanggu City C3 No. 8, Bogor 16113",
    "Jl. Panglima Sudirman Kav. 66-68, Gedung Mandiri Tower II, Lt 12, Surabaya, Jawa Timur, Indonesia",
    "Jalan C Simanjuntak No. 70, Terban, Gondokusuman, Terban, Gondokusuman, Kota Yogyakarta, Daerah Isti",
    "Jl. Raya Cikarang Cibarusah RT. 18/06 Kp. Pasir Konci, Ds. Pasir Sari Cikarang Selatan – Bekasi 17550",
    "Jl. Gunung Kelud 6 No. 30 Taman Simprug Lippo Cikarang",
    "Alamat : Jl Sidoyoso 3/3, depan grating selatan 1 Kota",
    "OFFICE\nLt.16 Tower RDTX ,Kav. E4,\nJalan Professor Doktor Satrio No.6 RT.005/RW.002,\nKuningan Timur, Jakarta Selatan,\nDaerah Khusus Ibukota Jakarta",
    "Alamat\nWisma Mulia lt. 41\nJalan Jenderal Gatot Subroto kav.42\nDKI Jakarta, Indonesia",
    "Jl. M.T. Haryono 47 Yogyakarta 55141",
    "Jl. Medan Merdeka Selatan No. 18\nJakarta Pusat 10110",
    "Jl. Raya Pasar Minggu No. 2, Duren Tiga\nPancoran - Jakarta Selatan. 12760",
    "Jl. Rawajati Timur No.K 14, RT.7/RW.6, Rawajati, Kec. Pancoran, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12750",
    "Jl. Rawajati Timur K 14, Kel. Rawajati, Kec. Pancoran - Jakarta Selatan 12750",
    "Jl. Raya Pasar Minggu No. 2, Kel. Duren Tiga, Kec. Pancoran - Jakarta Selatan 12760",
    "Jl. Kemuning Raya No. 16, Kel. Pejaten Timur, Kec. Pasar Minggu - Jakarta Selatan 12510",
    "Graha Aktiva 5th floor\nJl. HR. Rasuna Said Blok X1 Kav. 3\nKuningan - Jakarta Selatan",
    "Jalan Dewi Sri no. 18 Kuta\nBali – Indonesia",
    "Jl. Bikini Utama #1A\nDenpasar, Bali",
    "Kantor\nPergudangan Commpark Kota Wisata,Blok C No.6 Limusnunggal Cileungsi Kab.Bogor,Jawa Barat",
    "Address:\nJl. Raya Bekasi Tambun Km 39,5\nBekasi 17510, Indonesia",
    "Jl. KIG Raya Selatan Kav. C-5\nKawasan Industri Gresik 61121\nSurabaya - Indonesia",
    "Kebayoran Village Blok A 22\nJalan Boulevard Bintaro Jaya\nBintaro Jaya Sektor 7\nTangerang Selatan 15224",
    "Jalan Cantel no. 10, Jogjakarta 55165",
    "Jalan Gondosuli UH1/565, jogjakarta 55166",
    "Taman Niaga Sukajadi C-1B Batam, Indonesia 29462",
    "No. 10, Suren 1\nJakarta Selatan",
    "Lt-1.Gedung Dana Pensiun BRI, Lt-1.Jl. Veteran II, No. 15, Jakarta – Pusat (10110).",
    "Jalan Veteran II No.15, Gedung Dana Pensiun BRI Lt. 1, RT.5/RW.2, Gambir, Kecamatan Gambir, Kota Jakarta Pusat, Daerah Khusus Ibukota Jakarta 10110",
    "Panbil Plaza, JL Ahmad Yani Muka Kuning Batam 2933, Indonesia",
    "Jl. Scientia Boulevard Kav. U2,\nSummarecon Serpong,\nTangerang, Banten 15811 – Indonesia",
    "Address: Graha Anabatic, Jl. Scientia Boulevard Kav. U2, Summarecon Serpong, Tangerang, Banten 15811 – Indonesia",
    "NWP Retail\nMenara Jamsostek 8th Floor, North Tower\nJln. Jendral Gatot Subroto Kav. 38, Jakarta 12710",
    "Jl. Ahmad Yani KM 2, Banjarmasin, South Kalimantan",
    "Jalan Batu Jangkih Sepi Mungkung, Selong Belanak, Mangkung, West Praya, Kabupaten Lombok Tengah, West Nusa Tenggara, Lombok, Indonesia 83571",
    "Address\nDesa Asem Kandang M 24\nKraton – Pasuruan 67151\nEast Java – Indonesia",
    "Jl. Jendral Gatot Subroto No. 79 Jakarta Selatan Indonesia 12930",
    "JL. SUNSET ROAD TENGGAH, KUTA - BADUNG BALI DENPASAR - BALI, 80233",
    "JL. AHMAD YANI NO. 154. SUMUR PECUNG, SERANG. PROVINSI BANTEN",
    "LT. 8 TOWER B JL. GATOT SUBROTO NO. 38 KAV. 71-73 PANCORAN JAKARTA SELATAN, JAKARTA 12710",
    "JL. PEMUDA NO. 130 SEMARANG 50132, KOTA SEMARANG 50132",
    "JL. RAYA JUANDA NO 52 SEDATI - SIDOARJO, SURABAYA 61253",
    "JL. PH. HASAN MUSTAPA NO. 39 BANDUNG (LANTAI 3) BANDUNG 40124",
    "JL. MARSMA R. ISWAHYUDI RT 6 NO 58 SEPINGGAN RAYA BALIKPAPAN, BALIKPAPAN 76113",
    "JL. GUNUNG BAWAKARAENG NO. 222 MAKASSAR 90144, MAKASSAR 90144",
    "JL. BASUKI RAHMAT 1303 A - B RT. 20 RW. 008 KEL. 20 ILIR II KEC. KEMUNING, KOTA PALEMBANG, PALEMBANG 30126",
    "JL. KAPTEN PATTIMURA NO. 334 LANTAI II, MEDAN 20153",
    "JL. ARIFIN ACHMAD KOMPLEK PERKANTORAN MEGA ASRI GREEN OFFICE RUKAN A11-A12 PEKANBARU - RIAU, PEKANBARU 28294",
    "Jalan Kebon Jeruk Raya No. 27, Kemanggisan, Jakarta Barat - 11530",
    "Grha Tirtadi 3/F, Jl.Raden Saleh No. 20\n10430 Jakarta",
    "Jl. Kebun Jambu No. 7 Kapuk Jakarta Barat 11720 Indonesia",
    "Jalan Cijerokaso Cluster Green Residence Unit E, Sarijadi, Kec. Sukasari, Kota Bandung, Jawa Barat 40151",
    "Address: Jln.Cemara no.13 , Kebayoran Baru\nJakarta 12110 – Indonesia",
    "2nd Floors\nJalan Raya Lukluk Darmasaba\nBadung - Bali, Indonesia",
    "HK Tower Lt. 15, Jl. Letjen Mt. Haryono No. Kav 8, RT 12/RW 11 Cawang, Kecamatan Jatinegara Jakarta Timur 13340",
    "KANTOR\nTaman Pegangsaan Indah, Blok A No. 3-5\nJl. Pegangsaan Dua, Jakarta Utara 14250, Indonesia",
    "Jl. Kampung Bulu No. 29\nSetia Mekar, Tambun - Bekasi, 17510 Indonesia",
    "Jl. Raya Setu No. 9\nDesa Telajung - Setu, Cibitung",
    "Jl. Dr. Sutomo 6-8 Jakarta 10710 Indonesia",
    "Gedung B.J. Habibie Lantai 15\nJl. M.H Thamrin No. 8 Jakarta Pusat DKI Jakarta 10340",
    "Menara Karya, Lantai 16\nJL. H.R. Rasuna Said, Blok X-5,\nKav. 1-2 Jakarta 12950 - Indonesia",
    "Menara Bosowa\nJl. Jend. Sudirman, Ujung Pandang\nMakassar, Sulawesi Selatan 90113 - Indonesia",
    "Jalan Ahmad Yani No. 100 Kab. Banyuwangi Prov. Jawa Timur\nKode Pos : 68425",
    "Jl. Kemang Timur No.21, Jakarta Selatan",
    "Jl. Teuku Umar Barat No. 18 Denpasar, Bali",
    "Jl. Raya Sukawati, Batuan, Kec. Sukawati, Kab. Gianyar, Bali 80582",
    "Jl. Ir Soekarno No 88A Br Anyar, Kec. Kediri, Kab. Tabanan, Bali",
    "Jl. MT. Haryono No. 21-22 A-B RT 054, Kel Damai, Balikpapan Selatan",
    "Jl. Mr. T. Mohammad Hasan, Batoh, Kec Luengbata, Banda Aceh",
    "Jln Mawar No 32 B dan C, RT 04 RW 05, Kel Balik Alam, Kec Mandau, Duri",
    "Rukan Pesona View Blok B1, Jl. Ir. H. Juanda, Sukamaju, Mekar Jaya, Sukmajaya, Depok",
    "Ruko Talangsari Blok B-2 Jl. KH. Wahid Hasyim, Talangsari, Jember Kidul, Kab Jember",
    "Ruko PO Haryanto No. 4, Jl. Lingkar Timur 003/002, Kec Jati, Kab Kudus",
    "Jalan ST Alauddin No.91 RT 008/005 Kelurahan Pa Baeng – Baeng, Kecamatan Tamalate, Kota Makasar",
    "Kawasan Megamas Jl. A. J Sondakh Ruko Mega Profit Blok 1F2 No. 46 dan 47, Manado",
    "Komplek CBD Polonia Blok BB No.50 Kelurahan Sukadamai, Kecamatan Medan, Medan",
    "Jl. Arcamanik Endah No.11, Bandung, Indonesia 40293",
    "JL. MEDAN MERDEKA BARAT NO. 8 JAKARTA PUSAT\nDKI JAKARTA 10110",
    "Sentra Bisnis Thamrin Residence Blok RB No. 15\nJl. KH Mas Mansyur\nJakarta 10230 - Indonesia",
    "Jl. Raya Cakung Cilincing Kav 48 - 50,\nKelurahan Cakung Timur, Kecamatan Cakung, Jakarta Timur, DKI Jakarta 13910, Indonesia",
    "Jl. Raya Bandara Juanda No. 5,\nDesa Sedati Agung, Kecamatan Sedati\nSidoarjo, Jawa Timur 61253, Indonesia",
    "Address\nJl. Jend RS. Dr. Soekanto No.15, Pondok Kopi\nJakarta Timur Indonesia 13460",
    "Jl. Letda Nasir No. 70 Bojong Kulur\nJati Asih, Bekasi - Jawa Barat",
    "Ruko The Spring Blok SP Selatan No.43\nJl. Raya Telaga Gading Serpong,\nTangerang, 15810",
    "Jl. P. Jayakarta 117 Blok B 52-54 Jakarta 10730 INDONESIA",
    "Jl. Cijerah No. 19 Bandung 40213",
    "Majapahit Permai Blok B No. 120-121\nJl. Majapahit No. 18-22,\nJakarta 10160",
    "Jl. Jati Raya Blok J1 No 11,J 10 No 1E ,J10 No 1D Newton Techno Park Lippo Cikarang",
    "Jln. Pangeran Tubagus Angke Komp. Duta Square Blok A.8 – Jelambar, Jakarta Barat, 11460",
    "Address :\nKompek Duta Square Blok A No. 8\nJln. Pangeran Tubagus Angke\nJelambar - Jakarta Barat\nIndonesia 11460"
]

phones = [
    "+6221 719 0011",
    "(62-21) 600 9087",
    "(62-22) 6031235",
    "(62-21) 6009087",
    "+62-21-5839-7777",
    "66527513",
    "+62 274 562811",
    "+62 2941 9696",
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
                "(" +
                    "(" +
                        "(Address)|(Alamat)|(Jalan)|(Jln\W)|(Jl\W)|(Menara)|([^\n]{,20}Tower)|(OFFICE)|((?<!\w)KANTOR\W)|((?<!\W)Lt\W)|([^\n]{,40}Blok)|(Graha)|(Taman)" +
                    ")" +
                    "(" +
                        "[^}{$@*<>]{5,150}" +
                    ")" +
                    "(" +
                        "(\D\d{5}(?!\w))|(Indonesia)|" +
                        "(Bangka([\s\-]Belitung)?)|(Banten)|(Bengkulu)|(Gorontalo)|(Sumatera[–\s\-]{1,3}Utara)|(Sumatera[–\s\-]{1,3}Selatan)|(Sumatera[–\s\-]{1,3}Barat)|(Sumatera)|" + 
                        "(Jakarta[–\s\-]{1,3}Selatan)|(Jakarta[–\s\-]{1,3}Barat)|(Jakarta[–\s\-]{1,3}Utara)|(Jakarta[–\s\-]{1,3}Pusat)|(Jakarta[–\s\-]{1,3}Timur)|(Jakarta)|" + 
                        "(Kalimantan[–\s\-]{1,3}Selatan)|(Kalimantan[–\s\-]{1,3}Barat)|(Kalimantan[–\s\-]{1,3}Utara)|(Kalimantan[–\s\-]{1,3}Tengah)|(Kalimantan[–\s\-]{1,3}Timur)|(Kalimantan)|" + 
                        "(Jawa[–\s\-]{1,3}Barat)|(Jawa[–\s\-]{1,3}Timur)|(Jawa[–\s\-]{1,3}Tengah)|(Papua[–\s\-]{1,3}Barat)|(Papua)|(Yogyakarta)|(\WAceh)|(\WBali)|" + 
                        "(Riau)|(Lampung)|(Maluku)|(Maluku[–\s\-]{1,3}Utara)|(Nusa Tenggara[–\s\-]{1,3}Barat)|(Nusa Tenggara[–\s\-]{1,3}Timur)|(Nusa Tenggara)|" + 
                        "(Sulawesi[–\s\-]{1,3}Selatan)|(Sulawesi[–\s\-]{1,3}Barat)|(Sulawesi[–\s\-]{1,3}Utara)|(Sulawesi[–\s\-]{1,3}Tenggara)|(Sulawesi[–\s\-]{1,3}Tengah)|(Sulawesi)" +
                        "(Daerah\s[^\n]{3,25})"
                    ")" +
                ")"
            ]


'''
not_matched_counter = 0
p_matchedcounter = 0
for add in addresses:
    #print(add.replace("\n", " "), " >>> ", len(add))
    m = re.search(address_patterns[0], add, flags=re.IGNORECASE)
    if(not m):
        not_matched_counter += 1
        #print(m.group(0).replace("\n", " "))
        print(add.replace("\n", " "), " >>> ", len(add))
        print(50 * "*")
    elif(add != m.group(0)):
        p_matchedcounter += 1
        print(add.replace("\n", " "),  " >>> ", len(add))
        print(m.group(0).replace("\n", " "))
        print(50 * "*")

print("all: ", len(addresses))
print("not: ", not_matched_counter)
print("partial: ", p_matchedcounter)
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


from root.website_tools.company_website import website_info
'''
samples = json.loads(open(os.path.join("samples", "indonesia", "samples.json"), mode="r", encoding="utf-8").read())
all_data = []
for sample in samples[:1]:
    if(sample["Website"] != "-"):
        data = website_info(sample["Website"], sample["Organization Name"], "id", country="indonesia")
        all_data.append(data)
        print(50 * "*")

        with open(os.path.join("output", "indonesia", "add_regex_test.json"), mode="w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(all_data, indent=4, ensure_ascii=False))
'''
dic = {
    "Organization Name": "BINUS Alumni Relation Office - ARO,Indonesia",
    "Website": "www.jingga-architect.com"
}

data = website_info(dic["Website"], dic["Organization Name"], "id", country="indonesia")
print(json.dumps(data, indent=4, ensure_ascii=False))