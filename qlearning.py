import random
import pygame
from game import connectFour
import numpy as np
from collections import defaultdict
from copy import deepcopy
from tqdm import tqdm

class QAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.9995, epsilon_min=0.05):
        self.q_table = defaultdict(float)
        self.alpha = alpha  # Lernrate
        self.gamma = gamma  # Diskontierung
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def get_state(self, game):
        # Spielfeld in flache, hashbare Darstellung
        return tuple(cell for col in game.field for cell in col)

    def choose_action(self, game):
        valid_actions = [c for c in range(game.fieldwidth) if game.field[c][0] == 0]
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        else:
            state = self.get_state(game)
            q_vals = [self.q_table[(state, a)] for a in valid_actions]
            return valid_actions[np.argmax(q_vals)]

    def update_q(self, old_state, action, reward, new_state, done):
        old_q = self.q_table[(old_state, action)]
        future_qs = [self.q_table[(new_state, a)] for a in range(7)]
        max_future_q = max(future_qs) if not done else 0
        new_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
        self.q_table[(old_state, action)] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)




def train_agent(episodes=10000):
    agent = QAgent()
    for ep in tqdm(range(episodes)):
        game = connectFour(False)
        current_player = 1

        states = []
        actions = []

        while game.active:
            state = agent.get_state(game)
            action = agent.choose_action(game)
            win_state = game.chooseRow(action)
            new_state = agent.get_state(game)

            # Spiel vorbei?
            if win_state == current_player:
                agent.update_q(state, action, 1, new_state, True)
                break
            elif win_state == -1:
                agent.update_q(state, action, 0, new_state, True)
                break
            elif win_state != 0:
                agent.update_q(state, action, -1, new_state, True)
                break
            else:
                agent.update_q(state, action, 0, new_state, False)

        agent.decay_epsilon()

    return agent


def play_against_agent(agent):
    game = connectFour(True)
    human_player = int(input("Willst du anfangen? (1 = ja, 2 = nein): ") == "1") + 1

    while game.active:
        game.draw()
        pygame.time.delay(200)

        if game.currentPlayer == human_player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.active = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, _ = pygame.mouse.get_pos()
                    col = game.convertCoordinateToRow(x)
                    game.chooseRow(col)
        else:
            state = agent.get_state(game)
            action = agent.choose_action(game)
            game.chooseRow(action)
