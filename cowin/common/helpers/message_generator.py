# [{
#     'center_name': center['name'],
#     'district_name': center['district_name'],
#     'date': session['date'],
#     'fee_type': center['fee_type'],
#     'vaccine': session['vaccine'],
#     'available_capacity': session['available_capacity']
# }
#  =============>
# {
#     "slots": variables["slots"],
#       "hospital_name": variables["hospital_name"],
#       "district_name": variables["district_name"],
#       "website_name": variables["website_name"],
#    }

def get_message_params(slots):
    if not slots:
        return None

    params = {
        'slots': 0,
        'hospital_name': '',
        'district_name': slots[0]['district_name'],
        'website_name': 'https://selfregistration.cowin.gov.in/',
    }

    hospital_string = ''
    for count, slot in enumerate(slots):
        params['slots'] += slot['available_capacity']
        if count < 10:
            hospital_string += "{} ({}),".format(slot['center_name'], slot['date'])

    if len(slots) >= 10:
        hospital_string += "+{} more combinations of hospitals and dates".format(len(slots) - 10)

    params['hospital_name'] = hospital_string
    return params
