from random import randint

def getRandomMove(cf):
  rows = list(range(0, cf.fieldwidth))
  for row in range(len(cf.field)):
    if cf.field[row][0] != 0: rows.remove(row)
  return rows[randint(0, len(rows) - 1)]