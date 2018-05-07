#!/bin/env python2.7
''' This script is an utility for collecting processing Intel PT data and conform to Perflint's raw file format supporting only the vector container.
To be invoked as follows: python <script> <source_code> <container_directory>
Script assumes the standard C++ library location is: /usr/include/c++/5/bits
Generates a directory to keep all the files: tcc/
Overwrites an existing a.out
For containers invokes such as vector<vector<int>>, an illogical result will occur namely vector0<vector1<int>>
Han Liao
kirito@vt.edu
Andrew Cooper
squad3@vt.edu
Kyle Dyess
kdyess97@vt.edu
version=1.0'''
import re
import subprocess
import sys
import os
import time

#Collect relevant data
source_file_name = sys.argv[1]
if len(sys.argv) == 3:
    container_directory = sys.argv[2]
else:
    container_directory = "/usr/include/c++/5"
tcc_directory = "tcc"
modified_file_name = source_file_name.split(".")[0] + "_modified.cc"

#Extract containers and clone source code
vector_regex = re.compile("(vector)(\s*<)")
source_file = open(source_file_name, "r")
modified_file = open(modified_file_name, "w+")
#Irregardless of multiple containers or not; we generate unique functions to map functions back to a container
#We do not handle comments (ie. //vector<int> v) will yield an additional tcc file
source_code = source_file.read()
vectors = re.findall(vector_regex, source_code)
num_vectors = len(vectors)
print("Found " + str(num_vectors) + " vectors")
enumeration = list(range(num_vectors))
modified_source_code = re.sub(vector_regex, lambda match: "vector"+str(enumeration.pop(0))+"<", source_code)
for e in range(num_vectors):
    modified_file.write("#include \""+tcc_directory+"/"+"vector"+str(e)+"\"\n")
modified_file.write(modified_source_code)
modified_file.close()
print("Modified source_code generated: " + modified_file_name)

#Build tcc directory and bits subdirectory
if not os.path.exists(tcc_directory):
        os.makedirs(tcc_directory)
if not os.path.exists(tcc_directory+"/bits"):
        os.makedirs(tcc_directory+"/bits")

print("Begin generating clones")
start = time.time()
keywords = ["vector", "_S_word_bit", "_Bit_reference", "_Bit_iterator", "_GLIBCXX_EXPORT_TEMPLATE", "<bits/stl_vector.h>", "<bits/stl_bvector.h>", "<bits/vector.tcc>", "_Bit_const_iterator"]
header_file = open(container_directory+"/vector", "r")
header_source = header_file.read()
header_file.close()
tcc_file = open(container_directory+"/bits/"+"vector.tcc", "r")
tcc_source = tcc_file.read()
tcc_file.close()
stl_vector_file = open(container_directory+"/bits/"+"stl_vector.h", "r")
stl_vector_source = stl_vector_file.read()
stl_vector_file.close()
stl_bvector_file = open(container_directory+"/bits/"+"stl_bvector.h", "r")
stl_bvector_source = stl_bvector_file.read()
stl_bvector_file.close()
for e in range(num_vectors):
    unique_id = str(e)
    header_source_temp = re.sub(keywords[5], "\"./bits/stl_vector.h\"", header_source)
    header_source_temp = re.sub(keywords[6], "\"./bits/stl_bvector.h\"", header_source_temp)
    header_source_temp = re.sub(keywords[7], "\"./bits/vector.tcc\"", header_source_temp)
    header_source_temp = re.sub(keywords[0], keywords[0]+unique_id, header_source_temp, flags=re.I)
    header_source_temp = re.sub(keywords[4], keywords[4]+unique_id, header_source_temp)
    header_temp = open(tcc_directory+"/"+"vector"+unique_id, "w+")
    header_temp.write(header_source_temp)
    header_temp.close()
    tcc_source_temp = re.sub(keywords[0], "vector"+unique_id, tcc_source, flags=re.I)
    tcc_temp = open(tcc_directory+"/bits/"+"vector"+unique_id+".tcc", "w+")
    tcc_temp.write(tcc_source_temp)
    tcc_temp.close()
    stl_vector_source_temp = re.sub(keywords[0], "vector"+unique_id, stl_vector_source, flags=re.I)
    stl_vector_temp = open(tcc_directory+"/bits/"+"stl_vector"+unique_id+".h", "w+")
    stl_vector_temp.write(stl_vector_source_temp)
    stl_vector_temp.close()
    stl_bvector_source_temp = re.sub(keywords[5], "\"./stl_vector.h\"", stl_bvector_source)
    stl_bvector_source_temp = re.sub(keywords[0], "vector"+unique_id, stl_bvector_source_temp, flags=re.I)
    stl_bvector_source_temp = re.sub(keywords[1], keywords[1]+unique_id, stl_bvector_source_temp)
    stl_bvector_source_temp = re.sub(keywords[2], keywords[2]+unique_id, stl_bvector_source_temp)
    stl_bvector_source_temp = re.sub(keywords[3], keywords[3]+unique_id, stl_bvector_source_temp)
    stl_bvector_source_temp = re.sub(keywords[8], keywords[8]+unique_id, stl_bvector_source_temp)
    stl_bvector_temp = open(tcc_directory+"/bits/"+"stl_bvector"+unique_id+".h", "w+")
    stl_bvector_temp.write(stl_bvector_source_temp)
    stl_bvector_temp.close()
finish = time.time()
print("Done generating clones; took " + str(finish-start) + " seconds")

#Compile everything
result = subprocess.check_output(["g++", source_file_name, "-I",  tcc_directory])
if result == "":
    print("Compilation succeed.")
else:
    print("Compilation failed.")


