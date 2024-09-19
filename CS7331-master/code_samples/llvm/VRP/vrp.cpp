// 
// Expects headers to be in $LLVM_SRC/include; need to specify subdirs after that 
// Will need to change CMAKE files to alter include PATH 
//
#include "llvm/Pass.h"                                // writing a pass; 
#include "llvm/IR/Function.h"                         // writing a Function pass 
#include "llvm/Support/raw_ostream.h"                 // LLVM I/O
#include "llvm/IR/LegacyPassManager.h"                // new pass manager under dev for a while 
#include "llvm/Transforms/IPO/PassManagerBuilder.h"   // possibly not working; most folks work with "Legacy" manager


using namespace llvm;  // LLVM has own namespace 

namespace {                                       // make names local to _this_ file. don't want conflicts
  struct VRP : public FunctionPass {       // writng a function pass (module-function-bb-stmt)
    static char ID;                               // help LLVM to track this pass (for efficiency)
                                                  // must be called ID
    VRP() : FunctionPass(ID) {} 

    // must define a runOnFunction() for any function pass we want to create.    
    // overrides abstract method in FunctionPass class
    // When the pass is invoked on a function, this is where execution starts
    virtual bool runOnFunction(Function &F) {
      unsigned reg_count = 0;
      // the range-based for loop replaces iterators of this kind:
      // for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I)
      for(auto& bb : F) {
	for (auto& inst : bb) {
	  int ops = inst.getNumOperands();
	  for (int i = 0; i < ops; i++) {
	    Value *op = inst.getOperand(i);
	    if (isa<Instruction>(op)) 
	      reg_count++;
	  }
	}
      }
      errs() << F.getName() << " = " << reg_count << "\n";
      
      return false;
    }
  };
}   

char VRP::ID = 0;   // value can be anything, LLVM just looks at the address 



// define a function that will register your pass with the Pass Manager
// you can name the function anything; common form : regsiterFOO or registerFOOPAss
// this function just adds the pass
// can have debugging output
// invoke other passes etc. 
static void registerVRPPass(const PassManagerBuilder &,
 				   legacy::PassManagerBase &passManager) {
  passManager.add(new VRP());  
}


// Pass manager will look for this static class RegisterStandardPasses
// uses the private function RegisterMyPass
static RegisterStandardPasses RegisterMyPass(PassManagerBuilder::EP_EarlyAsPossible,
					     registerVRPPass);



