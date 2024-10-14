#include <iostream>

int main() {
    int j, k;
    int lastrow = 100;
    int firstrow = 1;
    double *a = new double[100];
    double *p = new double[100];
    double *w = new double[100];   
    int *colidx = new int[100];
    int *rowstr = new int[100];
    
    for (j = 1; j <= lastrow - firstrow + 1; j++)
    {
        double sum = 0.0;
        for (k = rowstr[j]; k < rowstr[j + 1]; k++)
        {
            sum = sum + a[k] * p[colidx[k]];
        }
        w[j] = sum;
    }

    for (j = 1; j <= lastrow - firstrow + 1; j++) {
        int iresidue;
        double sum1 = 0.0, sum2 = 0.0;
        int i = rowstr[j];
        iresidue = (rowstr[j + 1] - i) % 2;
        if (iresidue == 1) sum1 = sum1 + a[i] * p[colidx[i]];
        for (k = i + iresidue; k <= rowstr[j + 1] - 2; k += 2) {
            sum1 = sum1 + a[k] * p[colidx[k]];
            sum2 = sum2 + a[k + 1] * p[colidx[k + 1]];
        }
        w[j] = sum1 + sum2;
    }

    return 0;
}
