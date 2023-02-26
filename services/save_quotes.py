from api.api import Exchange
from datetime import datetime
import json

rates = Exchange()


def save_rates_to_file():
    google = rates.get_google_exchange('latest')
    mig = rates.get_mig_exchange()
    response_time = datetime.now().strftime("%d:%m:%Y %H:%M")

    json_file = {"update_time": response_time, "google": google, "mig": mig}

    json_object = json.dumps(json_file, indent=4)

    with open("services/quotes.json", "w") as outfile:
        outfile.write(json_object)
