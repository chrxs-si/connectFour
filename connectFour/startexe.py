import subprocess

path = "C:/Users/chris/Programming/Git/HWR/connectFour/connectFour/minmax.exe"

print("start")

try:
  ergebnis = subprocess.run(
        [path, "TESTWERT"],
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