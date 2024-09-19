/*
 *  Simple LibTool that counts the number of functions in the source file
 */
#include "clang/Basic/SourceManager.h"
#include "clang/Driver/Options.h"
#include "clang/AST/AST.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/ASTConsumers.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "clang/Rewrite/Core/Rewriter.h"
#include "llvm/Option/ArgList.h"
#include<fstream>

using namespace std;
using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace llvm;
using namespace llvm::opt;

static llvm::cl::OptionCategory MyToolCategory("Function Analyzer options");

unsigned numFunctions = 0;
unsigned kernel_calls = 0;

const unsigned ATTR_GLOBAL = 101;
const unsigned ATTR_DEVICE = 98;

// Checks if a function has the __global__ or __device__ attribute set (i.e., CUDA)     
bool isCUDAFunc(AttrVec& attrs) {
  for (unsigned int i = 0; i < attrs.size(); i++) {
    Attr this_attr = (*attrs[i]);
    attr::Kind attr_val = this_attr.getKind();
    if (attr_val == ATTR_GLOBAL)
      return true;
    if (attr_val == ATTR_DEVICE)
      return true;
  }
  return false;
}

class KernelArgVisitor : public RecursiveASTVisitor<KernelArgVisitor> {
private:
  ASTContext *astContext; 

public:
  explicit KernelArgVisitor(ASTContext *context) 
    : astContext(context) {}

  virtual bool VisitDeclRefExpr(DeclRefExpr *var_ref) {
    
    ValueDecl* decl = var_ref->getDecl();
    if (decl) {
      string name = decl->getDeclName().getAsString();
      llvm::outs() << "Decl Ref Expr: " << name << "\n";
    }
    return true;
  };

};
/* 
 * The RecursiveASTVisitor: real magic happens here!
 */
class CudaKernelAnalysisVisitor : public RecursiveASTVisitor<CudaKernelAnalysisVisitor> {
private:
  ASTContext *astContext; 
  
public:
  explicit CudaKernelAnalysisVisitor(CompilerInstance *CI) 
      : astContext(&(CI->getASTContext())) {}
  
  virtual bool VisitFunctionDecl(FunctionDecl *func) {
    numFunctions++;
    return true;
  }

  virtual bool VisitMemberExpr(MemberExpr *var_ref) {

    ValueDecl* decl = var_ref->getMemberDecl();
    if (decl) {
      string name = decl->getDeclName().getAsString();
      llvm::outs() << "Member Expr: " << name << "\n";
    }
    return true;
  };

  virtual bool VisitCUDAKernelCallExpr(CUDAKernelCallExpr *kernel_call) {
    FunctionDecl *kernel_decl = dyn_cast<FunctionDecl>(kernel_call->getCalleeDecl());
    string kernel_name = kernel_decl->getQualifiedNameAsString();
    kernel_calls++;
    llvm::outs() << "Call to CUDA kernel: " << kernel_name << "\n";
    KernelArgVisitor *visitor = new KernelArgVisitor(astContext);
    for (CUDAKernelCallExpr::arg_iterator i  = kernel_call->arg_begin(); i < kernel_call->arg_end(); i++) {
      (*i)->dumpColor();
      visitor->TraverseStmt(*i);
    }
    return true;
  }
};


/* 
 * The ASTConsumer: essentially just a wrapper for the Visitors 
 */
class CudaKernelAnalysisASTConsumer : public ASTConsumer {
private:
    CudaKernelAnalysisVisitor *visitor; 

public:

  /* instantiate the visitor and pass the current context */
  explicit CudaKernelAnalysisASTConsumer(CompilerInstance *CI)
    : visitor(new CudaKernelAnalysisVisitor(CI)) { }

  /* override call to HandleTranslationUnit() */
  virtual void HandleTranslationUnit(ASTContext &Context) {
    SourceManager& SM = Context.getSourceManager();
    auto Decls = Context.getTranslationUnitDecl()->decls();
    // do a pre-pass over all decls to count the number of distinct kernels                                     
    for (auto &Decl : Decls) {
      // ignore decls in header files                                                                           
      const auto& FileID = SM.getFileID(Decl->getLocation());
      if (FileID != SM.getMainFileID())
        continue;

      visitor->TraverseDecl(Decl);
    }

  }
};


/* 
 * The FrontEndAction class simply creates an AST Consumer
 *
 * What is the front-end action? 
 *   consume (i.e., process) the AST 
 */
class CudaKernelAnalysisFrontendAction : public ASTFrontendAction {
public:
  virtual std::unique_ptr<ASTConsumer> CreateASTConsumer(clang::CompilerInstance &CI,
							 llvm::StringRef file) {
    return std::unique_ptr<ASTConsumer>(new CudaKernelAnalysisASTConsumer(&CI)); 
  }
};

int main(int argc, const char **argv) {

  // parse the command-line args passed to your code
  CommonOptionsParser op(argc, argv, MyToolCategory);        

  // create a new LibTool instance 
  ClangTool Tool(op.getCompilations(), op.getSourcePathList());

  // run the tool, creating a new FrontendAction
  int result = Tool.run(newFrontendActionFactory<CudaKernelAnalysisFrontendAction>().get());

  // LLVM has it's own I/O
  llvm::outs() << "Number of functions encountered " << numFunctions << "\n";
  llvm::outs() << "Number of kernel calls " << kernel_calls << "\n";
  return result;
}


