import math
import random

digits = "0123456789"


def generate_otp():
    otp = ""
    for i in range(4):
        otp += digits[math.floor(random.random() * 10)]
    return otp
