import json

offices_info = "core/services/offices.json"


async def get_address_info(district: str):

    with open(offices_info, encoding='utf8') as openfile:
        addresses: dict = json.load(openfile)

    text = []

    for keys, values in addresses[district].items():
        text.append(f"<b>Номер отделения</b>: {keys}\n"
                    f"<b>Адрес</b>: {values['address']}\n"
                    f"<b>График работы</b>: {values['shift']}\n"
                    f"<b>Тел.</b>: {values['phones'].replace('-', '')}\n"
                    f"<b>На карте</b>: {values['link']}\n\n")

    return ''.join(text)
