from connectFour import connectFour 
import threading


def getMinMaxMove(cf, player):
  wins = [0] * len(cf.field)
  print(wins)
  for x in range(len(cf.field)):
    pass



cf = connectFour()

def game_thread():
    cf.start()

gameThread = threading.Thread(target=game_thread, args=(), daemon=True)
gameThread.start()

move = getMinMaxMove(cf, 2)
win = cf.chooseRow(move)