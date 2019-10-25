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
P1_SCORE = 0
P2_SCORE = 0
P1_GAMES = 0
P2_GAMES = 0
WIN = False

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


def renderDisplay(win=False):

    # Initialise display
    lcd.lcd_init()

    now = datetime.now()

    # dd/mm/YY H:M:S
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Send some more text
    lcd.lcd_string(f"{date_time}", lcd.LCD_LINE_1)
    if not win:
        lcd.lcd_string(f"Player 1: {P1_SCORE}", lcd.LCD_LINE_2)
        lcd.lcd_string(f"Player 2: {P2_SCORE}", lcd.LCD_LINE_3)
        lcd.lcd_string(f"{P1_GAMES} - {P2_GAMES}", lcd.LCD_LINE_4)
    else:
        player = "Player 1" if P1_SCORE > P2_SCORE else "Player 2" 
        lcd.lcd_string(f"WINNER! {player}", lcd.LCD_LINE_2)

def checkWin(player):
    abs_diff = abs(P1_SCORE - P2_SCORE)
    print(abs_diff)
    if player == 1:
        return abs_diff >= 2 and P1_SCORE >= 21
    else:
        return abs_diff >= 2 and P2_SCORE >= 21

def reset():
    P1_SCORE = 0
    P2_SCORE = 0
    P1_GAMES = 0
    P2_GAMES = 0
    WIN = False 

renderDisplay()
try:
    while True:
        if GPIO.event_detected(PIN_BUTTON_A):
            if WIN:
                reset()
            else:
                print(f"\n Button pressed {PIN_BUTTON_A}")
                P1_SCORE += 1
                WIN = checkWin(1)
                GPIO.output(PIN_LED_A, GPIO.HIGH)
                GPIO.output(PIN_LED_A, GPIO.LOW)
            renderDisplay(WIN)
        if GPIO.event_detected(PIN_BUTTON_B):
            if WIN:
                reset()
            else:
                print(f"\n Button pressed {PIN_BUTTON_B}")
                P2_SCORE += 1
                WIN = checkWin(2)
                GPIO.output(PIN_LED_B, GPIO.HIGH)
                GPIO.output(PIN_LED_B, GPIO.LOW)
            renderDisplay(WIN)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()
print("Stopping Table Tennis Switch")
