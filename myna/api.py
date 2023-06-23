from myna.reader import select_text_AP

def get_attr_info(cardservice, pin: str):
	text_ap = select_text_AP(cardservice)
	text_ap.verify_pin(pin)
	return text_ap.read_attributes()