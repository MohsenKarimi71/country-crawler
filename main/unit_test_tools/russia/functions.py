from root.general_tools.tools import load_country_context, json2composite
from root.country_tools.russia.russia_country_module_tools import getRussianCompanyInfo
import re

def test_json2composite_russia(json_obj):
    return json2composite(json_obj, "russia")


def test_getRussianCompanyInfo(domain, org_name):
    data = getRussianCompanyInfo(domain, org_name, language="ru")
    return data
