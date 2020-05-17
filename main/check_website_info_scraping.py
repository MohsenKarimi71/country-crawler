import json
import csv
import os
from root.website_tools.company_website import website_info

'''
input_file = "c:/temp/country_samples/200 Indonesia Samples.csv"
cases = []
with open(input_file, "r", encoding="utf-8") as infile:
    csy_reader = csv.DictReader(infile, delimiter=',',
                            fieldnames=['organization', 'country', 'website'])
    for row in csy_reader:
        cases.append(dict(row))
    cases.pop(0)
'''

cases = json.loads(open(os.path.join("samples", "germany", "samples.json"), mode="r", encoding="utf-8").read())
print(len(cases))

country = "germany"
all_counters = []
sum_of_all_counters = {}

titles = ["logo_url", "web_title", "social_pages", "phones", "emails", "addresses", "status_code"]
for n in titles:
    sum_of_all_counters[n] = 0

with open('innovators.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(['domain'] + titles)


all_data = []
for i, input_data in enumerate(cases[:]):
    print(i, " >>> ", input_data)
    r = website_info(input_data["Website"], input_data["Organization Name"], country)
    all_data.append(r)

    with open("germany_result.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(all_data, indent=4, ensure_ascii=False))
        #print(json.dumps(r, indent=4, ensure_ascii=False))

    result = r.get("result", "")
    domain = r.get("domain", "NO DOMAIN")
    values = []
    counters = []
    if result:
        for k in titles:
            if type(result.get(k, "")) == list:
                v = str(result[k])
                count = len(result[k])
            elif type(result.get(k, "")) == dict:
                v = str(result[k])
                count = len(result[k].keys())
            elif type(result.get(k, "")) == str:
                v = "" if len(result.get(k,"")) == 0 else result[k]
                count = 1 if len(v) > 0 else 0
            elif type(result.get(k, "")) == int:
                v = result[k] if result[k]> 0 else 0
                count = v
            else:
                v = "Unknown Field !"
            values.append(v)
            counters.append(count)
            sum_of_all_counters[k] = sum_of_all_counters[k] + (1 if count > 0 else 0)

    else:
        values = ['INVALID DOMAIN', '', '', '', '', '']
        counters = [0, 0, 0, 0, 0, 0]
    
    with open('innovators.csv', 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow([domain] + values)
        all_counters.append([domain] + counters)
    print(sum_of_all_counters)
    print(50 * "##")


with open('counters.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow([domain] + titles)
    for c in all_counters:
        writer.writerow(c)
    
    writer.writerow(['SUM :'] + list(sum_of_all_counters.values()))