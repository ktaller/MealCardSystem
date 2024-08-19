from machine import Pin
from conf import PB_ACCEPT, PB_UP, PB_CHECK_CANCEL, PB_DOWN

pb_accept = Pin(PB_ACCEPT, Pin.IN, Pin.PULL_UP)
pb_up = Pin(PB_UP, Pin.IN, Pin.PULL_UP)
pb_check_cancel = Pin(PB_CHECK_CANCEL, Pin.IN, Pin.PULL_UP)
pb_down = Pin(PB_DOWN, Pin.IN, Pin.PULL_UP)