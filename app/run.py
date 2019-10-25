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

P1 = "Player 1"
P2 = "Player 2"
SCORE = [0, 0]
GAMES = [0, 0]

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

class GameState:
    p1 = "Player 1"
    p2 = "Player 2"
    score = [0, 0]
    games = [0,0]
    win = False

    def resetScores(self):
        self.score = [0, 0]
        self.win = False
    
    def checkWin(self, player):
        abs_diff = abs(self.score[0] - self.score[1])
        score = self.score[0] if player == self.p1 else self.score[1]
        self.win = abs_diff >= 2 and score >= 21
        return self.win


def renderDisplay(state):

    # Initialise display
    lcd.lcd_init()

    now = datetime.now()

    # dd/mm/YY H:M:S
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Send some more text
    lcd.lcd_string(f"{date_time}", lcd.LCD_LINE_1)
    if not win:
        lcd.lcd_string(f"{state.p1}: {state.score[0]}", lcd.LCD_LINE_2)
        lcd.lcd_string(f"{state.p2}: {state.score[1]}", lcd.LCD_LINE_3)
        lcd.lcd_string(f"{state.games[0]} - {state.games[1]}", lcd.LCD_LINE_4)
    else:
        player = state.p1 if state.score[0] > state.score[1] else P2 
        lcd.lcd_string(f"WINNER! {player}", lcd.LCD_LINE_2)

def checkWin(player, state):
    abs_diff = abs(state.score[0] - state.score[1])
    score = state.score[0] if player == P1 else state.score[1]
    return abs_diff >= 2 and score >= 21

def handleButton(player, state):
    playerId = 0 if player == P1 else 1
    if state.win:
        state.games[playerId] += 1
        state.reset()
    else:
        print(f"\n Button pressed {PIN_BUTTON_A}")
        state.score[playerId] += 1
        state.checkWin(player)
    renderDisplay(state.win)

# def renderDisplay(win=False):

#     # Initialise display
#     lcd.lcd_init()

#     now = datetime.now()

#     # dd/mm/YY H:M:S
#     date_time = now.strftime("%d/%m/%Y %H:%M:%S")

#     # Send some more text
#     lcd.lcd_string(f"{date_time}", lcd.LCD_LINE_1)
#     if not win:
#         lcd.lcd_string(f"{P1}: {SCORE[0]}", lcd.LCD_LINE_2)
#         lcd.lcd_string(f"{P2}: {SCORE[1]}", lcd.LCD_LINE_3)
#         lcd.lcd_string(f"{GAMES[0]} - {GAMES[1]}", lcd.LCD_LINE_4)
#     else:
#         player = P1 if SCORE[0] > SCORE[1] else P2 
#         lcd.lcd_string(f"WINNER! {player}", lcd.LCD_LINE_2)

# def checkWin(player):
#     abs_diff = abs(SCORE[0] - SCORE[1])
#     score = SCORE[0] if player == P1 else SCORE[1]
#     return abs_diff >= 2 and score >= 21

# def reset():
#     global P1_SCORE
#     P1_SCORE = 0
#     global P2_SCORE
#     P2_SCORE = 0
#     global WIN
#     WIN = False
#     global SCORE
#     SCORE = [0, 0] 

# def handleButton(player, win):
#     playerId = 0 if player == P1 else 1
#     if win:
#         GAMES[playerId] += 1
#         reset()
#     else:
#         print(f"\n Button pressed {PIN_BUTTON_A}")
#         SCORE[playerId] += 1
#         win = checkWin(player)
#     renderDisplay(win)
    # return win

state = GameState()
renderDisplay()
try:
    while True:
        if GPIO.event_detected(PIN_BUTTON_A):
            WhandleButton(state.p1, state)
            time.sleep(1)
        if GPIO.event_detected(PIN_BUTTON_B):
            handleButton(state.p2, state)
            time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()
print("Stopping Table Tennis Switch")
