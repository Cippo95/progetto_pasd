import sys

if len(sys.argv) != 2:
    raise ValueError('Inserire <bit>')

bit = sys.argv[1]

file_name = (f'rca_{bit}.bench')
#formattazione
text_generated = '# ripplecarryadder\n# INPUT'
f = open(file_name, "a")
f.write(text_generated)

#GENERAZIONE INPUT
for i in range(int(bit)):
    text_generated = ('\n'
    f'INPUT(X{i})\n'
    f'INPUT(Y{i})')
    f.write(text_generated)

#SECONDA PARTE DEL CIRCUITO
#livello
for j in range(int(bit)):
    #al primo livello ho una entrata a 0 quindi devo separare
    b=j+1
    d=j-1
    if j==0:
        #primo giro ho un halfadder
        f.write(f'\n# HALFADDER BIT {j}')
        text_generated=('\n'
        f'S{j} = XOR(X{j}, Y{j})\n'
        f'Co{j} = AND(X{j}, Y{j})\n'
        f'OUTPUT(S{j})\n')
        f.write(text_generated)
    else:
        f.write(f'\n# FULLADDER BIT {j}')
        text_generated=('\n'
        f'1{j} = XOR(X{j}, Y{j})\n'
        f'2{j} = AND(X{j}, Y{j})\n'
        f'3{j} = AND(1{j}, Co{d})\n'
        f'S{j} = XOR(Co{d}, 1{j})\n'
        f'Co{j} = OR(3{j}, 2{j})\n'
        f'OUTPUT(S{j})\n')
        f.write(text_generated)
f.close()
