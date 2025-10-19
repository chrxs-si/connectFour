#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#define MAX_DEPTH 6
#define WIDTH 7
#define HEIGHT 6

int debug_level = 0;

int max_number(int list[], int size) {
  int max = list[0];
  for (int i = 0; i < size; i++) {
    if (list[i] > max) {
      max = list[i];
    }
  }
  return max;
}


int min_number(int list[], int size) {
  int min = list[0];
  for (int i = 0; i < size; i++) {
    if (list[i] < min) {
      min = list[i];
    }
  }
  return min;
}


int check_win(int field[][HEIGHT], int player) {
  // Check horizontal, vertical, and diagonal for a win
  for (int x = 0; x < WIDTH; x++) {
    for (int y = 0; y < HEIGHT; y++) {
      // Check vertical
      if (y <= HEIGHT - 4) {
        if (field[x][y] == player && field[x][y+1] == player && field[x][y+2] == player && field[x][y+3] == player) {
          return player;
        }
      }
      // Check horizontal
      if (x <= WIDTH - 4) {
        if (field[x][y] == player && field[x+1][y] == player && field[x+2][y] == player && field[x+3][y] == player) {
          return player;
        }
      }
      // Check diagonal (bottom-left to top-right)
      if (x <= WIDTH - 4 && y <= HEIGHT - 4) {
        if (field[x][y] == player && field[x+1][y+1] == player && field[x+2][y+2] == player && field[x+3][y+3] == player) {
          return player;
        }
      }
      // Check diagonal (top-left to bottom-right)
      if (x >= 3 && y <= HEIGHT - 4) {
        if (field[x][y] == player && field[x-1][y+1] == player && field[x-2][y+2] == player && field[x-3][y+3] == player) {
          return player;
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


int move(int field[][HEIGHT], int current_player, int row) {

  printf("%d\n", row);

  for (int i = HEIGHT - 1; i >= 0; i--) {
    if (field[row][i] == 0) {
      field[row][i] = current_player;
      return check_win(field, current_player); // successful move
    }
  }
  
  printf("Column is full!\n");
  return -1; // column is full
}


int heuristik(int field[][HEIGHT], int player) {
  return 0;
}


int choose_best_path(int field[][HEIGHT], int points[]) {

  // check in which row a move can actually be made
  for (int row = 0; row < WIDTH; row++) {
    if (field[row][0] != 0) {
      printf("choose_best_path - row %d, field: %d\n", row, field[row][0]);
      points[row] = -10000;
    }
  }

  int max_points = max_number(points, WIDTH);
  int indizes[WIDTH];
  int count = 0;
  for (int x = 0; x < WIDTH; x++) {
    if (points[x] == max_points) {
      indizes[count++] = x;
    }
  }

  if (debug_level > 1) {
    printf("choose_best_path - max_points: %d, count: %d, indizes:", max_points, count);
    for (int x = 0; x < WIDTH; x++) {
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


int minmax_step(int old_field[WIDTH][HEIGHT], int base_player, int current_player, int depth) {
  int points[WIDTH]; // indicates how good each path is; if the path is not finished yet, it gets 0 points
  memset(points, 0, sizeof(points)); // initialize points to 0

  if (depth > MAX_DEPTH) {
    return heuristik(old_field, base_player);
  }

  for (int row = 0; row < WIDTH; row++) {

    int field[WIDTH][HEIGHT];
    printf("old_field[%d][0]: %d\n", row, field[row][0]);
    memcpy(field, old_field, sizeof(int) * WIDTH * HEIGHT); // copy the field

    int win = 0;

    // Check if the row still has space
    printf("field: %d, row: %d\n", field[row][0], row);
    // play the next move
    win = move(field, current_player, row);
    
    if (debug_level > 1) {
      printf("minmax_step - depth: %d, base_player: %d, current_player: %d, row: %d, win: %d\n", depth, base_player, current_player, row, win);
    }


    // No end of game reached yet
    if (win == 0) {
      points[row] = minmax_step(field, base_player, (current_player % 2) + 1, depth + 1); // switch player
    }
    // Draw
    else if (win == -1) {
      points[row] = 0;
    }
    // A player has won
    else {
      // Points awarded for win or loss
      int point = MAX_DEPTH - depth + 2;
      if (win == base_player) {
        point *= 1; // more points for winning sooner
      } else {
        point *= -1;
      }      
      points[row] = point;
      break;
    }
  }

  if (depth == 0) {
    int path = choose_best_path(old_field, points);
    return path;
  }

  if (depth % 2 == 0) {
    // Player's turn: maximize
    return max_number(points, WIDTH);
  } else {
    // Opponent's turn: minimize
    return min_number(points, WIDTH);
  }
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
  for (int y = 0; y < HEIGHT; y++) {
    for (int x = 0; x < WIDTH; x++) {
        printf("%d ", field[x][y]);
    }
    printf("\n");
  }
  return 0;
}


int main(int argc, char *argv[]) {
  printf("calculating ...\n");
  
  srand(time(NULL)); // initialize random seed

  if (argc > 1) {
    debug_level = atoi(argv[1]);
  }

  if (debug_level > 0) {
    printf("Debug mode activated.\n");
  }
  
  int base_player = 0;  
  if (load_base_player(&base_player) != 0) {
    printf("Error loading player.\n");
    return 1;
  }
  int current_player = base_player;

  int field[WIDTH][HEIGHT];
  if (load_field(field) != 0) {
    return 1;
  }

  if (debug_level > 0) {
    print_field(field);   
  }

  int path = minmax_step(field, base_player, current_player, 0);

  printf(" %d\n", path);
   
  return 0;
}