#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_DEPTH 4
#define ROWS 6
#define COLS 7

int max_number(int list[]) {
  int max = list[0];
  for (int i = 1; i < (sizeof(list) / sizeof(list[0])); i++) {
    if (list[i] > max) {
      max = list[i];
    }
  }
  return max;
}

int min_number(int list[]) {
  int min = list[0];
  for (int i = 1; i < (sizeof(list) / sizeof(list[0])); i++) {
    if (list[i] < min) {
      min = list[i];
    }
  }
  return min;
}


int check_win(int field[ROWS][COLS], int player) {
  // Check horizontal, vertical, and diagonal for a win
  for (int r = 0; r < ROWS; r++) {
    for (int c = 0; c < COLS; c++) {
      // Check horizontal
      if (c <= COLS - 4) {
        int i = 0;
        if (field[r][c] == player && field[r][c+1] == player && field[r][c+2] == player && field[r][c+3] == player) {
          return player;
        }
      }
      // Check vertical
      if (r <= ROWS - 4) {
        if (field[r][c] == player && field[r+1][c] == player && field[r+2][c] == player && field[r+3][c] == player) {
          return player;
        }
      }
      // Check diagonal (bottom-left to top-right)
      if (r <= ROWS - 4 && c <= COLS - 4) {
        if (field[r][c] == player && field[r+1][c+1] == player && field[r+2][c+2] == player && field[r+3][c+3] == player) {
          return player;
        }
      }
      // Check diagonal (top-left to bottom-right)
      if (r >= 3 && c <= COLS - 4) {
        if (field[r][c] == player && field[r-1][c+1] == player && field[r-2][c+2] == player && field[r-3][c+3] == player) {
          return player;
        }
      }
    }
  }

  // Check for draw
  bool is_draw = true;
  for (int r = 0; r < ROWS; r++) {
    if (field[r][0] == 0) {
      is_draw = false;
      break;
    }
  }
  if (is_draw) {
    return -1; // Draw
  }

  return 0; // No win yet
}


int move(int field[ROWS][COLS], int player, int row) {

  for (int i = ROWS - 1; i >= 0; i--) {
    if (field[row][i] == 0) {
      field[row][i] = player;
      return check_win(field, player); // successful move
    }
  }
  
  printf("Column is full!\n");
  return -1; // column is full
}


int heuristik(int field[ROWS][COLS], int player) {
  return 0;
}


int minmax_step(int old_field[ROWS][COLS], int player, int depth) {
  int points[ROWS]; // indicates how good each path is; if the path is not finished yet, it gets 0 points
  memset(points, 0, sizeof(points)); // initialize points to 0

  if (depth > MAX_DEPTH) {
    return heuristik(&old_field, player);
  }

  for (int row = 0; row < ROWS; row++) {

    int field[ROWS][COLS];
    memcpy(&field, &old_field, sizeof(old_field)); // copy the field

    int win = 0;

    // Check if the row still has space
    if (&field[row][0] == 0) { 
      // play the next move
      win = move(field, player, row);
    }
    else {
      win = -1; // The row is already full, so its a draw
    }


    // No end of game reached yet
    if (win == 0) {
      points[row] = minmax_step(field, -player, depth + 1); // switch player
    }
    // Draw
    else if (win == -1) {
      points[row] = 0;
    }
    // A player has won
    else {
      // Points awarded for win or loss
      int point = 0;
      if (win == player) {
        point = 1;
      } else {
        point = -1;
      }      
      points[row] = point;
      break;
    }
  }

  if (depth % 2 == 0) {
    // Player's turn: maximize
    return max_number(points);
  } else {
    // Opponent's turn: minimize
    return min_number(points);
  }
}


int choose_best_path(int field[ROWS][COLS], int points[]) {
  
  // check in which row a move can actually be made
  for (int row = 0; row < ROWS; row++)
    if (field[row][0] != 0) {
      points[row] = -10000;
  }

  int max_points = max_number(points);
  int indizes[ROWS];
  int count = 0;
  for (int r = 0; r < ROWS; r++) {
    if (points[r] == max_points) {
      indizes[count++] = r;
    }
  }

  int row = indizes[rand() % count];

  // Debug output
  if (points) {
    printf("minmax - row: %d, points:", row);
    for (int r = 0; r < ROWS; r++) {
      printf(" %d", points[r]);
    }
    printf("\n");
  } else {
    printf("minmax - row: %d, points: (null)\n", row);
  }
  return row;
}


int load_field(int field[ROWS][COLS]) {
  for (int r = 0; r < ROWS; r++) {
    for (int c = 0; c < COLS; c++) {
      // load field from stdinW
      if (scanf("%d", &field[r][c]) != 1) {
        fprintf(stderr, "Error reading input and loading field.\n");
        return  1;
      }
    }
  }
  return 0;
}


int print_field(int field[ROWS][COLS]) {
  // Print the loaded field 
  for (int r = 0; r < ROWS; r++) {
    for (int c = 0; c < COLS; c++) {
        printf("%d ", &field[r][c]);
    }
    printf("\n");
  }
  
  printf("Field loaded.\n");

  return 0;
}


int main(int argc, char *argv[]) {
  printf("calculating ...");

  bool debug = (argc > 1 && strcmp(argv[1], "True") == 0);

  int field[ROWS][COLS];

  if (!load_field(field)) {
    return 1;
  }

  if (debug) {
    print_field(field);   
  }

  int path = choose_best_path(field, NULL);
   
  return path;
}