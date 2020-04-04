from root.general_tools.tools import get_google_formatted_address_using_address
import re
#from mylib.mymodules import fixed_title, save_logo

# VARIABLES
number_founder_pattern = "\D?(\d+)\D?"

mexican_states = {
    "Ags.":"Aguascalientes",
    "B.C.":"Baja California",
    "BC.":"Baja California",
    "B.C.S.":"Baja California Sur",
    "BCS.":"Baja California Sur",
    "Camp.":"Campeche",
    "Chis.":"Chiapas",
    "Chih.":"Chihuahua",
    "Coah.":"Coahuila",
    "Col.":"Colima",
    "CDMX":"México City",
    "Dgo.":"Durango",
    "Gto.":"Guanajuato",
    "Gro.":"Guerrero",
    "Hgo.":"Hidalgo",
    "Jal.":"Jalisco",
    "Méx.":"México",
    "Mich.":"Michoacán",
    "Mor.":"Morelos",
    "Nay.":"Nayarit",
    "N.L.":"Nuevo León",
    "NL.":"Nuevo León",
    "Oax.":"Oaxaca",
    "Pue.":"Puebla",
    "Qro.":"Querétaro",
    "Q.R.":"Quintana Roo",
    "QR.":"Quintana Roo",
    "S.L.P.":"San Luis Potosí",
    "SLP.":"San Luis Potosí",
    "Sin.":"Sinaloa",
    "Son.":"Sonora",
    "Tab.":"Tabasco",
    "Tamps.":"Tamaulipas",
    "Tlax.":"Tlaxcala",
    "Ver.":"Veracruz",
    "Yuc.":"Yucatán",
    "Zac.":"Zacatecas"
}

# FUNCTIONS
def find_mexican_addresses(text, patterns):
    found_addresses = []
    for pattern in patterns:
        items = re.findall(pattern, text, flags=re.IGNORECASE)
        for item in items:
            found_addresses.append(item[0])
    return list(set(found_addresses))

def recheck_mexican_address(address):
    if(" tel" in address):
        address = address.split(" tel")[0]
    elif(" Tel" in address):
        address = address.split(" Tel")[0]
    elif(" TEL" in address):
        address = address.split(" TEL")[0]
    address = re.sub("(MÃ©xico)|(Mexico)", "México", address, flags=re.IGNORECASE)
    address = re.sub("\n", " ", address)
    address = re.sub("\|", ",", address)
    address = re.sub("Dirección\s?\:?\s?", "", address, flags=re.IGNORECASE)
    address = re.sub("address\s?:\s?", "", address, flags=re.IGNORECASE)
    if((address.lower()).startswith("oficina")):
        m = re.search("(Oficinas?\s?:?\s?)", address, flags=re.IGNORECASE)
        temp = address.split(m.group(0))[1:]
        address = ""
        for part in temp:
            address += part
    address = address.strip()
    address = address.strip(",")
    address = re.sub("\s{2,}", " ", address)
    if(len(address.strip()) > 15 and len(address.strip()) < 120):
        return address.strip()
    else:
        return None

