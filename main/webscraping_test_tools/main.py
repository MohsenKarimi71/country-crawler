from test_tools.tools import text_out_test, test_domain, excel_out_test, test_composite, json_out_test
from general_tools.tools import load_country_context
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

vietnam_samples_path = os.path.join(dir_path, "test_tools", "samples", "vietnam.json")
vietnam_context = load_country_context("vietnam", add_with_global_setting=False)

brazil_samples_path = os.path.join(dir_path, "test_tools", "samples", "brazil.json")
brazil_context = load_country_context("brazil", add_with_global_setting=False)

mexico_samples_path = os.path.join(dir_path, "test_tools", "samples", "mexico.json")
mexico_context = load_country_context("mexico", add_with_global_setting=False)

russia_samples_path = os.path.join(dir_path, "test_tools", "samples", "russia.json")
russia_context = load_country_context("russia", add_with_global_setting=False)

# vietnam test
#text_out_test(os.path.join(dir_path, "output", "vietnam", "vietnam-result.txt"), "vietnam", vietnam_samples_path, "vi")
#test_domain("www.vsip.com.vn", "vsip", "vietnam", "vi")
#test_regex(vietnam_context["address_patterns"][0], "text")
#test_addresses(vietnam_context["address_patterns"][0], vietnam_samples_path)
#domains2url(vietnam_samples_path)
#excel_out_test(os.path.join(dir_path, "output", "vietnam", "vietnam-result.xlsx"), "vietnam", vietnam_samples_path, "vi")

# brazil test
#text_out_test(os.path.join(dir_path, "output", "brazil", "brazil-result.txt"), "brazil", brazil_samples_path, "pt")
#test_domain("www.disksistema.com.br", "disksistema", "brazil", "pt")
#test_regex(brazil_context["address_patterns"][0], "text")
#test_addresses(brazil_context["address_patterns"][0], brazil_samples_path)
#domains2url(brazil_samples_path)
#excel_out_test(os.path.join(dir_path, "output", "brazil", "brazil-result.xlsx"), "brazil", brazil_samples_path, "pt")

# mexico test
#text_out_test(os.path.join(dir_path, "output", "mexico", "mexico-result.txt"), "mexico", mexico_samples_path, "es")
#test_domain("www.spt.vn", "spt", "mexico", "es")
#test_regex(mexico_context["address_patterns"][0], "text")
#test_addresses(mexico_context["address_patterns"][0], mexico_samples_path)
#domains2url(mexico_samples_path)
#excel_out_test(os.path.join(dir_path, "output", "mexico", "mexico-result.xlsx"), "mexico", mexico_samples_path, "es")

# russia test
#text_out_test(os.path.join(dir_path, "output", "russia", "russia-result.txt"), "russia", russia_samples_path, "ru")
#json_out_test(os.path.join(dir_path, "output", "russia", "russia-result.json"), "russia", russia_samples_path, "ru")
#test_domain("www.vitec.ru", "vitec", "russia", "ru")
#test_regex(russia_context["address_patterns"][0], "text")
#test_addresses(russia_context["address_patterns"][0], russia_samples_path)
#domains2url(russia_samples_path)
#excel_out_test(os.path.join(dir_path, "output", "russia", "russia-result.xlsx"), "russia", russia_samples_path, "ru")

# composite tese
# russia test
test_composite(os.path.join(dir_path, "output", "russia", "russia_composite.json"), os.path.join(dir_path, "test_tools", "samples", "russia_complate.json"), "russia")
