#include<stdlib.h>
#include<stdio.h>

#define DIMSIZE 5000

int main() {
  int **a;
  
  a = (int **) malloc(sizeof(int *) * DIMSIZE);
  
  int i, j;
  for (i = 0; i < DIMSIZE; i++) 
    a[i] = (int *) malloc(sizeof(int) * DIMSIZE);


  for (i = 0; i < DIMSIZE; i++)
    for (j = 0; j < DIMSIZE; j++) 
      a[i][j] = 17;

  return 0;

}
