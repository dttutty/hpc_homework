# OpenMP Tasking 


## Description

 * understand the use of the OpenMP `task` directive
 * recognize the need for dependence analysis for parallelization


## Outline 

  * [Need for Task Parallelization](#need_for_task_par)
  * [The single Directive](#single_directive)
  * [The task Directive](#task_directive)
  * [Parallelization and Dependence](#dependence)
  
  
## <a name="need_for_task_par"></a>Need for Task Parallelization

Consider the following (meaningless) code that prints the value `19`. 

```C
include<stdio.h>

int main() {
  int i = 17;
  int j = 0;
  int k = 0;

  j++;
  k++;

  printf("result = %d\n", i + j + k);

  return 0;
}
```

The two increment operations of `i` and `j` can be executed in parallel. We can insert the OpenMP
`parallel` directive to try to parallelize that segment of the program. 

```C
#include<stdio.h>
#include<omp.h>

int main() {
  int i = 17;
  int j = 0;
  int k = 0;

  omp_set_num_threads(2);

  #pragma omp parallel
  {
    j++;
    k++;
  }

  printf("result = %d\n", i + j + k);

  return 0;
}
```

We are parallelizing the code using two threads. We have included `omp.h` for the call to
`omp_set_num_threads()`. Let's compile and run this code. 

```bash
(knuth)% g++ -o inc inc1.c -fopenmp 
```

_What is the expected output?_

```bash
(knuth)% ./inc 
result = 21
(knuth)% ./inc 
result = 21
```

_Can you explain why we are getting `21`?_

Recall how the `parallel` directive works. 

  * the pragma marks a _parallel_ region in the program
  * at runtime OpenMP creates _n_ threads where _n_ is determined from the environment
  * each thread executes each statement in the block in parallel (i.e., an instance of block is
    executed _n_ times) 


## <a name="single_directive"></a>The `single` Directive 

The `parallel` directive is not suitable for the type of task parallelization we want for this
program. OpenMP provides the `task` directive which will allow us to execute the two instructions
in parallel. The `task` directive is often used in combination with the `single` pragma. The
`single` pragma tells OpenMP to execute the statements in the block using a single thread. 

```C
  omp_set_num_threads(2);
  #pragma omp parallel
  {
    #pragma omp single
    {
        printf("Thread %d incrementing\n", omp_get_thread_num());
        j++;
        printf("Thread %d incrementing\n", omp_get_thread_num());
        k++;
    }
  }
```

If we compile and run this code, we should get the expected behavior. 

```bash
(knuth)% g++ -o inc inc2.c -fopenmp 
(knuth)% ./inc 
Thread 0 incrementing
Thread 0 incrementing
result = 19
(knuth)% ./inc 
Thread 0 incrementing
Thread 0 incrementing
result = 19
```

## <a name="task_directive"></a>The `task` Directive 

Although we are getting the correct results now, we have essentially made this a sequential
program. To run the two statements inside the `single` block in parallel, we can introduce the
`task` directive. 

```C
int main() {
  int i = 17;
  int j = 0;
  int k = 0;

  omp_set_num_threads(2);
  #pragma omp parallel
  {
    #pragma omp single
    {
      #pragma omp task
      {
        printf("Thread %d incrementing\n", omp_get_thread_num());
        j++;
      }
      #pragma omp task
      {
        printf("Thread %d incrementing\n", omp_get_thread_num());
        k++;
      }
    }
  }

  printf("result = %d\n", i + j + k);
```

In this version of the code, when we enter the `single` block, only one thread is operational. But
when we counter the task directive, a new task is created which is either executed by the _current_
thread or a different thread in the team. While the thread is executing the first task, execution of
other statements in the block can move forward. When we hit the second `task` construct, another
task is created, and executed by the either the thread that was assigned to the first task (if it
has already finished) or a different thread from the team. 


## <a name="dependence"></a>Parallelization and Dependence

Let's look at another program that produces the same output in a slightly different way. 

```C
#include<stdio.h>

int main() {

  int i = 17;
  int j = 0;
  int k = 0;

  j = i + 1;
  k = j + 1;

  printf("k = %d\n", k);

  return 0;
}
```

We are incrementing `i` and storing the result in `j` and then incrementing `j` and storing the
result in `k`. Therefore, effectively `i` is incremented twice. 

```bash
(knuth)% g++ -o inc dep_inc0.c -fopenmp 
(knuth)% ./inc 
k = 19
```

We can follow the template from the previous example and task parallelize this code with `parallel`, `single` and
`task` directives. 

```C
int main() {

  int i = 17;
  int j = 0;
  int k = 0;

  #pragma omp parallel
  {
    #pragma omp single
    {
      #pragma omp task
      j = i + 1;

      #pragma omp task
      k = j + 1;
    }
  }

  printf("result = %d\n", k);
```

Now let's run it to make sure we have parallelized correctly. 

```bash
(knuth)% g++ -o inc dep_inc1.c -fopenmp 
(knuth)% ./inc 
result = 19
(knuth)% ./inc 
result = 19
(knuth)% ./inc 
result = 19
(knuth)% ./inc 
result = 1
(knuth)% ./inc 
result = 19
(knuth)% ./inc 
result = 19
```

_What happened?_

The two increment statements in this program cannot be safely parallelized! The second statement
_depends_ on the value produced by the first statement. Another way to phrase this is to say, there is a
_dependence_ from the first increment to the second increment statement. This is the _casual_
definition of dependence. 

Before the compiler can perform any kind of parallelization or apply a _reordering transformation_
(e.g., to increase ILP),  it needs to determine if the statements involved can be executed independently
without violating program semantics. This type of analysis is known as dependence analysis. 
