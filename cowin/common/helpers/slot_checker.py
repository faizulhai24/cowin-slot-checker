import datetime
import os
import platform
import time


import requests

class SlotChecker:
    def __init__(self):
        self.DISTRICT_IDS = [(294, "BBMP"), (265, "Bengaluru Urban")]
        self.NUM_WEEKS = 5
        self.DATES = []
        self.URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
        self.WRITE_TO_FILE = True
        self.ALARM = True
        self.FILE_NAME = "vaccine.txt"
        self.MIN_AGE = 18
        self.MIN_CAPACITY = 5

        now = datetime.datetime.now()
        for i in range(5):
            target_time = now + datetime.timedelta(days=7 * i)
            self.DATES.append(target_time.strftime("%d-%m-%Y"))

    def check_free_slots(self, data):
        free_slots = []
        centers = data['centers']
        for center in centers:
            for session in center['sessions']:
                if session['min_age_limit'] == self.MIN_AGE and session['available_capacity'] > self.MIN_CAPACITY:
                    free_slots.append(
                        "{} - {} - {} - {} - {}".format(center['name'], center['district_name'], session['date'],
                                                        center['fee_type'], session['vaccine']))
        return free_slots

    def write_to_file(self, slots):
        print(slots)
        f = open(self.FILE_NAME, "a")
        data = '\n'.join(slots)
        f.write(data)
        f.write('\n')
        f.close()

    def run(self):
        slots = []
        for district_id in self.DISTRICT_IDS:
            for date in self.DATES:
                resp = requests.get(self.URL.format(district_id[0], date))
                if resp.status_code != 200:
                    print(resp.status_code)
                    # print("Failed to fetch slots on {} for {}".format(date, district_id[1]))
                    continue
                free_slots = self.check_free_slots(resp.json())
                if free_slots:
                    slots.extend(free_slots)
                else:
                    print("No free slots found on {} for {}".format(date, district_id[1]))