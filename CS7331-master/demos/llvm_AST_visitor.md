## LLVM AST Manipulation with RecursiveASTVisitors 

### Description

This tutorial introduces the RecursiveASTVisitor class in LLVM. A convenient tool for AST
manipulation. We do a step-by-step walk-through of how the RecursiveASTVisitor can be used to write
a LibTool that gathers attributes from each function defined in a C++ source file. 

The tutorial builds on the following introductory LibTool tutorial. 

   * [LibTooling from Scratch](https://git.txstate.edu/aq10/CS7331/blob/master/demos/llvm_libtool.md)


### Outline 

  * [LibtTools with pre-defined FrontEndAction](#basic_template)
  * [Defining our own FrontEndAction](#frontend)
  * [The ASTConsumer](#ASTConsumer)
  * [Visitors](#visitors)
  * [ASTContext](#context)
  * [Doing more with Visitors](#extending)
  
  
### <a name="basic_template"></a>[LibtTools with pre-defined FrontEndAction]


As we discussed in [LibTooling from
Scratch](https://git.txstate.edu/aq10/CS7331/blob/master/demos/llvm_libtool.md), creating a LibTool
with one of the pre-defined front-end actions is exceedingly simple. 

```C++
/*                                                                                            
 *  The simplest LibTool                                                                      
 */

#include "clang/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"

using namespace std;
using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace llvm;

static cl::OptionCategory MyToolCategory("Syntax-checker options");

int main(int argc, const char **argv) {

  // parse command-line args passed to your code                                              
  CommonOptionsParser op(argc, argv, MyToolCategory);

  // create a new LibTooling instance                                                         
  ClangTool Tool(op.getCompilations(), op.getSourcePathList());

  // run the LibTool                                                                          
  // the tool creates a new FrontEndAction that just checks the syntax of the input file      
  // need the return value to send to LLVM                                                    
  int result = Tool.run(newFrontendActionFactory<SyntaxOnlyAction>().get());

  llvm::outs() << "Syntax checking successful!\n";

  // send result to LLVM                                                                      
  return result;
}
```

All we need to do is to create the _Tool_ and then _run_ it with action we want performed. LibTools
with pre-defined actions are not that interesting, however. Generally, we want to be able to define
our own _FrontEndActions_. This process is a little more involved. 


### <a name="frontend"></a>Creating our own front-end actions

To create a front-end action, we need to define a `FrontEndAction` class which extends
`ASTFrontEndAction.` 

```C
class FuncAnalysisFrontendAction : public ASTFrontendAction {
public:
  virtual std::unique_ptr<ASTConsumer> CreateASTConsumer(clang::CompilerInstance &CI,
							 llvm::StringRef file) {
    return std::unique_ptr<ASTConsumer>(new FuncAnalysisASTConsumer(&CI)); 
  }
};
```

For front-end actions that manipulate the AST, in many cases, all that is needed is creating an
_ASTConsumer_. This tells LLVM that the front-end action is going to read the AST, and possibly
modify it. 

### <a name="ASTConsumer"></a>The ASTConsumer


```C
class FuncAnalysisASTConsumer : public ASTConsumer {
private:
    FuncAnalysisVisitor *visitor; 

public:

  /* instantiate the visitor and pass the current context */
  explicit FuncAnalysisASTConsumer(CompilerInstance *CI)
    : visitor(new FuncAnalysisVisitor(CI)) { }

  /* override call to HandleTranslationUnit() */
  virtual void HandleTranslationUnit(ASTContext &Context) {

    /* TranslationUnit represents the entire source file (input to our tool)
       We can use ASTContext to create a handle for the unit in our Tool
       The entire source can be represented with a top-level decl 
    */
    visitor->TraverseDecl(Context.getTranslationUnitDecl());
  }
};
```

The ASTConsumer class is also fairly straightforward. Essentially it serves as a wrapper for the
_Visitors_. In most cases, the ASTConsumer will do two things (i) instantiate the Visitors and (ii)
provide the starting location of the traversal. For the second task, we provide a definition of the 
`HandleTranslationUnit()` virtual function. In this example, we are telling LLVM to start the
traversal at the top-level _Decl_ in the input source file. 


### <a name="visitors"></a>Visitors

We can now define our visitor classes to perform the AST tasks. It's in these visitors where all the
magic happens! 

```C

unsigned numFunctions = 0;
/* 
 * The RecursiveASTVisitor: real magic happens here!
 */
class FuncAnalysisVisitor : public RecursiveASTVisitor<FuncAnalysisVisitor> {
private:
  ASTContext *astContext; 
  
public:
  explicit FuncAnalysisVisitor(CompilerInstance *CI) 
      : astContext(&(CI->getASTContext())) {}
  
  virtual bool VisitFunctionDecl(FunctionDecl *func) {
    numFunctions++;
	return true;
  }
  
};
```

We can define multiple visitors in the same RecursiveASTVisitor class. In this example, we define a
FunctionDecl visitor which will visit each function declaration in the scope defined by the
`HandleTransLationUnit()` in _ASTConsumer_. Here, all we want our very simple visitor to do is just
count the number of function definitions. We declare a global variables, `numFunctions` to hold the
count. It is not uncommon in LLVM to include global variables when doing accounting tasks on
a given source input. 

We can write visitors to visit almost any type of node in the Clang AST. 


### <a name="context"></a>ASTContext 

The _ASTContext_ class holds information about the source file that is not available within the
AST. For example, it can give us the line number for a particular AST construct. The context is
embedded inside what LLVM calls a _CompilerInstance_. We want to pass the _ASTContext_ to the top-level
_FrontEndAction_ class, which in turn passes it to the _ASTConsumer_ which in turn passes it to the
_RecursiveASTVisitor_. 

Let's build and run the LibTool which counts the number of function declarations. 

```
(minksy)% cd $LLVM_BUILD
(minksy)% make
(minksy)% push ~/cs7331/llvm
(minksy)% func-analyzer cg.cpp -- -I$HOME/CS7331.git/NPB/CG -I$HOME/CS7331.git/NPB/common
Number of functions encountered 4033
```

**What happened**?

The _translation unit_ includes the source C++ file plus all the expanded headers. Our LibTool is
counting function declaration in all header files included in `cg.cpp`. We can use the
ASTContext to narrow the scope of analysis to the AST that represents just the input source file. 


```C++
virtual void HandleTranslationUnit(ASTContext &Context) {
  /* TranslationUnit represents the entire source file (and all expanded headers)
     We can iterate through top-level decls and just select the ones that appear 
     in the main source file 
   */
  SourceManager& SM = Context.getSourceManager();
  auto Decls = Context.getTranslationUnitDecl()->decls();
  for (auto &Decl : Decls) {
    const auto& FileID = SM.getFileID(Decl->getLocation());
	if (FileID != SM.getMainFileID())
	   continue;
    visitor->TraverseDecl(Decl);
  }
}
```

The _ASTContext_ includes a _SourceManager_ which keeps track of file and line information. We can write
an iterator that goes through each _Decl_ in the translation unit and picks only those that appear
in the source file itself. 

### <a name="extending"></a>Doing more with Visitors 

We can extend our _FunDeclVisitor_ to extract a wide array of information about the functions defined in the
source file. 

```C++
virtual bool VisitFunctionDecl(FunctionDecl *func) {
  string funcName = func->getQualifiedNameAsString();
  llvm::outs() << "Function name: " << funcName << "\n";
  numFunctions++;
  return true;
}
```

The Clang API is indexed by Google. So just typing `clang _Name_Of_Class_` should take you directly
to the functions API. The _FunDecl_ class is derived from _NamedDecl_. Each _NamedDecl_ construct
has a name. We can extract that name using `getQualifiedNameAsString()` and print it
out. 




















