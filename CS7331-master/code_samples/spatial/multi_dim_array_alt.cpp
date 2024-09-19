#include<stdlib.h>
#include<stdio.h>

int main(int argc, char *argv[]) {

  if (argc < 2) {
    fprintf(stderr, "usage: \n");
    fprintf(stderr, "       ./multi_dim_array N\n");
    exit(0);
  }

  int N = atoi(argv[1]);
  
  int **a = (int **) malloc(sizeof(int *) * N);
  
  int i,j;
  for (i = 0; i < N; i++) 
    a[i] = (int *) malloc(sizeof(int) * N);

  for (j = 0; j < N; j++) 
    for (i = 0; i < N; i++)
      a[i][j] = 17;

  printf("%d\n", a[17][17]);
  return 0;

}
