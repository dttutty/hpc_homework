#include<stdlib.h>
#include<stdio.h>

#define VAL_RANGE 1023

bool check(int *a, int *b, int M) {
  for (unsigned i = 0; i < M; i++) 
    if (b[i] != a[i])
      return false;

  return true;
}

int get_rand(bool *rands, int range) {
  int rand_num; 
  do
    rand_num = rand() % range;
  while(rands[rand_num]);
  rands[rand_num] = true;
  return rand_num;
}

int main(int argc, char *argv[]) {

  if (argc < 3) {
    fprintf(stderr, "usage: \n");
    fprintf(stderr, "       ./array_copy N M\n");
    exit(0);
  }

  int N = atoi(argv[1]);
  int M = atoi(argv[2]);

  int *a, *b;
  
  a = (int *) malloc(sizeof(int) * N);
  b = (int *) malloc(sizeof(int) * M);

  bool *rands = (bool *) malloc(sizeof (bool) * M);
  for (unsigned i = 0; i < M; i++) 
    rands[i] = false;

  for (unsigned i = 0; i < N; i++) 
    a[i] = rand() / (double) (RAND_MAX/VAL_RANGE);

  for (unsigned i = 0; i < M; i++) {
    int j = get_rand(rands, M);
    b[i] = a[j];
  }


  if (check(a, b, M))
    fprintf(stderr, "PASS\n");
  else
    fprintf(stderr, "FAIL\n");
    
  return 0;

}