def get_mexican_unique_addresses(address_list):
    unique_addresses = []
    if(len(address_list) > 1):
        filtered_add_list = [add.lower() for add in address_list]
        for index, add in enumerate(filtered_add_list):
            for state in mexican_states.keys():
                if(state.lower() in add):
                    filtered_add_list[index] = filtered_add_list[index].replace(state.lower(), mexican_states[state].lower())
                    break

        filtered_add_list = [add.replace(",", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace(".", ". ") for add in filtered_add_list]
        filtered_add_list = [add.replace("-", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace("(", " ") for add in filtered_add_list]
        filtered_add_list = [add.replace(")", " ") for add in filtered_add_list]
        filtered_add_list = [re.sub("\s{2,}", " ", add) for add in filtered_add_list]
        filtered_add_list = [add.split(" ") for add in filtered_add_list]
        temp_list = [splitted_list for splitted_list in filtered_add_list]
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
            is_unique = True
            if(index1 != max_index):
                add_results = {"original":address_list[index1], "splitted":splitted_list}
                for index2, unq_dic in enumerate(unique_addresses):
                    if(len(unq_dic["splitted"]) > len(splitted_list)):
                        score = 0
                        for word in splitted_list:
                            if(word in unq_dic["splitted"]):
                                score += 1
                        if(score / len(splitted_list)) >= 0.6:
                            unique_addresses[index2]["splitted"] = list(set(unique_addresses[index2]["splitted"] + splitted_list))
                            is_unique = False
                            break
                    else:
                        score = 0
                        for word in unq_dic["splitted"]:
                            if(word in splitted_list):
                                score += 1
                        if(score / len(unq_dic["splitted"])) >= 0.6:
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

def get_mexican_address_parts(address, language="es"):
    temp = address
    parts = {
        "country":"México",
        "state":"",
        "city":"",
        "street-address":"",
        "zip-code":""
    }
    m = re.search("((c\.p\.\s?\d{5})|(cp\.\s?\d{5})|((?<!\w)\d{5}(?!\w)))", address, flags=re.IGNORECASE)
    if(m):
        parts["zip-code"] = re.sub("\D", "", m.group(0))
        temp = re.sub(m.group(0), "", temp)
    m = re.search("(\s?,\s?México$)", temp, flags=re.IGNORECASE)
    if(m):
        temp = re.sub(m.group(0), "", temp, flags=re.IGNORECASE)
    
    state_abr = ""
    for key in mexican_states.keys():
        if(key != "Col."):
            if(key in temp):
                state_abr = key
                parts["state"] = mexican_states[key]
                break
            else:
                ptr = "((Estado de " + mexican_states[key] + ")|(Edo\.\s?" + mexican_states[key] + "))"
                m = re.search(ptr, temp, flags=re.IGNORECASE)
                if(m):
                    state_abr = m.group(0)
                    parts["state"] = mexican_states[key]
                    break
        else:
            ptr = "((Estado de Colima)|(Edo\.\s?Colima))"
            m = re.search(ptr, temp, flags=re.IGNORECASE)
            if(m):
                state_abr = m.group(0)
                parts["state"] = "Colima"
                break
    
    if(not parts["state"]):
        for key in mexican_states.keys():
            if(mexican_states[key] not in ["México City", "México"]):
                if(mexican_states[key] in temp):
                    items = re.findall(mexican_states[key], temp, flags=re.IGNORECASE)
                    if(len(items) > 1):
                        parts["city"] = mexican_states[key]
                    state_abr = mexican_states[key]
                    parts["state"] = mexican_states[key]
                    break

    if(parts["state"]):
        if(state_abr.endswith(".")):
            state_abr = state_abr.replace(".", "\.")
        temp = re.sub(state_abr, "", temp, flags=re.IGNORECASE)
        temp = re.sub("(\s*,[\W]*$)", "", temp)
        temp = re.sub("(,\s*,)", ",", temp)
        temp = re.sub("(\s{2,})", " ", temp)
        if(not parts["city"]):
            splitted = temp.split(",")
            if(len(splitted) > 1):
                parts["city"] = splitted[-1].strip()
                parts["street-address"] = (",".join(i for i in splitted[:-1])).strip()
            else:
                splitted = temp.split(" ")
                if(len(splitted) > 1):
                    parts["city"] = splitted[-1].strip()
                    parts["street-address"] = (" ".join(i for i in splitted[:-1])).strip()
        else:
            parts["street-address"] = temp

    if(not parts["city"]):
        print("Splitting not successfull. Using google ...")
        # using google API to find formatted address
        
        address_dic = get_google_formatted_address_using_address(address, language)
        if(address_dic):
            return {"address":address_dic["address"], "components":address_dic["components"], "source": "google_geo_api"}

    return {"address":address, "components":parts, "source":"company-website"}

def purify_mexican_addresses(address_list):
    '''
    get a list of mexican addresses and return a list of unique
    and splitted addresses extracted from input addresses 
    '''
    rechecked_addresses = set()
    for address in address_list:
        new_add = recheck_mexican_address(address)
        if(new_add):
            rechecked_addresses.add(new_add)
    
    unique_addresses = get_mexican_unique_addresses(list(rechecked_addresses))

    splitted_addresses = []
    for add in unique_addresses:
        splitted_addresses.append(get_mexican_address_parts(add))
    return splitted_addresses


def find_mexican_phones(text, patterns):
    phones = []
    for pattern in patterns:
        items = re.findall(pattern, text)
        for i in items:
            phones.append(i)
    return list(set(phones))

def purify_mexican_phones(phone_list):
    '''
    This function takes a list of phone numbers as input, extracts all unique 
    phone numbers from input list and finally return a list of unique phone numbers.
    '''
    unique_phones = []
    if(phone_list):
        if(len(phone_list) == 1):
            return phone_list
        else:
            ten_digit_set = set()
            new_phones = []

            for phone in phone_list:
                numbers = re.sub("\D", "", phone).strip()[-10:]
                new_phones.append({"phone": phone, "numbers":numbers})
            for dic in new_phones:
                if(not dic["numbers"] in ten_digit_set):
                    if(("(" in dic["phone"] and ")" in dic["phone"]) or (not "(" in dic["phone"] and not ")" in dic["phone"])):
                        ten_digit_set.add(dic["numbers"])
                        unique_phones.append(dic["phone"])
            return unique_phones
    else:
        return []
