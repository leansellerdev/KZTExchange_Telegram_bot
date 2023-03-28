from datetime import datetime
import json
from core.api.api import rates


class QuotesData:

    """
    This class is using for work with quotes and write/read it to json file
    """

    google_data = rates.get_google_exchange('latest')
    mig_data = rates.get_mig_exchange()
    response_time = datetime.now().strftime("%d:%m:%Y %H:%M")
    file = "core/services/quotes.json"

    def collect_data(self):

        json_file = {"update_time": self.response_time, "google": self.google_data, "mig": self.mig_data}
        return json.dumps(json_file, indent=4)

    def save_data(self):
        json_object = self.collect_data()

        with open(self.file, "w") as outfile:
            outfile.write(json_object)

    def get_data(self):
        file = open(self.file)

        if file:
            return json.load(file)


data = QuotesData()
