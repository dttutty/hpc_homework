#include<stdio.h>    // 包含标准输入输出头文件
#include<stdlib.h>   // 包含标准库函数头文件
#include<sys/time.h> // 包含获取时间的头文件

#define VAL_RANGE 1023 // 定义常量VAL_RANGE为1023

double mysecond() {
  struct timeval tp;  // 定义timeval结构体tp，存储时间信息
  // struct timezone tzp; // 定义timezone结构体tzp（已注释掉）
  int i;              // 定义整型变量i
  i = gettimeofday(&tp, NULL);  // 获取当前时间，存入tp
  return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );  // 返回以秒为单位的时间
}

double dot_prod(double *x, double *y, int n) {
  double res = 0.0;  // 初始化结果为0
  int i;             // 定义循环变量i

  for (i = 0; i < n; i++)      // 遍历向量元素
      res += x[i] * y[i];      // 计算向量点积
  return res;                  // 返回结果
}

void matrix_vector_mult(double **mat, double *vec, double *result, 
    			long long rows, long long cols) { 
  int i;  // 定义循环变量i
  for (i = 0; i < rows; i++)                    // 遍历矩阵的每一行
    result[i] = dot_prod(mat[i], vec, cols);    // 计算矩阵行与向量的点积，存入结果数组
}

void display_matrix(const double **matrix, long long N) {
  int i, j;  // 定义循环变量i和j
  for (i = 0; i < N; i++) {          // 遍历矩阵的行
    for (j = 0; j < N; j++)          // 遍历矩阵的列
      printf("%3.4f ", matrix[i][j]); // 打印矩阵元素，保留4位小数
    printf("\n");                     // 换行
  }
}

int main(int argc, char *argv[]) {
  
  double t_all = mysecond();  // 记录程序开始时间

  double **matrix;  // 定义二维矩阵指针
  double *vec;      // 定义向量指针
  double *result;   // 定义结果向量指针

  if (argc < 3) {   // 检查命令行参数个数
    printf("usage: \n");
    printf("       ./matvec N n\n");
    printf("       N = matrix dimension\n");  // N为矩阵维度
    printf("       n = number of reps\n");    // n为重复次数
    exit(0);    // 退出程序
  }

  long long N = atoll(argv[1]);  // 将第一个参数转换为整数N
  unsigned n = (unsigned)atoi(argv[2]);   // 将第二个参数转换为整数n
  int i, j;                     // 定义循环变量i和j

  matrix = (double **) malloc(sizeof(double *) * N);  // 分配矩阵行指针数组
  for (i = 0; i < N; i++)
    matrix[i] = (double *) malloc(sizeof(double) * N);  // 为每一行分配空间

  vec = (double *) malloc(sizeof(double) * N);     // 分配向量空间
  result = (double *) malloc(sizeof(double) * N);  // 分配结果向量空间

  for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
      matrix[i][j] = rand() / (double) (RAND_MAX/VAL_RANGE);  // 随机初始化矩阵元素
         
  for (i = 0; i < N; i++)
    vec[i] = rand() / (double) (RAND_MAX/VAL_RANGE);  // 随机初始化向量元素
  
  double t0 = mysecond();  // 记录矩阵向量乘法开始时间
  for (i = 0; i < n; i++)
    matrix_vector_mult(matrix, vec, result, N, N);  // 重复进行矩阵向量乘法
  t0 = (mysecond() - t0) * 1.e3;       // 计算矩阵向量乘法耗时，转换为毫秒
  t_all = (mysecond() - t_all) * 1.e3; // 计算程序总耗时，转换为毫秒
  // printf("$ ./a.out %s %s\n", argv[1], argv[2]);
  printf("matrix_vector_mult execution time: %f ms\n", t0);  // 打印矩阵向量乘法耗时
  printf("total execution time: %f ms\n", t_all);            // 打印程序总耗时

  printf("Result = %3.2e\n", result[N - 1]);  // 打印结果向量的最后一个元素

  return 0;  // 程序正常结束
}
