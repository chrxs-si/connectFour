# Connect Four

This is a Python implementation of the classic Connect Four game with diffrent AI strategies.

## Features

- Play Connect Four against different AI strategies:
  - Minimax algorithm programmed in python. (very slow & not very good at connect 4)
  - Minimax algorithm programmed in c. (slow & yet very bad at connect 4, but still in progress)
  - Monte Carlo Tree Search (fast & very good at connect 4)
  - Neuroevolution (very fast & bad at connect 4)
  - Random moves (very fast & very bad at connect 4)

## How to Run

1. Clone project: ```clone https://github.com/chrxs-si/connectFour.git```.
2. create venv: ```python -m venv venv```.
3. install requirements ```pip install -r .\requirements.txt```
2. choose AI by changing player variable in main.py.
5. Run the main program: ```python ./connectFour/main.py```