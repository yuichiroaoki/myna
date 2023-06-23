from myna.api import get_attr_info
from myna.reader import TextAttrs
from myna.validate import validate_4_digit_pin
import json

def show_attributes(cardservice, pin: str):
    if pin == "":
        pin = input("Enter PIN: ")
    
    if not validate_4_digit_pin(pin):
        raise ValueError("PIN must be 4 digits")
    
    attr = get_attr_info(cardservice, pin)
    output_text_attrs(attr, "text")

def output_text_attrs(attr: TextAttrs, form: str):
    if form == "json":
        obj = {
            "name": attr.name,
            "address": attr.address,
            "birth": attr.birth,    
            "sex": attr.sex,
        }
        print(json.dumps(obj))
    else:
        print("Name:    ", attr.name)
        print("Address: ", attr.address)
        print("Birth:   ", attr.birth)
        print("Sex:     ", attr.sex)
