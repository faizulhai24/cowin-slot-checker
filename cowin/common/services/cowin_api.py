import requests


class CowinApi:

    def __init__(self):
        self.URL_BASE = "https://cdn-api.co-vin.in"

    def check_slots_by_district_and_date(self, district_id, date):
        resp = requests.get(
            self.URL_BASE + "/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(
                district_id, date))
        if resp.status_code != 200:
            return None
        return resp.json()


cowin_api = CowinApi()
