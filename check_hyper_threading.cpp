#include <iostream>

#if defined(_MSC_VER)
#include <intrin.h>
#elif defined(__GNUC__) || defined(__clang__)
#include <cpuid.h>
#endif

int main() {
    unsigned int eax, ebx, ecx, edx;

    // 调用 CPUID，功能号为 1
#if defined(_MSC_VER)
    int CPUInfo[4];
    __cpuid(CPUInfo, 1);
    eax = CPUInfo[0];
    ebx = CPUInfo[1];
    ecx = CPUInfo[2];
    edx = CPUInfo[3];
#elif defined(__GNUC__) || defined(__clang__)
    __cpuid(1, eax, ebx, ecx, edx);
#endif

    // 检查 edx 第28位（Hyper-Threading Technology Available）
    bool hyperThreading = edx & (1 << 28);

    if (hyperThreading) {
        std::cout << "CPU 支持超线程（Hyper-Threading）。" << std::endl;
    } else {
        std::cout << "CPU 不支持超线程（Hyper-Threading）。" << std::endl;
    }

    return 0;
}
