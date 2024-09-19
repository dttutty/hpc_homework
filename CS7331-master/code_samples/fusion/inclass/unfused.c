#include<stdlib.h>
#include<stdio.h>

#define DIMSIZE 80

int main(int argc, char *argv[]) {
  int **a, **b, **c, **d;
  
  int dim = atoi(argv[1]);

  a = (int **) malloc(sizeof(int *) * dim);
  b = (int **) malloc(sizeof(int *) * dim);
  c = (int **) malloc(sizeof(int *) * dim);
  d = (int **) malloc(sizeof(int *) * dim);
  
  int i,j,k;
  for (i = 0; i < dim; i++) {
    a[i] = (int *) malloc(sizeof(int) * dim);
    b[i] = (int *) malloc(sizeof(int) * dim);
    c[i] = (int *) malloc(sizeof(int) * dim);
    d[i] = (int *) malloc(sizeof(int) * dim);
  }
  
  for (i = 1; i < dim; i++)
    for (j = 1; j < dim; j++) { 
      a[i][j] = 0;
      b[i][j] = 1.0;
    }


  for (i = 1; i < dim; i++)
    for (j = 1; j < dim; j++) {
      c[i][j] = 0;
      d[i][j] = 1.0;
    }


  float scale = 0.17;
  for (k = 0; k < 10; k++) {
    for (i = 1; i < dim; i++)
      for (j = 1; j < dim; j++) 
	a[i][j] = b[i][j] * scale;
  }
  for (k = 0; k < 10; k++) {
    for (i = 1; i < dim; i++)
      for (j = 1; j < dim; j++) 
	c[i][j] = a[i][j] + d[i][j] * scale;
  }

    
  printf("%d\n",c[10][10]);

  return 0;

}
