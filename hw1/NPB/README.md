This folder contains:

	- NPB-OMP - Directory with the parallel version translated from the original NPB version

Each directory is independent and contains its own implemented version of the kernels:

	IS - Integer Sort, random memory access
	EP - Embarrassingly Parallel
	CG - Conjugate Gradient, irregular memory access and communication
	MG - Multi-Grid on a sequence of meshes, long- and short-distance communication, memory intensive
	FT - discrete 3D fast Fourier Transform, all-to-all communication

# How to Compile 

Enter the directory from the version desired and execute:

	make _BENCHMARK CLASS=_VERSION


_BENCHMARKs are: 
		
	EP, CG, MG, IS and FT 
																									
_VERSIONs are: 
	
	Class S: small for quick test purposes
	Class W: workstation size (a 90's workstation; now likely too small)	
	Classes A, B, C: standard test problems; ~4X size increase going from one class to the next	
	Classes D, E, F: large test problems; ~16X size increase from each of the previous Classes  


Command:

	make ep CLASS=B
