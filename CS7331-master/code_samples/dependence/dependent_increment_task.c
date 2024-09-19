#include<stdio.h>

int main() {

  int i = 17;
  int j = 0;
  int k = 0;

#pragma omp parallel
{
  #pragma omp single
  {
    #pragma omp task
    j = i + 1;

    #pragma omp task
    k = j + 1;
  }
 }

 printf("result = %d\n", k);

 return 0;
}
