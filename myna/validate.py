import re

def validate_4_digit_pin(pin: str):
    # validate with regex
    if re.match(r"^[0-9]{4}$", pin):
        return True
    else:
        return False