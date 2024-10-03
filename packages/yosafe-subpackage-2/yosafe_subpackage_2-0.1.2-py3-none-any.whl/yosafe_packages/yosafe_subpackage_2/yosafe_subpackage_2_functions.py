from requests import get
from yosafe_packages.yosafe_subpackage_1.yosafe_subpackage_1_functions import to_capitllal_letters


def yosafe_get_yosafe_subpackage_2():
    text = "yosafe_subpackage_2"
    url = "https://cowsay.morecode.org/say"
    params = {
        "message": text,
        "format": "text",
    }
    response = get(url, params=params)
    if response.status_code == 200:
        return response.text 
    else:
        return f"Error: {response.status_code} - Could not retrieve ASCII art."


def yosafe_sub(a, b):
    return a - b


def to_capitllal_letters_2(txt: str) -> str:
    return to_capitllal_letters(txt)


