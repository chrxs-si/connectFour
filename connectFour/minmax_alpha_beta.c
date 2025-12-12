#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#define WIDTH 7
#define HEIGHT 6

int MAX_DEPTH = 6;
int debug_level = 0;

int max_number(int list[], int size) {
    int max = list[0];
    for (int i = 1; i < size; i++) {
        if (list[i] > max) max = list[i];
    }
    return max;
}

int min_number(int list[], int size) {
    int min = list[0];
    for (int i = 1; i < size; i++) {
        if (list[i] < min) min = list[i];
    }
    return min;
}


int check_win(int field[][HEIGHT], int player, int needed_length) {
  // Check horizontal, vertical, and diagonal for a win
  for (int x = 0; x < WIDTH; x++) {
    for (int y = 0; y < HEIGHT; y++) {
      // Check vertical
      int i = 0;
      while (y+i < HEIGHT && field[x][y + i] == player) {
        i++;
        if (i >= needed_length) {
          return player;
        }
        if (y + i >= HEIGHT) {
          break;
        }
      }
      // Check horizontal
      i = 0;
      while (x+i < WIDTH && field[x + i][y] == player) {
        i++;
        if (i >= needed_length) {
          return player;
        }
        if (x + i >= WIDTH) {
          break;
        }
      }
      // Check diagonal (bottom-left to top-right)
      i = 0;
      while (x+i < WIDTH && y+i < HEIGHT && field[x + i][y + i] == player) {
        i++;
        if (i >= needed_length) {
          return player;
        }
        if (y + i >= HEIGHT || x + i >= WIDTH) {
          break;
        }
      }
      // Check diagonal (top-left to bottom-right)
      i = 0;
      while (x-i >= 0 && y+i < HEIGHT && field[x - i][y + i] == player) {
        i++;
        if (i >= needed_length) {
          return player;
        }
        if (y + i >= HEIGHT || x - i < 0) {
          break;
        }
      }
    }
  }

  // Check for draw
  bool is_draw = true;
  for (int x = 0; x < WIDTH; x++) {
    if (field[x][0] == 0) {
      is_draw = false;
      break;
    }
  }
  if (is_draw) {
    return -1; // Draw
  }

  return 0; // No win yet
}


int check_win_with_last_row(int field[][HEIGHT], int player, int needed_length, int last_x, int last_y) 
{
  int dirs[4][2][2] = {
    {{ 1,  0}, {-1,  0}}, // Horizontal
    {{ 0,  1}, { 0, -1}}, // Vertikal
    {{ 1,  1}, {-1, -1}}, // Diagonal
    {{ 1, -1}, {-1,  1}}, // Diagonal
  };

  for (int d = 0; d < 4; d++) {
    int count = 1;  // Startpunkt zählt

    // beide Richtungen der Achse ablaufen
    for (int s = 0; s < 2; s++) {
      int dx = dirs[d][s][0];
      int dy = dirs[d][s][1];
      int x = last_x + dx;
      int y = last_y + dy;

      while (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT && field[x][y] == player) 
      {
        count++;
        x += dx;
        y += dy;
      }
    }

    // Gewinn gefunden
    if (count >= needed_length)
      return player;
  }

  // Unentschieden prüfen
  for (int x = 0; x < WIDTH; x++) {
    if (field[x][0] == 0)
      return 0; // kein Draw, Spiel läuft
  }

  return -1; // Draw
}


int move(int field[][HEIGHT], int current_player, int row) {

  for (int i = HEIGHT - 1; i >= 0; i--) {
    if (field[row][i] == 0) {
      field[row][i] = current_player;
      return i; // return the row where the piece was placed
    }
  }

  return -1; // column is full
}

// Heuristik-Funktionen
int evaluate_window(int window[4], int player) {
    int opponent = (player % 2) + 1;
    int count_player = 0;
    int count_opponent = 0;
    int count_empty = 0;

    for (int i = 0; i < 4; i++) {
        if (window[i] == player) count_player++;
        else if (window[i] == opponent) count_opponent++;
        else count_empty++;
    }

    int score = 0;

    if (count_player == 4) score += 10000;
    else if (count_player == 3 && count_empty == 1) score += 100;
    else if (count_player == 2 && count_empty == 2) score += 10;

    if (count_opponent == 4) score -= 10000;
    else if (count_opponent == 3 && count_empty == 1) score -= 100;
    else if (count_opponent == 2 && count_empty == 2) score -= 10;

    return score;
}

int score_horizontal(int field[][HEIGHT], int player) {
    int score = 0;
    int window[4];

    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH - 3; x++) {
            for (int i = 0; i < 4; i++) window[i] = field[x + i][y];
            score += evaluate_window(window, player);
        }
    }

    return score;
}

int score_vertical(int field[][HEIGHT], int player) {
    int score = 0;
    int window[4];

    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT - 3; y++) {
            for (int i = 0; i < 4; i++) window[i] = field[x][y + i];
            score += evaluate_window(window, player);
        }
    }

    return score;
}

int score_diagonal_up(int field[][HEIGHT], int player) {
    int score = 0;
    int window[4];

    for (int x = 0; x < WIDTH - 3; x++) {
        for (int y = 3; y < HEIGHT; y++) {
            for (int i = 0; i < 4; i++) window[i] = field[x + i][y - i];
            score += evaluate_window(window, player);
        }
    }

    return score;
}

