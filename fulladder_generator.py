import sys

if len(sys.argv) != 7:
    raise ValueError('Inserire <addendo1> <addendo2> <somma> <carryout> <livello> <profondità>')

A = sys.argv[1]
B = sys.argv[2]
S = sys.argv[3]
C = sys.argv[4]
L = sys.argv[5]
D = sys.argv[6]

text_generated = (f'{S}M{L}{D} = XOR({A}, {B})\n{C}M{L}{D} = AND({A}, {B})')
file_name = (f'fa_{A}-{B}-{S}-{C}-{L}-{D}.txt')
f = open(file_name, "w")
f.write(text_generated)
f.close()