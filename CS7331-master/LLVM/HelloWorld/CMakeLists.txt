set(LLVM_LINK_COMPONENTS support)

add_clang_executable(hello-world-pass
  HelloWorld.cpp
  )
target_link_libraries(hello-world-pass
  PRIVATE
  clangTooling
  clangBasic
  clangASTMatchers
  )
