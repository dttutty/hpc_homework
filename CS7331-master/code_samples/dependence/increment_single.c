#include<stdio.h>
#include<omp.h>

using namespace std;

int main() {
  int i = 17;
  int j = 0;
  int k = 0;

  omp_set_num_threads(2);
  #pragma omp parallel
  {
    #pragma omp single
    {
  	printf("Thread %d incrementing\n", omp_get_thread_num());
	j++;
	printf("Thread %d incrementing\n", omp_get_thread_num());
	k++;
    }
  }

  printf("result = %d\n", i + j + k);

  return 0;
}
