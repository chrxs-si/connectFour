from connectFour import connectFour 
import threading


def getMinMaxMove(cf, player):
  wins = [0] * len(cf.field)
  print(wins)
  for x in range(len(cf.field)):
    games = []




cf = connectFour()

def game_thread():
    cf.start()

gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
gameThread.start()

move = getMinMaxMove(cf, 2)
win = cf.chooseRow(move)

[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5]