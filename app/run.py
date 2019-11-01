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

PIN_RESET_BUTTON = 13

# Numbers pins by physical location
GPIO.setmode(GPIO.BOARD)

# GPIO PIN_BUTTON set up as input.
GPIO.setup(PIN_BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print(f"Waiting for falling edge on port {PIN_BUTTON_A} or {PIN_BUTTON_B}")
# now the program will do nothing until the signal on the pin
# starts to fall towards zero. This is why we used the pull-up
# to keep the signal high and prevent a false interrupt
# During this waiting time, your computer is not
# wasting resources by polling for a button press

GPIO.add_event_detect(PIN_BUTTON_A, GPIO.RISING, bouncetime=500)
GPIO.add_event_detect(PIN_BUTTON_B, GPIO.RISING, bouncetime=500)
GPIO.add_event_detect(PIN_RESET_BUTTON, GPIO.RISING, bouncetime=500)


class GameState:
    p1 = "Player 1"
    p2 = "Player 2"
    score = [0, 0]
    games = [0, 0]
    win = False

    def resetGame(self):
        self.games = [0, 0]
        self.resetScores()

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
    if not state.win:
        lcd.lcd_string(f"{state.p1}: {state.score[0]}", lcd.LCD_LINE_2)
        lcd.lcd_string(f"{state.p2}: {state.score[1]}", lcd.LCD_LINE_3)
        lcd.lcd_string(f"{state.games[0]} - {state.games[1]}", lcd.LCD_LINE_4)
    else:
        player = state.p1 if state.score[0] > state.score[1] else state.p2
        lcd.lcd_string(f"WINNER! {player}", lcd.LCD_LINE_2)


def handleButton(player, state):
    playerId = 0 if player == state.p1 else 1
    if state.win:
        state.games[playerId] += 1
        state.resetScores()
    else:
        state.score[playerId] += 1
        state.checkWin(player)
    renderDisplay(state)


state = GameState()
renderDisplay(state)
try:
    while True:
        if GPIO.event_detected(PIN_BUTTON_A):
            handleButton(state.p1, state)
        if GPIO.event_detected(PIN_BUTTON_B):
            handleButton(state.p2, state)
        if GPIO.event_detected(PIN_RESET_BUTTON):
            print(f"\n Button pressed {PIN_RESET_BUTTON}")
            state.resetGame()
            renderDisplay(state)
except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit

GPIO.cleanup()
print("Stopping Table Tennis Switch")
