#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>

#define VAL_RANGE 1023

double mysecond() {
  struct timeval tp;
  struct timezone tzp;
  int i;
  i = gettimeofday(&tp,&tzp);
  return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
}

double dot_prod(double *x, double *y, int n) {
  double res = 0.0;
  int i;

  for (i = 0; i < n; i++)
      res += x[i] * y[i];
  return res;
}

void matrix_vector_mult(double **mat, double *vec, double *result, 
			long long rows, long long cols) { 
  int i;
  for (i = 0; i < rows; i++)
    result[i] = dot_prod(mat[i], vec, cols);
}

void display_matrix(const double **matrix, long long N) {
  int i, j;
  for (i = 0; i < N; i++) {
    for (j = 0; j < N; j++) 
      printf("%3.4f ", matrix[i][j]);
    printf("\n");
  }
}

int main(int argc, char *argv[]) {
  struct timeval start, end;
  long seconds, useconds;
  double elapsed;
  gettimeofday(&start, NULL);

  double **matrix;
  double *vec;
  double *result;

  if (argc < 3) {
    printf("usage: \n");
    printf("       ./matvec N n\n");
    printf("       N = matrix dimension\n");
    printf("       n = number of reps\n");
    exit(0);
  }

  long long N = atoi(argv[1]);
  unsigned n = atoi(argv[2]);
  int i, j;


  matrix = (double **) malloc(sizeof(double *) * N);
  for (i = 0; i < N; i++)
    matrix[i] = (double *) malloc(sizeof(double) * N);


  vec = (double *) malloc(sizeof(double) * N);
  result = (double *) malloc(sizeof(double) * N);

  for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
      matrix[i][j] = rand() / (double) (RAND_MAX/VAL_RANGE);
     
  for (i = 0; i < N; i++)
    vec[i] = rand() / (double) (RAND_MAX/VAL_RANGE);
  
  double t0 = mysecond();
  for (i = 0; i < n; i++)
    matrix_vector_mult(matrix, vec, result, N, N);
  t0 = (mysecond() - t0) * 1.e3;
  
  printf("Result = %3.2e\n", result[N - 1]);


  gettimeofday(&end, NULL);

  seconds  = end.tv_sec  - start.tv_sec;
  useconds = end.tv_usec - start.tv_usec;
  elapsed = seconds + useconds / 1000000.0;
  printf("Elapsed time: %f seconds\n", elapsed);

  return 0;
}
