#include<stdlib.h>
#include<stdio.h>

int main(int argc, char *argv[]) {
  float **a, **b;
  
  int dim = atoi(argv[1]);
  int BLOCK = atoi(argv[2]);
  
  a = (float **) malloc(sizeof(float *) * dim);
  b = (float **) malloc(sizeof(float *) * dim);
  
  int i,j,k,jj;
  for (i = 0; i < dim; i++) {
    a[i] = (float *) malloc(sizeof(float) * dim);
    b[i] = (float *) malloc(sizeof(float) * dim);
  }
  
  for (i = 0; i < dim; i++)
    for (j = 0; j < dim; j++) { 
      a[i][j] = 2.3;
      b[i][j] = 1.7;
    }

  float scale = 0.17;
  for (j = 0; j < dim; j = j + BLOCK) 
    for (k = 0; k < 100; k++)
      for (i = 0; i < dim; i++)
	for (jj = j; jj < j + BLOCK; jj++) 
	  a[i][jj] = b[i][jj] * scale;
  

  printf("a[17][17] = %3.2f\n",a[17][17]);

  return 0;

}
