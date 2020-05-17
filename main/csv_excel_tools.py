import os
import json
import re

dir_path = os.path.dirname(os.path.abspath(__file__))
samples_path = os.path.join(dir_path, "samples")

def csv2json(csv_file_path):
    json_data = []
    infile = open(csv_file_path, mode='r', encoding='utf-8')
    lines = [line for line in infile]
    #titles = lines[0].split(',')
    #titles = [title.rstrip('\n') for title in titles]
    titles = ["Organization Name", "Website"]
    for line in lines[1:]:
        dic = {}
        line = line.rstrip('\n')
        info = line.split(',')
        if(len(info) >= len(titles)):
            info = []
            m = re.search('(.*),([^,]*)', line)
            info.append(m.group(1))
            info.append(m.group(2))
        for i, data in enumerate(info):
            dic[titles[i]] = data
        json_data.append(dic)
    return json_data

def csv2json2(csv_file_path):
    json_data = []
    infile = open(csv_file_path, mode='r', encoding='utf-8')
    lines = [line for line in infile]
    #titles = lines[0].split(',')
    #titles = [title.rstrip('\n') for title in titles]
    titles = ["Organization Name", "Website"]
    for line in lines[1:]:
        dic = {}
        line = line.rstrip('\n')
        info = line.split(',')
        if(len(info) >= len(titles)):
            m = re.search('(.*),([^,]*)', line)
            if(m.group(2) != "-"):
                json_data.append("http://" + m.group(2))
    return json_data


def get_csv_outputs(file_name, country):
    input_file_path = os.path.join(samples_path, country, file_name)
    output_file_path = os.path.join(samples_path, country, "samples.json")
    output_file_path2 = os.path.join(samples_path, country, "domain_only.json")

    data = csv2json(input_file_path)
    with open(output_file_path, mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))

    data = csv2json2(input_file_path)
    with open(output_file_path2, mode="w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))