#include<stdlib.h>
#include<stdio.h>
#include<omp.h>

#define N 100

int main(int argc, char *argv[]) {

  float **a, **b;
  
  int dim = atoi(argv[1]);
  int THREADS = atoi(argv[2]);

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

  omp_set_num_threads(THREADS);
  float scale = 0.17;
#pragma omp parallel for private(i,j)
  for (k = 0; k < N; k++)
    for (i = 0; i < dim; i++)
      for (j = 0; j < dim; j++) 
	a[i][j] = b[i][j] * scale;


  printf("a[17][17] = %3.2f\n",a[17][17]);

  return 0;

}
