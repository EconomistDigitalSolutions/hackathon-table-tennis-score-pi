class GameState:

    def __init__(self, p1="Player 1", p2="Player 2"):
        self.p1 = p1
        self.p2 = p2
        self.resetGame()

    def resetGame(self):
        self.__games = [0, 0]
        self.resetScores()

    def resetScores(self):
        self.__score = [0, 0]
        self.gameOver = False

    def scorePoint(self, player):
        self.__score[self.__getPlayerId(player)] += 1
        if self.hasWon(player):
            self.__scoreGame(player)

    def hasWon(self, player):
        abs_diff = abs(self.__score[0] - self.__score[1])
        __score = self.__score[self.__getPlayerId(player)]
        return abs_diff >= 2 and __score >= 21

    def printScore(self, player):
        return f"{player}: {self.__score[self.__getPlayerId(player)]}"

    def printGames(self):
        return f"{self.__games[0]} - {self.__games[1]}"

    def __scoreGame(self, player):
        self.__games[self.__getPlayerId(player)] += 1
        self.gameOver = True

    def __getPlayerId(self, player):
        return 0 if player == self.p1 else 1
