from machine import SPI
from mfrc522 import MFRC522


class RFID:
    def __init__(self, spi: SPI, rst_pin: int, sda_pin: int):
        self.rfid = MFRC522(spi, rst_pin, sda_pin)

    def read(self) -> str:
        uid = ""
        (stat, tag_type) = self.rfid.request(self.rfid.REQIDL)
        if stat == self.rfid.OK:
            (stat, raw_uid) = self.rfid.anticoll()
            if stat == self.rfid.OK:
                uid = "0x%02x%02x%02x%02x" % (
                    raw_uid[0],
                    raw_uid[1],
                    raw_uid[2],
                    raw_uid[3],
                )
                return uid
