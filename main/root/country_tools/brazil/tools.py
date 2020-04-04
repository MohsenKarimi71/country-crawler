from root.general_tools.tools import get_google_formatted_address_using_address
import re

# VARIABLES
to_be_deleted_from_address = [" av. ", "avenida", " R. ", " rua ", " rod ", "rodovia", "praça", " cep", ":", " andar", " sala", " centro", " departamento", " conj", "caixa postal"]
cep_regex = "\d{2}\D?\d{3}\D?\d{3}"
number_founder_pattern = "[^\d]?(\d+)[^\d]?"

sep_ptr = "(\s?(\s|-|–|,|\.|/|\|)\s?)"
cep_ptr = "(cep:?" + sep_ptr + ")?" + "(\d{2}\D?\d{3}(-|–|\s)\d{3})"
country_ptr = "(brasil)"
city_state_ptr = "((\w[\w\s]?)" + sep_ptr + "((AC)|(AL)|(AM)|(AP)|(BA)|(CE)|(DF)|(ES)|(GO)|(MA)|(MG)|(MS)|(MT)|(PA)|(PB)|(PE)|(PI)|(PR)|(RJ)|(RN)|(RO)|(RR)|\
(RS)|(SC)|(SE)|(SP)|(TO)|(Acre)|(Alagoas)|(Amazonas)|(Amapá)|(Bahia)|(Ceará)|(Distrito Federal)|(Espírito Santo)|(Goiás)|(Maranhão)|(Minas Gerais)|\
(Mato Grosso do Sul)|(Mato Grosso)|(Pará)|(Paraíba)|(Pernambuco)|(Piauí)|(Paraná)|(Rio de Janeiro)|(Rio Grande do Norte)|(Rondônia)|(Roraima)|(Rio Grande do Sul)|\
(Santa Catarina)|(Sergipe)|(São Paulo)|(Tocantins)))"

end_patterns = [
    city_state_ptr + sep_ptr + cep_ptr + sep_ptr + country_ptr,
    cep_ptr + sep_ptr + city_state_ptr + sep_ptr + country_ptr,
    cep_ptr + sep_ptr + country_ptr + sep_ptr + city_state_ptr,
    city_state_ptr + sep_ptr + country_ptr + sep_ptr + cep_ptr,
    country_ptr + sep_ptr + city_state_ptr + sep_ptr + cep_ptr,
    country_ptr + sep_ptr + cep_ptr + sep_ptr + city_state_ptr,

    city_state_ptr + sep_ptr + country_ptr,
    cep_ptr + sep_ptr + country_ptr,
    cep_ptr + sep_ptr + city_state_ptr,
    city_state_ptr + sep_ptr + cep_ptr,
    country_ptr + sep_ptr + cep_ptr,
    country_ptr + sep_ptr + city_state_ptr,

    city_state_ptr + "(?!\w)",
    cep_ptr,
    country_ptr,
]

start_pattern = "\
(\
(\W?AV\.?)|(\W?Av\.?)|(\W?av\.?)|(Avenida)|(AVENIDA)|(avenida)|\
(\W?RUA\W?)|(\W?Rua\W?)|(\W?R\.)|(\W?rua\W?)|\
(Rod)|(ROD)|(Rodovia)|(RODOVIA)|(Praça)|(praça)|(PRAÇA)\
)\
([\W\w]{5,100}?)\
"

brazil_states = {
    "AC":"Acre",
    "AL":"Alagoas",
    "AM":"Amazonas",
    "AP":"Amapá",
    "BA":"Bahia",
    "CE":"Ceará",
    "DF":"Distrito Federal",
    "ES":"Espírito Santo",
    "GO":"Goiás",
    "MA":"Maranhão",
    "MG":"Minas Gerais",
    "MS":"Mato Grosso do Sul",
    "MT":"Mato Grosso",
    "PA":"Pará",
    "PB":"Paraíba",
    "PE":"Pernambuco",
    "PI":"Piauí",
    "PR":"Paraná",
    "RJ":"Rio de Janeiro",
    "RN":"Rio Grande do Norte",
    "RO":"Rondônia",
    "RR":"Roraima",
    "RS":"Rio Grande do Sul",
    "SC":"Santa Catarina",
    "SE":"Sergipe",
    "SP":"São Paulo",
    "TO":"Tocantins"
}

