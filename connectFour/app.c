#include<stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  char *uebergebener_wert_als_string = argv[1];
  printf("Erster Wert (argv[1]): %s\n", uebergebener_wert_als_string);
  return 0;
}