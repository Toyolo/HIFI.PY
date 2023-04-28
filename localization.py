import json

# Load localized texts
with open("localized_texts.json", "r") as file:
    localized_texts = json.load(file)

def get_localized_text(language_code, key):
    """
    Get the localized text for the specified language code and key.

    :param language_code: The language code (e.g., 'en', 'fr', 'de').
    :param key: The key of the localized text.
    :return: The localized text.
    """
    if language_code in localized_texts and key in localized_texts[language_code]:
        return localized_texts[language_code][key]
    elif key in localized_texts["en"]:
        return localized_texts["en"][key]
    else:
        return key

