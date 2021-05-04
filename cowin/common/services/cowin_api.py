import requests
import logging

logger = logging.getLogger(__name__)


class CowinApi:

    def __init__(self):
        self.URL_BASE = "https://cdn-api.co-vin.in"

    def check_slots_by_district_and_date(self, district_id, date):
        url = self.URL_BASE + "/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district_id, date)
        logger.info(url)
        resp = requests.get(url)
        if resp.status_code != 200:
            logger.exception("Cowin API failed, {}, {}".format(resp.url, resp.status_code))
            return None
        else:
            logger.info("Cowin API success, {}, {}".format(resp.url, resp.status_code))
        return resp.json()


cowin_api = CowinApi()
