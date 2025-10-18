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

  cf.field[0][5] = 1
  cf.field[0][4] = 2
  cf.field[0][3] = 1
  cf.field[0][2] = 2
  cf.field[0][1] = 1
  cf.field[0][0] = 2


  data = '1 ' + ' '.join(str(cf.field[col][row]) for row in range(len(cf.field[0])) for col in range(len(cf.field)))

  print(f"data {data}")

  ergebnis = subprocess.run(
        [path, " 2"],
        input=data,
        check=False,  # Löst eine Ausnahme aus, wenn die EXE einen Fehlercode zurückgibt
        capture_output=True,
        text=True
    )
    
  
  stdout = ergebnis.stdout.strip()
  tokens = stdout.split()
  print(f"Output from EXE:\n {stdout}")
  if len(tokens) > 0:
    print(f"Return value: {tokens[-1]}")  # Ausgabe der EXE
  
except subprocess.CalledProcessError as e:
    print(f"Fehler beim Starten der EXE: {e}")
    print(f"Fehlerausgabe: \n{e.stderr}")
except FileNotFoundError:
    print(f"Fehler: Die Datei {path} wurde nicht gefunden.")