#include<stdlib.h>
#include<stdio.h>

#define REPS 100

int main(int argc, char *argv[]) {
  float **a, **b;

  if (argc < 2) {
    printf("usage: \n");
    printf("       ./scale N\n");
    exit(0);
  }

  int dim = atoi(argv[1]);
  
  a = (float **) malloc(sizeof(float *) * dim);
  b = (float **) malloc(sizeof(float *) * dim);
  
  int i,j,k;
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
  for (k = 0; k < REPS; k++)
    for (i = 0; i < dim; i++)
      for (j = 0; j < dim; j++) 
	a[i][j] = b[i][j] * scale;
  
  
  printf("a[17][17] = %3.2f\n",a[17][17]);
  
  return 0;

}
