# backend/services/oui_lookup.py

import re
import requests

OUI_URL = "https://standards-oui.ieee.org/oui.txt"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
}


def download_oui():
    r = requests.get(OUI_URL, headers=headers)
    r.raise_for_status()
    return r.text


def parse_oui(raw_text):
    """
    Parse IEEE oui.txt format and return dict {mac_prefix: vendor_name}
    """
    oui_map = {}
    pattern = re.compile(r"^([0-9A-F]{6})\s+\(base 16\)\s+(.+)$", re.MULTILINE)
    matches = pattern.findall(raw_text)
    for mac, vendor in matches:
        oui_map[mac.upper()] = vendor.strip()
    return oui_map


def load_oui_map():
    raw = download_oui()
    return parse_oui(raw)


# Usage example:
# OUI_MAP = load_oui_map()
# vendor = OUI_MAP.get(mac[:6].upper())
