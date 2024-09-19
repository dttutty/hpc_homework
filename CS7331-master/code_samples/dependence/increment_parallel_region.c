#include<stdio.h>
#include<omp.h>

int main() {
  int i = 17;
  int j = 0;
  int k = 0;

  omp_set_num_threads(2);

  #pragma omp parallel
  {
    j++;
    k++;
  }  

  printf("result = %d\n", i + j + k);

  return 0;
}
