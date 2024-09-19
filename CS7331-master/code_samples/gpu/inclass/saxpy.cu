#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>

#define VAL_RANGE 1023

double mysecond() {
  struct timeval tp;
  struct timezone tzp;
  gettimeofday(&tp,&tzp);
  return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
}

void saxpy_cpu(int n, float s, float* x, float* y) {
  for(int i = 0; i < n; i++) 
    y[i] = s * x[i] + y[i];
}


__global__ void  saxpy(int n, float s, float* x, float* y) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i < n)
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

  result = (float *) malloc(sizeof(float) * N);

  for (i = 0; i < N; i++) {
    x[i] = rand() / (float) (RAND_MAX/VAL_RANGE);
    y[i] = rand() / (float) (RAND_MAX/VAL_RANGE);
  }

  float* dev_x;
  float* dev_y;
  cudaMalloc(&dev_x, N * sizeof(float));
  cudaMalloc(&dev_y, N * sizeof(float));

  float s = 2.3;

  cudaMemcpy(dev_x, x, N * sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(dev_y, y, N * sizeof(float), cudaMemcpyHostToDevice);

  int blocksize = 1024;
  int numblocks = N/blocksize; // assume N is evenly divisible by block size
  saxpy<<<numblocks, blocksize>>>(N, s, dev_x, dev_y);

  cudaMemcpy(result, dev_y, N * sizeof(float), cudaMemcpyDeviceToHost);

  // verify

  saxpy_cpu(N, s, x, y);
  if (y[17] == result[17]) 
    printf("Passed %3.4f.\n", result[17]);

  cudaDeviceReset();
  return 0;
}

