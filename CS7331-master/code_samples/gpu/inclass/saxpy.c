#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>

#include<omp.h>

#define VAL_RANGE 1023

double mysecond() {
  struct timeval tp;
  struct timezone tzp;
  gettimeofday(&tp,&tzp);
  return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
}

void saxpy(int n, float s, float* x, float* y) {
  int i;
  for(i = 0; i < n; i++) 
    y[i] = s * x[i] + y[i];
}

int main(int argc, char *argv[]) {

  float *x, *y;
  float *result;

  if (argc < 2) {
    printf("usage: \n");
    printf("       ./saxpy <size>\n");
    exit(0);
  }

  long long N = atoi(argv[1]);
  int i;

  x = (float *) malloc(sizeof(float) * N);
  y = (float *) malloc(sizeof(float) * N);

  for (i = 0; i < N; i++) {
    x[i] = rand() / (float) (RAND_MAX/VAL_RANGE);
    y[i] = rand() / (float) (RAND_MAX/VAL_RANGE);
  }

  float s = 2.3;
  double t0 = mysecond();
  saxpy(N, s, x, y);
  t0 = (mysecond() - t0) * 1.e3;

  fprintf(stdout, "%3.4f\n", y[17]);
  fprintf(stderr, "saxpy = %3.2f ms\n", t0);
  return 0;
}

