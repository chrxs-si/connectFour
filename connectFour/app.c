#include<stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  int list[] =  {1, 2, 3, 4, 5, 6};
  printf("sizeof test: %d\n", (sizeof(list) / sizeof(list[0])));
}