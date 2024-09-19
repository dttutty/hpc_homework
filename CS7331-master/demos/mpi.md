## Running MPI on your own cluster 


### Description

This tutorial shows how to set up your own cluster and run MPI programs. 


### Outline 

  * [Setting up your own cluster](#cluster_setup)
  * [Checking MPI installation](#mpi_install)
  * [MPI Hello World](#hello_world)
  * [Building and Running](#build)

### <a name="cluster_setup">Setting up your own cluster</a>

It's fairly easy to set-up your own Beowulf cluster. All you need is access to two or more
desktop/systems running Linux. There are four main steps to setting up the cluster 

   1. **Connectivity:** make sure the systems are on the same network and have ssh connectivity
   2. **Password-less ssh:** MPI users must be able to connect to the nodes in the cluster without having
     to type in their password. 
   3. **NFS mount:** the nodes must be able to share files between them. 
   4. **Consistent MPI installation:** Ensure that the same version of MPI is installed on all nodes. 

The above steps are outlined in at the following GeekforGeeks tutorial. 

  [Creating an MPI Cluster](https://www.geeksforgeeks.org/creating-an-mpi-cluster/)

You can follow the instructions in that tutorial with with the following notes. 

   * **Host name**: if you are setting up your cluster on a network where the machines are already
   named then you will be not be able to re-name them in /etc/hosts. You can just use the
   pre-defined hostnames or use IP address in your MPI host file 
   
   * **MPI user**: if there are more than one user on your cluster then it is better to give access
     to individual users rather than creating a new mpi user. 
	 
      
### <a name="mpi_install">Checking MPI installation</a>
	  
Just like OpenMP, it's now common to have integrated MPI installation with GCC and LLVM. Check the
MPI installation on your system. 

    mpicc --version 
	
Check library and header locations. 

    which mpicc
    whereis mpicc

If you have MPICH installed then you should find it in under `/opt`

    which mpicc
    whereis mpicc
    opt/mpich2/gnu/bin/mpicc

Check the MPI runtime version. 

    mpiexec --version
    /opt/mpich2/gnu/bin/mpiexec --version

Multiple versions of MPI may be installed on the same cluster. Cannot mix build and execute. Default
mpiexec must be same on all compute nodes.


If MPI not installed, you can use `apt-get` to install it. 

    sudo apt-get install libopenmpi-dev
    sudo apt-get install libmpich-dev


Download and installation instruction for MPICH can be found at the following sties. 

   * [MPICH](http://www.mpich.org/downloads/)
   * [OpenMPI](https://www.open-mpi.org/software/ompi/v3.0)


## <a name="hello_world">MPI Hello World</a>

Below is an example of the minimal Hello World program in MPI

```C

#include<mpi.h>
#include<stdio.h>

int main(int argc, char** argv) {

  // initialize the environment 
  MPI_Init(NULL, NULL);
  
  // get total number of processes 
  int world_size = MPI_Comm_size(MPI_COMM_WORLD, &world_size);

  // get the process ID for _this_ node 
  int world_rank = MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);


  // get host name 
  char processor_name[MPI_MAX_PROCESSOR_NAME];
  int name_len;
  MPI_Get_processor_name(processor_name, &name_len);

  // print identifying message 
  printf("Hello world from processor %s, rank %d out of %d processors\n",
         processor_name, world_rank, world_size);
	
  // clean-up 	
  MPI_Finalize();
}
```


### <a href="build">Building and running</a>

We can compile the code with an MPI compiler. 

    mpicc -o mpi_hello_world mpi_hello_world.c
	
To execute the program we need to run it inside the MPI environment. Note the program can execute
as a standalone but then we won't see any MPI behavior. 

    mpirun ./mpi_hello_world

To specify the number of processes, we can use the `-np` flag. 

    mpirun -np 2 ./mpi_hello_world

To specify which nodes we want the program to run on we can use command-line flag `host` or create a
host file. 

    mpirun -host minksy,shadowfax ./mpi_hello_world


