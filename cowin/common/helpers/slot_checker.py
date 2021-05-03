from cowin.common.services.cowin_api import cowin_api


class SlotChecker:

    def __init__(self):
        self.min_age = 18
        self.min_capacity = 1

    def check_free_slots(self, data):
        free_slots = []
        centers = data['centers']
        for center in centers:
            for session in center['sessions']:
                if session['min_age_limit'] == self.min_age and session['available_capacity'] > self.min_capacity:
                    free_slots.append({
                        'center_name': center['name'],
                        'district_name': center['district_name'],
                        'date': session['date'],
                        'fee_type': center['fee_type'],
                        'vaccine': session['vaccine'],
                        'available_capacity': session['available_capacity']
                    })
        return free_slots

    def check(self, district_id, date):
        data = cowin_api.check_slots_by_district_and_date(district_id, date)
        if not data:
            return []
        free_slots = self.check_free_slots(data)
        return free_slots