# FUNCTIONS
def find_brazilian_addresses(text, patterns):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        if(items):
            for item in items:
                # cleaning addresses
                add = re.sub("\n", " ", item[0])
                add = add.strip()
                if(re.search("^.R\.", add)):
                    add = add[1:]
                if(re.search("\D\d{2}\D?\d{3}(-|–)\d{3}\D$", add)):
                    add = add[:-1]
                add = re.sub("'|\(|\)", " ", add)
                add = re.sub('"', " ", add)
                add = re.sub("\s{2,}", " ", add)
                found_addresses.append(add)
    return list(set(found_addresses))


def recheck_brazilian_address(address):
    adds = []
    max_address_found = 0
    for ptr in end_patterns:
        full_pattern = "(" + start_pattern + ptr + ")"
        items = re.findall(full_pattern, address, flags=re.IGNORECASE)
        if(items):
            if(len(items) > max_address_found):
                adds = []
                max_address_found = len(items)
                for item in items:
                    adds.append(item[0])
    if(len(adds) == 0):
        adds.append(address)
    return adds

def get_brazilian_unique_addresses(address_list):
    unique_addresses = []
    if(len(address_list) > 1):
        filtered_add_list = [" " + add for add in address_list]
        filtered_add_list = [add.lower() for add in filtered_add_list]
        temp_list = [add for add in filtered_add_list]
        filtered_add_list = []
        # deleting common words
        for add in temp_list:
            for phrase in to_be_deleted_from_address:
                add = add.replace(phrase, " ")
            filtered_add_list.append(add)
        temp_list = [add for add in filtered_add_list]
        filtered_add_list = []
        # extracing CEP number and spliting on ','
        for add in temp_list:
            cep = None
            m = re.search(cep_regex, add)
            if(m):
                cep = m.group(0)
                add = add.replace(cep, " ")
            add = re.sub("-|–|/|,|\.|\|", " ", add)
            add = (re.sub("\s{2,}", " ", add)).strip()
            add = add.split(" ")
            if(cep):
                cep = re.sub("[\D]", "", cep)
                add.append(cep)
            filtered_add_list.append(add)
        
        temp_list = [add for add in filtered_add_list]
        filtered_add_list = []
        # extracting all numbers
        for splitted_list in temp_list:
            word_list = []
            for word in splitted_list:
                m = re.search(number_founder_pattern, word)
                if(m):
                    word_list.append(m.group(1))
                    word = re.sub(m.group(0), " ", word)
                word = (re.sub("\s{2,}", " ", word)).strip()
                if(not word.endswith(".")):
                    if(len(word) >= 2):
                        word_list.append(word)
            word_list = list(set(word_list))
            filtered_add_list.append(word_list)

        # getting unique addresses
        max_length = 0
        max_index = 0
        for i in range(len(filtered_add_list)):
            if(len(filtered_add_list[i]) > max_length):
                max_length = len(filtered_add_list[i])
                max_index = i
        unique_addresses.append({"original":address_list[max_index], "splitted":filtered_add_list[max_index]})

        for index1, splitted_list in enumerate(filtered_add_list):
            if(len(splitted_list) > 0):
                is_unique = True
                if(index1 != max_index):
                    add_results = {"original":address_list[index1], "splitted":splitted_list}
                    for index2, unq_dic in enumerate(unique_addresses):
                        if(len(unq_dic["splitted"]) > len(splitted_list)):
                            score = 0
                            for word in splitted_list:
                                if(word in unq_dic["splitted"]):
                                    score += 1
                            if(score / len(splitted_list)) > 0.6:
                                unique_addresses[index2]["splitted"] = list(set(unique_addresses[index2]["splitted"] + splitted_list))
                                is_unique = False
                                break
                        else:
                            score = 0
                            for word in unq_dic["splitted"]:
                                if(word in splitted_list):
                                    score += 1
                            if(score / len(unq_dic["splitted"])) > 0.6:
                                unique_addresses[index2]["splitted"] = list(set(unique_addresses[index2]["splitted"] + splitted_list))
                                unique_addresses[index2]["original"] = address_list[index1]
                                is_unique = False
                                break
                    if(is_unique):
                        unique_addresses.append(add_results)
            
        unique_addresses = [dic["original"] for dic in unique_addresses]
        return unique_addresses
    else:
        return address_list

