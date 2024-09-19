// 
// Expects headers to be in $LLVM_SRC/include; need to specify subdirs after that 
// Will need to change CMAKE files to alter include PATH 
//
#include "llvm/Pass.h"                                // writing a pass; 
#include "llvm/IR/Function.h"                         // writing a Function pass 
#include "llvm/Support/raw_ostream.h"                 // LLVM I/O



using namespace llvm;  // LLVM has own namespace 

namespace {                                       // make names local to _this_ file. don't want conflicts
  struct HelloWorld : public FunctionPass {       // writng a function pass (module-function-bb-stmt)
    static char ID;                               // help LLVM to track this pass (for efficiency)
                                                  // must be called ID
    HelloWorld() : FunctionPass(ID) {} 

    // must define a runOnFunction() for any function pass we want to create.    
    // overrides abstract method in FunctionPass class
    // When the pass is invoked on a function, this is where execution starts
    bool runOnFunction(Function &F) override {
      errs() << "Hello from  " << F.getName() << "\n";  
      return false;
    }
  };
}   

char HelloWorld::ID = 0;   // value can be anything, LLVM just looks at the address 

// Register your pass with opt (if you want to run it directly through clang then follow
// alternate method with legacu pass manager
// "hello" is the command-line argument needed to invoke this pass
// "Hello World Pass" is the name of this pass 
static RegisterPass<HelloWorld> X("hello", "Hello World Pass",
                             false /* Only looks at CFG */,
                             false /* Analysis Pass */);


