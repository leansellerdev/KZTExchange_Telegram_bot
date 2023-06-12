from datetime import datetime
import json
from core.api.api import rates


class QuotesData:

    """
    This class is using for work with quotes and write/read it to json file
    """

    file = "core/services/quotes.json"

    @staticmethod
    async def collect_data():
        google_data = await rates.get_google_exchange('latest')
        mig_data = await rates.get_mig_exchange()

        response_time = datetime.now().strftime("%d:%m:%Y %H:%M")

        json_file = {"update_time": response_time, "google": google_data, "mig": mig_data}
        return json.dumps(json_file, indent=4)

    async def save_data(self):
        json_object = await self.collect_data()

        with open(self.file, "w") as outfile:
            outfile.write(json_object)

    async def get_data(self):
        file = open(self.file)

        if file:
            return json.load(file)

        file.close()


data = QuotesData()