def get_brazilian_address_parts(address, language="pt"):
    temp = address
    parts = {
        "country":"Brasil",
        "state":"",
        "city":"",
        "postal-code":"",
        "street-address":"",
    }

    address = re.sub("cep\s?:?", " ", address, flags=re.IGNORECASE)
    address = re.sub("brasil", " ", address, flags=re.IGNORECASE)

    m = re.search(cep_regex, address)
    if(m):
        parts["postal-code"] = m.group(0)
        address = re.sub(m.group(0), " ", address)

    address = re.sub("-|–|/|\|", ",", address)
    address = re.sub("\s{2,}", " ", address)
    address = address.split(",")
    address = [part.strip() for part in address if part.strip() != ""]

    state = is_brazilian_state(address[-1])
    if(state):
        if(len(address) >= 2):
            parts["state"] = state
            city_parts = address[-2].split(" ")
            parts["city"] = city_parts[-1]
            address[-2] = address[-2].replace(city_parts[-1], "").strip()

            parts["street-address"] = ", ".join(i for i in address[:-1])
        else:
            parts["street-address"] = ", ".join(i for i in address)
    else:
        print("Splitting not successfull. Using google ...")
        # using google API to find formatted address
        address_dic = get_google_formatted_address_using_address(temp, language)
        if(address_dic):
            return {"address":address_dic["address"], "components":address_dic["components"], "source": "google_geo_api"}

    return {"address":temp, "components":parts, "source":"company-website"}

def purify_brazilian_addresses(address_list):
    '''
    get a list of brazilian addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = []
    for address in address_list:
        adds = recheck_brazilian_address(address)
        for add in adds:
            if(not add in rechecked_addresses):
                rechecked_addresses.append(add)
    
    unique_addresses = get_brazilian_unique_addresses(rechecked_addresses)

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_brazilian_address_parts(add))
    return splitted_addresses


def find_brazilian_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for item in items:
            phone = item[0]
            if(len(phone) >= 12 and "\n" not in phone):
                phones.append(phone)
    return list(set(phones))

def purify_brazilian_phones(phone_list):
    '''
    This function takes a list of phone numbers as input, extracts all unique 
    phone numbers from input list and finally return a list of unique phone numbers.
    '''
    if(phone_list):
        if(len(phone_list) == 1):
            return phone_list
        else:
            unique_phones = []
            filtered_list = [re.sub("[\D]", "", phone)[-10:] for phone in phone_list]

            unique_phones.append({"original": phone_list[0], "filtered":filtered_list[0]})
            for i in range(1, len(phone_list)):
                is_unique = True
                for dic in unique_phones:
                    if(filtered_list[i] == dic["filtered"]):
                        is_unique = False
                        break
                if(is_unique):
                    unique_phones.append({"original": phone_list[i], "filtered":filtered_list[i]})
            return [dic["original"] for dic in unique_phones]
    else:
        return []


def is_brazilian_state(phrase):
    for tup in brazil_states.items():
        if(phrase.upper() == tup[0] or phrase.upper() == tup[1].upper()):
            return tup[1]
    return False


