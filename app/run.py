import RPi.GPIO as GPIO
import time
import os
from datetime import datetime

# our libs
from src import lcd

print("Starting Table Tennis Switch")

# constants
PIN_BUTTON_A = 36
PIN_BUTTON_B = 37
PIN_LED_A = 32
PIN_LED_B = 33

# Numbers pins by physical location
GPIO.setmode(GPIO.BOARD)

# setup output
GPIO.setup(PIN_LED_A, GPIO.OUT)
GPIO.setup(PIN_LED_B, GPIO.OUT)
# GPIO PIN_BUTTON set up as input.
GPIO.setup(PIN_BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print(f"Waiting for falling edge on port {PIN_BUTTON_A} or {PIN_BUTTON_B}")
# now the program will do nothing until the signal on the pin
# starts to fall towards zero. This is why we used the pull-up
# to keep the signal high and prevent a false interrupt
# During this waiting time, your computer is not
# wasting resources by polling for a button press

GPIO.add_event_detect(PIN_BUTTON_A, GPIO.RISING)
GPIO.add_event_detect(PIN_BUTTON_B, GPIO.RISING)


def renderDisplay():

    # Initialise display
    lcd.lcd_init()

    now = datetime.now()

    # dd/mm/YY H:M:S
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Send some more text
    lcd.lcd_string("Line 1:", lcd.LCD_LINE_1)
    lcd.lcd_string("Line2", lcd.LCD_LINE_2)
    lcd.lcd_string(f"{date_time}", lcd.LCD_LINE_3)
    lcd.lcd_string("Line 3", lcd.LCD_LINE_4)


try:
    while True:
        if GPIO.event_detected(PIN_BUTTON_A):
            print(f"\n Button pressed {PIN_BUTTON_A}")
            GPIO.output(PIN_LED_A, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_LED_A, GPIO.LOW)
        if GPIO.event_detected(PIN_BUTTON_B):
            print(f"\n Button pressed {PIN_BUTTON_B}")
            GPIO.output(PIN_LED_B, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(PIN_LED_B, GPIO.LOW)
            renderDisplay()
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()
print("Stopping Table Tennis Switch")