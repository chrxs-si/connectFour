from game import connectFour
import threading
from itertools import permutations
from collections import Counter

MAX_DEPTH = 4

def getMinMaxMove(cf, player):
  wins = [0] * len(cf.field)
  print(wins)
  for x in range(len(cf.field)):
    games = []


def generate_permutations(n):
    # Ursprüngliche Liste mit n Wiederholungen jeder Zahl von 0 bis 5
    original_list = [i for i in range(6) for _ in range(n)]
    
    # Verwende set(), um Duplikate zu vermeiden
    unique_permutations = set(permutations(original_list))
    
    return unique_permutations

# Beispiel: n = 2
n = 2
all_perms = generate_permutations(n)

print(f"Anzahl der eindeutigen Permutationen: {len(all_perms)}")
for p in list(all_perms)[:10]:  # Nur die ersten 10 anzeigen
    print(p)


#cf = connectFour()

#move = getMinMaxMove(cf, 2)
#win = cf.chooseRow(move)

[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5]

[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]