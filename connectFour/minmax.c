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


int check_win(int field[][HEIGHT], int player, int needed_length) {
  // Check horizontal, vertical, and diagonal for a win
  for (int x = 0; x < WIDTH; x++) {
    for (int y = 0; y < HEIGHT; y++) {
      // Check vertical
      int i = 0;
      while (field[x][y + i] == player) {
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
      while (field[x + i][y] == player) {
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
      while (field[x + 1][y + i] == player) {
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
      while (field[x - 1][y + i] == player) {
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


int move(int field[][HEIGHT], int current_player, int row) {

  for (int i = HEIGHT - 1; i >= 0; i--) {
    if (field[row][i] == 0) {
      field[row][i] = current_player;
      return check_win(field, current_player, 4); // successful move
    }
  }

  return -1; // column is full
}


int heuristik(int field[][HEIGHT], int player) {
  int base_player_check = check_win(field, player, 3);
  int opponent_player_check = check_win(field, (player % 2) + 1, 3);
  if (base_player_check > 0) {
    return 1;
  } else if (base_player_check > 0) {
    return -1;
  }

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
  int points_paths[WIDTH]; // indicates how good each path is; if the path is not finished yet, it gets 0 points
  memset(points_paths, 0, sizeof(points_paths)); // initialize points to 0

  if (depth > MAX_DEPTH) {
    return heuristik(old_field, base_player);
  }

  for (int row = 0; row < WIDTH; row++) {

    int field[WIDTH][HEIGHT];
    memcpy(field, old_field, sizeof(int) * WIDTH * HEIGHT); // copy the field

    int win = 0;

    // play the next move
    win = move(field, current_player, row);
    
    if (debug_level > 1) {
      printf("minmax_step - depth: %d, base_player: %d, current_player: %d, row: %d, win: %d\n", depth, base_player, current_player, row, win);
    }

    // No end of game reached yet
    if (win == 0) {
      points_paths[row] = minmax_step(field, base_player, (current_player % 2) + 1, depth + 1); // switch player
    }
    // Draw
    else if (win == -1) {
      points_paths[row] = 0;
    }
    // A player has won
    else {
      // Points awarded for win or loss
      int points;
      if (win == base_player) {
        points =  MAX_DEPTH - depth + 2; // more points for winning sooner
      } else {
        points = -(MAX_DEPTH - depth + 2);
      }      
      //printf("\npoints: %d", points);
      points_paths[row] = points;
      break;
    }
  }

  if (depth == 0) {
    int path = choose_best_path(old_field, points_paths);
    return path;
  }

  if (depth % 2 == 0) {
    // Player's turn: maximize
    return max_number(points_paths, WIDTH);
  } else {
    // Opponent's turn: minimize
    return min_number(points_paths, WIDTH);
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