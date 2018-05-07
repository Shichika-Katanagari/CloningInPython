# CloningInPython
Ever want to clone std::vector for a very small yet nontrivial use case. Well here's my attempt.

''' This script is an utility for cloning and compiling C++ programs with enumerated vector classes.
To be invoked as follows: python <script> <source_code> <container_directory>
Script assumes the standard C++ library location is: /usr/include/c++/5/bits
Generates a directory to keep all the files: tcc/
Overwrites existing a.out
For containers invokes such as vector<vector<int>>, an illogical result will occur namely vector0<vector1<int>>
Han Liao
kirito@vt.edu
Andrew Cooper
squad3@vt.edu
Kyle Dyess
kdyess97@vt.edu
version=1.0'''
