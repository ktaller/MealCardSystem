from machine import reset
from time import time
from conf import (
    RFID_RST_PIN,
    RFID_SDA_PIN,
    DISP_AO_PIN,
    DISP_RST_PIN,
    DISP_CS_PIN,
    SELECTOR_DIMENSIONS,
    BACKGROUND_RGB,
    SELECTOR_RGB,
    CHECKBOX_RGB,
    CHECKBOX_X,
    CHECKBOX_RADIUS,
    CHECKBOX_Y_OFFSET,
    MENU_ITEM_MARGIN_TOP,
)
from utils import spi
from rfid import RFID
from screen import SCREEN, sysfont
from screens import (
    populate_menu,
    open_confirmation_screen,
    populate_menu,
)
from pushbutton import *
from networking import Network, Client, WIFI_SSID, WIFI_PASSWORD
from credentials import SERVER_IP, SERVER_PORT
from socket import socket, getaddrinfo

rfid = RFID(spi, RFID_RST_PIN, RFID_SDA_PIN)
display = SCREEN(spi, DISP_AO_PIN, DISP_RST_PIN, DISP_CS_PIN)
network = Network(WIFI_SSID, WIFI_PASSWORD)

network.connect_station()
# client = Client(SERVER_IP, SERVER_PORT)


display.fill((0, 0, 0))
display.text((52, 0), "Menu", (25, 245, 89), font_size=1)

# display.circle((5, sysfont.get("Height")+5), 3, (255, 5, 89))

# fetched from the database
menu_items = {"Ugali": 20, "Sukuma Wiki": 10, "Beans": 20, "Rice": 30, "Beef": 60}
selected_meals = dict()
lst_menu = list(menu_items.items())

pointed_item = 1

y_offset = font_height = sysfont.get("Height") + 5

prev_uid = ""


y_offset = populate_menu(display, lst_menu, selected_meals, pointed_item, y_offset)

prev_time = time()
should_clear = False  # variable to monitor if the screen should be cleared

try:
    while True:
        rfid.read()
        if not pb_up.value() and pointed_item > 1:
            display.selector(
                0, font_height, pointed_item, 4, SELECTOR_DIMENSIONS, BACKGROUND_RGB
            )
            pointed_item -= 1
            display.selector(
                0, font_height, pointed_item, 4, SELECTOR_DIMENSIONS, SELECTOR_RGB
            )

        if not pb_down.value() and pointed_item < len(lst_menu):
            display.selector(
                0, font_height, pointed_item, 4, SELECTOR_DIMENSIONS, BACKGROUND_RGB
            )
            pointed_item += 1
            display.selector(
                0, font_height, pointed_item, 4, SELECTOR_DIMENSIONS, SELECTOR_RGB
            )

        if not pb_check_cancel.value():
            if pointed_item in selected_meals.keys():
                # remove the meal from the dictionary
                del selected_meals[pointed_item]
                display.checker(
                    CHECKBOX_X,
                    (pointed_item * (sysfont.get("Height") + MENU_ITEM_MARGIN_TOP))
                    + CHECKBOX_Y_OFFSET,
                    CHECKBOX_RADIUS,
                    BACKGROUND_RGB,
                )
                display.selector(
                    0, font_height, pointed_item, 4, SELECTOR_DIMENSIONS, SELECTOR_RGB
                )
            else:
                # add the meal to the list
                selected_meals[pointed_item] = {
                    "name": lst_menu[pointed_item - 1][0],
                    "price": lst_menu[pointed_item - 1][1],
                }
                display.checker(
                    CHECKBOX_X,
                    (pointed_item * (sysfont.get("Height") + MENU_ITEM_MARGIN_TOP))
                    + CHECKBOX_Y_OFFSET,
                    CHECKBOX_RADIUS,
                    CHECKBOX_RGB,
                )
                display.selector(
                    0, font_height, pointed_item, 4, SELECTOR_DIMENSIONS, SELECTOR_RGB
                )
            print(selected_meals)

        print(should_clear, ":", prev_time, ":", time(), ":", (time() - prev_time >= 2))
        if should_clear and (time() - prev_time >= 2):
            display.text((5, 150), "                     ", (255, 0, 0), font_size=1)
            should_clear = False
            print("Cleared")

        if not pb_accept.value():
            if len(selected_meals) == 0:
                display.text((5, 150), "Please select a meal", (255, 0, 0), font_size=1)
                prev_time = time()
                should_clear = True
                # break
            else:
                total = 0
                for id, meal_details in selected_meals.items():
                    total += meal_details.get("price")
                print("Total: ", total)

                # TODO:move this to the second screen
                open_confirmation_screen(display, rfid, selected_meals)
                # client.pay_meal(selected_meals, total, prev_uid)
                selected_meals = dict()
                display.fill((0, 0, 0))
                display.text((52, 0), "Menu", (25, 245, 89), font_size=1)
                y_offset = font_height = sysfont.get("Height") + 5

                y_offset = populate_menu(
                    display, lst_menu, selected_meals, pointed_item, y_offset
                )

except KeyboardInterrupt as e:
    print("Keyboard Interrupt!")
    # This is necessary because the SPI need to reset if you don't intend to reset the board manually
    reset()
