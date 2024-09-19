#include<stdio.h>
#include<omp.h>

int main() {

  int i = 17;
  int j = 0;
  int k = 0;

  j = i + 1;
  k = j + 1;

  printf("k = %d\n", k);

  return 0;
}
