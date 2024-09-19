add_library(VRP MODULE
    vrp.cpp
)

# code has C++11 feature; must pass -std=c++11 
target_compile_features(VRP PRIVATE cxx_range_for cxx_auto_type)

# LLVM built with no C++ RTTI (runtime identification of object data)
# must pass this flag when building our pass
# otherwise it will look for names at _runtime_ that are not be defined
# (e.g., FunctionPass) 
set_target_properties(VRP PROPERTIES
   COMPILE_FLAGS "-DLLVM_DISABLE_ABI_BREAKING_CHECKS_ENFORCING=1 -fno-rtti"
)

