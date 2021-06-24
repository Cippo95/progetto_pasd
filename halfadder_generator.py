import sys

if len(sys.argv) != 6:
    raise ValueError('Inserire <addendo1> <addendo2> <somma> <carryout> <livello>')

A = sys.argv[1]
B = sys.argv[2]
S = sys.argv[3]
C = sys.argv[4]
L = sys.argv[5]

text_generated = (f'{S}M{L} = XOR({A}, {B})\n{C}M{L} = AND({A}, {B})')
file_name = (f'ha_{A}-{B}-{S}-{C}-{L}.txt')
f = open(file_name, "w")
f.write(text_generated)
f.close()