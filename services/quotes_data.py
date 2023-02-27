from datetime import datetime
import json
from api.api import rates


def collect_data():
    google = rates.get_google_exchange('latest')
    mig = rates.get_mig_exchange()
    response_time = datetime.now().strftime("%d:%m:%Y %H:%M")

    json_file = {"update_time": response_time, "google": google, "mig": mig}
    return json.dumps(json_file, indent=4)


def save_data():
    json_object = collect_data()

    with open("services/quotes.json", "w") as outfile:
        outfile.write(json_object)


def get_data():
    file = open("services/quotes.json")

    if file:
        return json.load(file)
