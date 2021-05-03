import requests
import os

class VerloopWhatsappApi:

    def __init__(self):
        self.URL = "https://feedmyblr.verloop.io/api/v1/Campaign/SendMessage"
        self.otp_campaign_id = os.getenv('OTP_CAMPAIGN_ID')
        self.slots_campaign_id = os.getenv('SLOTS_CAMPAIGN_ID')

    def send_otp(self, phone_number, variables):
        body = {
            "CampaignID": self.otp_campaign_id,
            "To": {
                "PhoneNumber": phone_number
            },
            "Parameters": {
                "name": variables["name"],
                "number": variables["number"]
            }
        }
        headers = {"Content-Type": "application/json"}
        return self._send_msg(headers=headers, body=body)


    def send_slot_availability(self, phone_number, variables):
        body = {
           "CampaignID": self.slots_campaign_id,
           "To": {
               "PhoneNumber": phone_number
           },
           "Parameters": {
              "name": variables["name"],
              "slots": variables["slots"],
              "hospital_name": variables["hospital_name"],
              "district_name": variables["district_name"],
              "website_name" : variables["website_name"],
           }
        }
        headers = {"Content-Type": "application/json"}
        return self._send_msg(headers=headers, body=body)

    def _send_msg(self, headers, body):
        resp = requests.post(self.URL, data=body, headers=header)
        if resp.status_code != 200:
            return None
        return resp.json()

verloop_whatsapp_api = VerloopWhatsappApi()
