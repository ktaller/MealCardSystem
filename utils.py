from machine import SoftSPI, Pin
from conf import SPI_BAUDRATE, SPI_MOSI_PIN, SPI_MISO_PIN, SPI_SCK_PIN

spi = SoftSPI(
    baudrate=SPI_BAUDRATE,
    polarity=0,
    phase=0,
    sck=Pin(SPI_SCK_PIN, Pin.OUT),
    mosi=Pin(SPI_MOSI_PIN, Pin.OUT),
    miso=Pin(SPI_MISO_PIN, Pin.OUT),
)

def url_encode(s)->str:
    # Define characters that need to be encoded
    specials = [
        " ",
        '"',
        "#",
        "%",
        "&",
        "+",
        ",",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "`",
        "{",
        "|",
        "}",
        "~",
    ]
    encoded = ""
    for char in s:
        if char in specials:
            encoded += "%" + hex(ord(char))[2:]
        else:
            encoded += char
    return encoded
