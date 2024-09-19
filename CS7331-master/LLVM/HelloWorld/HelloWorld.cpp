/*
 *  The simplest LibTool 
 */

#include "clang/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"

/* 
 * namespaces (leave out if you would rather qualify names)
 */
using namespace std;
using namespace clang;
using namespace clang::tooling;
using namespace llvm;

static cl::OptionCategory MyToolCategory("NAME_OF_TOOL options");

int main(int argc, const char **argv) {

  // parse command-line args passed to your code
  CommonOptionsParser op(argc, argv, MyToolCategory);        

  // create a new LibTooling instance 
  ClangTool Tool(op.getCompilations(), op.getSourcePathList());

  // run the LibTool
  // the tool creates a new FrontEndAction
  // that just checks the syntax of the input file
  // need the return value to send to LLVM
  int result = Tool.run(newFrontendActionFactory<NAME_OF_ACTION>().get());
  
  // send result to LLVM
  return result;
}


