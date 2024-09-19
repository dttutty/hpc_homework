set(LLVM_LINK_COMPONENTS support)

add_clang_executable(cuda-kernel-analyzer
  CudaKernelAnalyzer.cpp
  )
target_link_libraries(cuda-kernel-analyzer
  PRIVATE
  clangTooling
  clangBasic
  clangASTMatchers
  )
