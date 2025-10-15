import subprocess
from game import connectFour

path = "C:/Users/chris/Programming/Git/HWR/connectFour/connectFour/minmax.exe"

print("start")

try:
  cf = connectFour(False)

  cf.field[6][5] = 1
  cf.field[6][4] = 1
  cf.field[6][3] = 1
  cf.field[3][5] = 2
  cf.field[4][5] = 2

  data = ' '.join(str(cf.field[col][row]) for row in range(len(cf.field[0])) for col in range(len(cf.field)))

  print(f"data {data}")

  ergebnis = subprocess.run(
        [path, "True"],
        input=data,
        check=True,  # Löst eine Ausnahme aus, wenn die EXE einen Fehlercode zurückgibt
        capture_output=True,
        text=True
    )
  print(ergebnis.stdout)  # Ausgabe der EXE
  
except subprocess.CalledProcessError as e:
    print(f"Fehler beim Starten der EXE: {e}")
    print(f"Fehlerausgabe: \n{e.stderr}")
except FileNotFoundError:
    print(f"Fehler: Die Datei {path} wurde nicht gefunden.")