int score_diagonal_down(int field[][HEIGHT], int player) {
    int score = 0;
    int window[4];

    for (int x = 0; x < WIDTH - 3; x++) {
        for (int y = 0; y < HEIGHT - 3; y++) {
            for (int i = 0; i < 4; i++) window[i] = field[x + i][y + i];
            score += evaluate_window(window, player);
        }
    }

    return score;
}

int heuristik(int field[][HEIGHT], int player) {
    int opponent = (player % 2) + 1;

    // Harte Win-Checks für schnelle Pruning-Entscheidungen
    if (check_win(field, player, 4) == player)  return  100000;
    if (check_win(field, opponent, 4) == opponent) return -100000;

    int score = 0;

    score += score_horizontal(field, player);
    score += score_vertical(field, player);
    score += score_diagonal_up(field, player);
    score += score_diagonal_down(field, player);

    return score;
}


int choose_best_path(int field[][HEIGHT], int points[]) {

  // check in which row a move can actually be made
  for (int row = 0; row < WIDTH; row++) {
    if (field[row][0] != 0) {
      printf("choose_best_path - row %d, field: %d\n", row, field[row][0]);
      points[row] = -1000000; // column is full, cannot choose this path
    }
  }

  int max_point = max_number(points, WIDTH);
  int indizes[WIDTH];
  int count = 0;
  for (int x = 0; x < WIDTH; x++) {
    if (points[x] == max_point) {
      indizes[count++] = x;
    }
  }

  if (debug_level > 1) {
    printf("choose_best_path - max_points: %d, count: %d, indizes:", max_point, count);
    for (int x = 0; x < count; x++) {
      printf(" %d", indizes[x]);
    }
    printf("\n");
  }


  int row = indizes[rand() % count];

  // Debug output
  if (debug_level > 0) {
    printf("minmax - row: %d, points:", row);

    printf("\n");
  }
  if (points) {
    printf("points:");
    for (int x = 0; x < WIDTH; x++) {
      printf("%d,", points[x]);
    }
  }
  return row;
}


void get_column_order(int order[WIDTH]) {
    int center = WIDTH / 2;
    int index = 0;
    for (int offset = 0; offset <= center; offset++) {
        if (center - offset >= 0) order[index++] = center - offset;
        if (center + offset < WIDTH && offset != 0) order[index++] = center + offset;
    }
}

// MinMax mit Alpha-Beta-Pruning
int minmax_step(int old_field[WIDTH][HEIGHT], int base_player, int current_player, int depth, int alpha, int beta) {
    int points_paths[WIDTH];
    for (int i = 0; i < WIDTH; i++) points_paths[i] = 0;

    if (depth >= MAX_DEPTH) return heuristik(old_field, base_player);

    int column_order[WIDTH];
    get_column_order(column_order);

    for (int idx = 0; idx < WIDTH; idx++) {
        int row = column_order[idx];

        if (old_field[row][0] != 0) continue; // Spalte voll

        int field[WIDTH][HEIGHT];
        memcpy(field, old_field, sizeof(int) * WIDTH * HEIGHT);

        int last_y = move(field, current_player, row);
        int win = check_win_with_last_row(field, current_player, 4, row, last_y);

        int score;
        if (win == 0) {
            score = minmax_step(field, base_player, (current_player % 2) + 1, depth + 1, alpha, beta);
        } else if (win == -1) {
            score = 0; // Draw
        } else if (win == base_player) {
            score = 100000 - depth;
        } else {
            score = -(100000 - depth + 2);
        }

        points_paths[row] = score;

        // Alpha-Beta Update
        if (current_player == base_player) {
            if (score > alpha) alpha = score;
        } else {
            if (score < beta) beta = score;
        }

        if (alpha >= beta) break; // Pruning
    }

    if (depth == 0) return choose_best_path(old_field, points_paths);

    if (current_player == base_player) return max_number(points_paths, WIDTH);
    else return min_number(points_paths, WIDTH);
}


int load_base_player(int *base_player) {
  if (scanf("%d", base_player) != 1) {
    printf("Error reading input and loading player.\n");
    return 1;
  }
  return 0;
}


int load_field(int field[][HEIGHT]) {
  for (int x = 0; x < WIDTH; x++) {
    for (int y = 0; y < HEIGHT; y++) {
      // load field from stdin
      if (scanf("%d", &field[x][y]) != 1) {
        printf("Error reading input and loading field.\n");
        return  1;
      }
    }
  }
  return 0;
}


int print_field(int field[][HEIGHT]) {
  // Print the loaded field 
  printf("\nField:\n");
  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
        printf("%d ", field[x][y]);
    }
    printf("\n");
  }
  return 0;
}


int main(int argc, char *argv[]) {
    srand(time(NULL));

    if (argc > 1) MAX_DEPTH = atoi(argv[1]);
    if (argc > 2) debug_level = atoi(argv[2]);

    int base_player = 0;
    load_base_player(&base_player);
    int current_player = base_player;

    int field[WIDTH][HEIGHT];
    load_field(field);

    int path = minmax_step(field, base_player, current_player, 0, -1000000, 1000000);

    print_field(field);
    printf("Best column: %d\n", path);
    return 0;
}
