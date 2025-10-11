#include<stdio.h>
#include <stdlib.h>
#include <string.h>


int max_number(int list[]) {
  int max = list[0];
  for (int i = 1; i < sizeof(list) / sizeof(list[0]); i++) {
    if (list[i] > max) {
      max = list[i];
    }
  }
  return max;
}


int choose_best_path(int cf[], int points[]) {
  
  int max_rows = sizeof(points) / sizeof(points[0]); 

  // check in which row a move can actually be made
  for (int row = 0; row < max_rows; row++)
    if (cf[row][0] != 0) {
      points[row] = -10000;
  }

  int max_points = max_number(points);
  int indizes[max_rows];
  for (int i = 0; i < sizeof(points) / sizeof(points[0]); i++) {
    if (points[i] == max_points) {
      indizes.push(i);
    }
  }

  int row = indizes[rand() % sizeof(indizes) / sizeof(indizes[0])];

  return row;
}

int main(int argc, char *argv[]) {
  char *uebergebener_wert_als_string = argv[1];
  printf("Erster Wert (argv[1]): %s\n", uebergebener_wert_als_string);
  return 0;
}