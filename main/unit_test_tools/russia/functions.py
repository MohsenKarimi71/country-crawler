from root.general_tools.tools import load_country_context, json2composite
import re

def test_json2composite_russia(json_obj):
    return json2composite(json_obj, "russia")