import json

json_file = "offices.json"


def get_address_info(district: str):

    with open(json_file, encoding='utf8') as openfile:
        addresses: dict = json.load(openfile)

    text = []

    for keys, values in addresses[district].items():
        text.append(f"Номер отделения: {keys}\nАдрес: {values['address']}\n"
                    f"График работы: {values['shift']}\nКонтакты: {values['phones']}\n\nНа карте: {values['link']}\n\n")

    return ''.join(text)
