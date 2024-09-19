add_library(HelloWorld MODULE
    HelloWorld.cpp
)

add_library(HelloWorld_clang MODULE
    HelloWorld_clang_loadable.cpp
)

# code has C++11 feature; must pass -std=c++11 
target_compile_features(HelloWorld PRIVATE cxx_range_for cxx_auto_type)
target_compile_features(HelloWorld_clang PRIVATE cxx_range_for cxx_auto_type)

# LLVM built with no C++ RTTI (runtime identification of object data)
# must pass this flag when building our pass
# otherwise it will look for names at _runtime_ that are not defined
# (e.g., FunctionPass) 
set_target_properties(HelloWorld PROPERTIES
   COMPILE_FLAGS "-DLLVM_DISABLE_ABI_BREAKING_CHECKS_ENFORCING=1 -fno-rtti"
)

set_target_properties(HelloWorld_clang PROPERTIES
   COMPILE_FLAGS "-DLLVM_DISABLE_ABI_BREAKING_CHECKS_ENFORCING=1 -fno-rtti"
)

