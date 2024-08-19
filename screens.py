from conf import CHECKBOX_X, CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, CHECKBOX_RGB, MENU_ITEM_MARGIN_TOP, SELECTOR_DIMENSIONS,SELECTOR_RGB,BACKGROUND_RGB
from credentials import SERVER_IP, SERVER_PORT
from socket import socket, getaddrinfo
from utils import url_encode
from sysfont import sysfont
from time import sleep
from pushbutton import pb_accept,pb_up,pb_down
from screen import SCREEN
from rfid import RFID

def send_and_wait_from_server(display:SCREEN, meals:dict, font_height:int=8) -> dict:
    encoded_data = url_encode(str(meals)).encode()
    addr_info = getaddrinfo(SERVER_IP, SERVER_PORT)

    addr = addr_info[-1][-1]
    print("Connect address:", addr)

    while True:
        soc = socket()
        soc.connect(addr)
        soc.send(b"GET /pay?meals=" + encoded_data + b" HTTP/1.0\r\n\r\n")
        res = soc.recv(4096).decode()
        if len(res) > 200:
            start_index = res.find("{")
            stop_index = res.find("}", start_index) + 1
            print("RES:", res)
            data = dict(eval(res[start_index:stop_index]))

            status = data.get("status")
            message = data.get("message")

            y = 40 + font_height + MENU_ITEM_MARGIN_TOP
            if status != "error":
                student_name = data.get("student_name")
                display.text((20, y), student_name, (0,0,255), font_size=1)
                y += font_height + MENU_ITEM_MARGIN_TOP
                if status == "success":
                    display.text((5, y), message, (0,255,0), font_size=1)
                else:
                    display.text((0, y), message, (250,255,160), font_size=1)
            else:
                display.text((10, y), message, (255,0,0), font_size=1)

            # OK Button
            while True:
                display.text((100, 100), "OK", (0, 0, 255), font_size=1)
                display.checker(95, 100+CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, (255, 255, 0))

                if not pb_accept.value():
                    return
        soc.close()
        sleep(1)


def show_card_scan_screen(display:SCREEN, rfid:RFID, meals: dict, font_height:int=8):
    prev_uid = ""
    # FIXME
    y_offset = font_height + MENU_ITEM_MARGIN_TOP
    display.fill()
    display.text((20, 10), "Scan Your Card", (0, 255, 0), font_size=1)

    while True:
        uid = rfid.read()
        if uid is not None and prev_uid != uid:
            prev_uid = uid
            print("UID", uid)
            # meals.update({"uid": uid})
            # print("Sending:\n", meals)
            y = 10 + font_height + MENU_ITEM_MARGIN_TOP
            display.text((25, y), "Querying ...", (0, 255, 0), font_size=1)
            send_and_wait_from_server(display, meals)
            return



def open_confirmation_screen(display:SCREEN, rfid:RFID, meals: dict, font_height:int=8):
    y_offset = font_height + MENU_ITEM_MARGIN_TOP
    display.fill()
    display.text((20, 0), "Selected Meals", (25, 245, 89), font_size=1)

    count = 1
    print(meals)
    total_price = 0
    for meal_id, meal_details in meals.items():
        display.text((10, y_offset),
                     f"{count}. {"%-13s" % meal_details.get("name")} {meal_details.get("price")}", (25, 245, 89), font_size=1)
        print(meal_details)
        y_offset += font_height + MENU_ITEM_MARGIN_TOP
        total_price += meal_details.get("price")
        count += 1

    display.text((10, y_offset + 16),
                 f"{"%-6s" % "Total"} {total_price}", (25, 245, 89), font_size=2)

    y_offset = y_offset + 16 + (font_height * 2) + MENU_ITEM_MARGIN_TOP + 30
    x = 15

    display.text((x, y_offset), "Cancel", (255, 0, 0), font_size=1)
    x += 55
    display.text((x, y_offset), "Proceed", (0, 0, 255), font_size=1)

    x -= 5
    display.checker(x, y_offset+CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, (255, 255, 0))

    selection = True
    sleep(.5)
    while True:
        if not pb_up.value() and selection:
            display.checker(x, y_offset+CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, BACKGROUND_RGB)
            x = 10
            display.checker(x, y_offset+CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, (255, 255, 0))
            selection = False

        if not pb_down.value() and not selection:
            display.checker(x, y_offset+CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, BACKGROUND_RGB)
            x = 65
            display.checker(x, y_offset+CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, (255, 255, 0))
            selection = True

        if not selection and not pb_accept.value():
            return

        if selection and not pb_accept.value():
            print("Should go to another screen to request for payment approval")
            show_card_scan_screen(display, rfid, meals)
            # function
            return

def populate_menu(display: SCREEN, lst_menu:list, selected_meals:dict, pointed_item:int, y_offset:int, font_height:int=8) -> int:
    """Display the menu items on the screen"""
    for i in range(len(lst_menu)):
        display.text((10, y_offset),
                     f"{i+1}. {"%-13s" % lst_menu[i][0]} {lst_menu[i][1]}", (25, 245, 89), font_size=1)
        print(type(selected_meals), selected_meals)
        if i+1 in selected_meals.keys():
            display.checker(CHECKBOX_X, y_offset +
                            CHECKBOX_Y_OFFSET, CHECKBOX_RADIUS, CHECKBOX_RGB)
        y_offset += sysfont.get("Height") + MENU_ITEM_MARGIN_TOP
    display.selector(0, font_height, pointed_item, 4,
                     SELECTOR_DIMENSIONS, SELECTOR_RGB)
    return y_offset

