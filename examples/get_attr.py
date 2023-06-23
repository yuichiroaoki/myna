from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardRequest import CardRequest
from smartcard.CardType import ATRCardType
import sys
from myna.text import show_attributes

for reader in readers():
    try:
        connection = reader.createConnection()
        connection.connect()
        atr = connection.getATR()
        print("reader: ", reader)
        print("ATR: ", toHexString(connection.getATR()))
        cardtype = ATRCardType( atr )

        cardrequest = CardRequest( timeout=1, cardType=cardtype )

        cardservice = cardrequest.waitforcard()
        print("card detected")
        cardservice.connection.connect()

        show_attributes(cardservice, "")


    except NoCardException:
        print(reader, 'no card inserted')

if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)

