#include<stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DEPTH 4
#define ROWS 6
#define COLS 7

int max_number(int list[]) {
  int max = list[0];
  for (int i = 1; i < sizeof(list) / sizeof(list[0]); i++) {
    if (list[i] > max) {
      max = list[i];
    }
  }
  return max;
}


void move(int field[ROWS][COLS], int player, int row) {

  for (int i = ROWS - 1; i >= 0; i--) {
    if (field[row][i] == 0) {
      field[row][i] = player;
      return; // successful move
    }
  }
  
  printf("Column is full!\n");
  return; // column is full
}


int heuristik(int field[ROWS][COLS], int player) {
  return 0;
}


int minmax_step(int field[ROWS][COLS], int player, int depth) {

  int points[ROWS];
  memset(points, 0, sizeof(points));

  if (depth > MAX_DEPTH) {
    return heuristik(field, player);
  }

  for (int row = 0; row < ROWS; row++) {

    // TODO: create copy of field 

    if (field[row][0] == 0) { // check if the column is not full
      // simulate the move
      move(field, player, row); // assuming player is represented by an integer

      // recursive call
      points[row] = minmax_step(field, -player, depth + 1); // switch player

      // undo the move
      field[row][0] = 0;
    } else {
      points[row] = -10000; // invalid move
    }
  }

  if (player == 1) { // maximizing player
    return max_number(points);
  } else { // minimizing player
    return -max_number(points); // invert for minimizing
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
  for (int i = 0; i < ROWS; i++) {
    if (points[i] == max_points) {
      indizes[count++] = i;
    }
  }

  int row = indizes[rand() % count];

  return row;
}


void load_field(int field[ROWS][COLS]) {
    // Print the loaded field 
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            printf("%d ", field[i][j]);
        }
        printf("\n");
    }
}


int main(int argc, char *argv[]) {
  bool debug = argv[1] == "True" ? true : false;

  int field[ROWS][COLS];
  
  for (int i = 0; i < ROWS; i++) {
      for (int j = 0; j < COLS; j++) {
          // load field from stdin
          if (scanf("%d", &field[i][j]) != 1) {
              fprintf(stderr, "Fehler beim Lesen der Eingabedaten.\n");
              return 1;
          }
      }
  }

  load_field(field);

  printf("Field loaded.\n");

  //int path = choose_best_path(NULL, NULL);
  return 0;
}