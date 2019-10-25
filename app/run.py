import time
import os

print("Starting Table Tennis Switch")

# constants
PIN_BUTTON_A = 36
PIN_BUTTON_B = 37
PIN_LED_A = 32
PIN_LED_B = 33

# Numbers pins by physical location
GPIO.setmode(GPIO.BOARD)

# GPIO PIN_BUTTON set up as input.
GPIO.setup(PIN_BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print(f"Waiting for falling edge on port {PIN_BUTTON_A} or {PIN_BUTTON_B}")
# now the program will do nothing until the signal on the pin
# starts to fall towards zero. This is why we used the pull-up
# to keep the signal high and prevent a false interrupt
# During this waiting time, your computer is not
# wasting resources by polling for a button press

try:
    while True:
        # poll
        if GPIO.input(PIN_BUTTON_A):
            print(f"\n Button pressed {PIN_BUTTON_A}")
        # if GPIO.input(PIN_BUTTON_B):
        #     print(f"\n Button pressed {PIN_BUTTON_B}")
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()
print("Stopping Table Tennis Switch")
