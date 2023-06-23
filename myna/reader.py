from smartcard.util import toBytes
from myna.apdu import new_APDU_case2, new_APDU_case3
from myna.utils import ASN1PartialParser
import asn1

class TextAP:
	def __init__(self, cardservice):
		self.cardservice = cardservice

	def verify_pin(self, pin: str):
		select_EF(self.cardservice, "0011")
		verify(self.cardservice, pin)
		print("PIN verified")

	def read_attributes(self):
		select_EF(self.cardservice, "0002")
		data = read_binary(self.cardservice, 7)
		if len(data) != 7:
			raise ValueError("Error at read_binary()")
		
		parser = ASN1PartialParser(0, 0)
		parser.parse(data)
		data = read_binary(self.cardservice, parser.get_size())
		return TextAttrs(data)


class TextAttrs:
	def __init__(self, data):
		decoder = asn1.Decoder()
		decoder.start(bytes(data))
		tag = decoder.peek()
		assert tag == (0x20, asn1.Types.Constructed, asn1.Classes.Private)
		decoder.enter()
		tag, value = decoder.read()
		self.header = value

		tag, value = decoder.read()
		self.name = value.decode("utf-8")

		tag, value = decoder.read()
		self.address = value.decode("utf-8")

		tag, value = decoder.read()
		self.birth = int(value)

		tag, value = decoder.read()
		self.sex = int(value)

def select_text_AP(cardservice)->TextAP:
	select_DF(cardservice, "D3921000310001010408")
	return TextAP(cardservice)

def select_DF(cardservice, id: str):
	bid = toBytes(id)
	apdu = new_APDU_case3(0x00, 0xA4, 0x04, 0x0C, bid)
	response, sw1, sw2 = cardservice.connection.transmit(apdu)

	if sw1 == 0x90 and sw2 == 0x00:
		return

	raise ValueError("Error selecting DF")

def select_EF(cardservice, id: str):
	bid = toBytes(id)
	apdu = new_APDU_case3(0x00, 0xA4, 0x02, 0x0C, bid)
	response, sw1, sw2 = cardservice.connection.transmit(apdu)

	if sw1 == 0x90 and sw2 == 0x00:
		return

	raise ValueError("Error selecting EF")

	
def verify(cardservice, pin: str):
	if pin == "":
		raise ValueError("Empty PIN")

	bpin = bytearray()
	bpin.extend(map(ord, pin))
	bpin = list(bpin)

	apdu = new_APDU_case3(0x00, 0x20, 0x00, 0x80, bpin)
	response, sw1, sw2 = cardservice.connection.transmit(apdu)

	if sw1 == 0x90 and sw2 == 0x00:
		return
	elif sw1 == 0x63:
		counter = int(sw2 & 0x0F)
		if counter == 0:
			raise ValueError("Wrong PIN, PIN blocked")
		raise ValueError("Wrong PIN, " + str(counter) + " tries left")
	elif sw1 == 0x69 and sw2 == 0x84:
		raise ValueError("PIN already blocked")
	else:
		raise ValueError("Wrong PIN, " + str(sw1) + " " + str(sw2))

def read_binary(cardservice, size: int):
	length: int
	pos: int = 0
	res: list[int] = []

	while pos < size:
		if size-pos > 0xFF:
			length = 0
		else:
			length = size - pos
		
		apdu = new_APDU_case2(0x00, 0xB0, (pos >> 8) & 0xFF, pos & 0xFF, length)
		response, sw1, sw2 = cardservice.connection.transmit(apdu)
		if sw1 != 0x90 or sw2 != 0x00:
			return
		res += response
		pos += len(response)
	
	return res