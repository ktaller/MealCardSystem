from ST7735 import TFT, TFTColor
from sysfont import sysfont


class SCREEN:
    def __init__(
        self, spi: SPI, ao_pin: int, rst_pin: int, cs_pin: int, use_rgb: bool = True
    ):
        self.display = TFT(spi, ao_pin, rst_pin, cs_pin)
        self.display.initr()
        self.display.rgb(use_rgb)

    def fill(self, rgb: tuple = (0, 0, 0)):
        if len(rgb) != 3:
            raise ValueError("RGB should have a tuple of 3 colors, (r, g, b)")
        self.display.fill(TFTColor(rgb[0], rgb[1], rgb[2]))

    def fill_rect(self, position: tuple = (0, 0), size: tuple = (50, 20), color: tuple = (255, 255, 255)):
        if (len(color) < 3):
            raise ValueError(
                "You must provide a color with 3 values, (r, g, b)")
        self.display.fillrect(position, size, TFTColor(color[0], color[1], color[2]))

    def rectangle(self):
        pass

    def text(
        self,
        pos: tuple,
        text: str,
        text_color: tuple,
        font=sysfont,
        font_size: int = 2,
        wrap: bool = True,
    ):
        if len(pos) != 2:
            raise ValueError("")
        if len(text_color) != 3:
            raise ValueError("RGB should have a tuple of 3 colors, (r, g, b)")
        self.display.text(
            (pos[0], pos[1]),
            text,
            TFTColor(text_color[0], text_color[1], text_color[2]),
            font,
            font_size,
            wrap,
        )

    def checker(self, x: int, y_offset: int, radius: int, rgb: tuple):
        if len(rgb) != 3:
            raise ValueError("RGB should have a tuple of 3 colors, (r, g, b)")
        self.display.circle((x, y_offset), radius,
                            TFTColor(rgb[0], rgb[1], rgb[2]))

    def selector(
        self,
        x: int,
        font_height: int,
        multiplier_constant: int,
        offset: int,
        dimensions: tuple,
        rgb: tuple,
    ):
        if len(rgb) != 3:
            raise ValueError("RGB should have a tuple of 3 colors, (r, g, b)")
        self.display.rect(
            (x, (font_height * multiplier_constant) - offset),
            (dimensions[0], dimensions[1]),
            TFTColor(rgb[0], rgb[1], rgb[2]),
        )
