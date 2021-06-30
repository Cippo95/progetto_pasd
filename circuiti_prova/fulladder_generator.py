import sys

if len(sys.argv) != 6:
    raise ValueError('Inserire <addendo1> <addendo2> <carryin> <livello> <profondità>')

A = sys.argv[1]
B = sys.argv[2]
C = sys.argv[3]
L = sys.argv[4]
D = sys.argv[5]

text_generated = (f'\n\
1M{L}{D} = XOR({A}, {B})\n\
2M{L}{D} = AND({A}, {B})\n\
3M{L}{D} = AND(1M{L}{D}, {C})\n\
SM{L}{D} = XOR({C}, 1M{L}{D})\n\
CoM{L}{D} = OR(3M{L}{D}, 2M{L}{D}')

file_name = (f'fa_{A}-{B}-{C}-{L}-{D}.txt')
f = open(file_name, "w")
f.write(text_generated)
f.close()