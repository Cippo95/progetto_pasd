import sys
# import re

if len(sys.argv) != 2:
    raise ValueError("Specifica il file da leggere come argomento!")

#gli argomenti sono stringhe, converto in int
file_name = sys.argv[1]

# Using for loop
count_fault = 0
count_line = 0
print("\nUsing for loop")
 
#apertura del file in lettura 
with open(file_name) as fp:
    for line in fp:
        if 'test' in line:
            if(count_fault!=0 and count_line!=0):
                test_fault_coverage=(count_fault/count_line)*100
                print("counted faults: {}".format(count_fault),
                "\ncounted test vectors: {}".format(count_line),
                "\nfault_detected: {}%".format(test_fault_coverage))
            count_fault = 0
            count_line = 0
            print("\n{}".format(line.strip()))
        else:
            count_line += 1
            if '*' in line:
                count_fault += 1
                print("{}".format(line.strip()))
