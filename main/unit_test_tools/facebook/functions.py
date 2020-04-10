from root.facebook_tools.tools import verify_facebook_link

def test_verify_facebook_link(link, domain, country, phone_prefix):
    return verify_facebook_link(link, domain, country, phone_prefix)