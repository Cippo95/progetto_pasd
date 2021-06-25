import sys

if len(sys.argv) != 2:
    raise ValueError('Inserire <bit>')

bit = sys.argv[1]

file_name = (f'multiplicator_{bit}.txt')
#formattazione
text_generated = '# multiplicator\n# INPUT'
f = open(file_name, "a")
f.write(text_generated)

#GENERAZIONE INPUT
for i in range(int(bit)):
    text_generated = ('\n'
    f'INPUT(X{i})\n'
    f'INPUT(Y{i})')
    f.write(text_generated)

#formattazione
text_generated = '\n# PRIMA PARTE DEL CIRCUITO'
f.write(text_generated)

#PRIMA PARTE DEL CIRCUITO
for i in range(int(bit)):
    for j in range(int(bit)):
        text_generated = ('\n'
        f'W{j}{i} = AND(X{j}, Y{i})')
        f.write(text_generated)

#PRIMO OUTPUT
text_generated = '\nOUTPUT(W00)'
f.write(text_generated)

#formattazione
text_generated = '\n# SECONDA PARTE DEL CIRCUITO'
f.write(text_generated)

#SECONDA PARTE DEL CIRCUITO
#livello
for i in range(int(bit)-1):
    #numero bit
    for j in range(int(bit)):
        #al primo livello ho una entrata a 0 quindi devo separare
        a=i+1
        b=j+1
        c=i-1
        d=j-1
        if i==0:
            if j==0:
                #primo giro ho un halfadder
                f.write(f'\n# HALFADDER LIVELLO {i} BIT {j}')
                text_generated=('\n'
                f'SL{i}D{j} = XOR(W{j}{a}, W{b}{i})\n'
                f'CoL{i}D{j} = AND(W{j}{a}, W{b}{i})\n'
                f'OUTPUT(SL{i}D{j})\n')
            else:
                #per ora lascio W40 o quello che è da correggere!
                A=f'W{j}{a}'
                B=f'W{b}{i}'
                if j!=int(bit)-1:
                    f.write(f'\n# FULLADDER LIVELLO {i} BIT {j}')
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
                else:
                    f.write(f'\n# INGRESSO 0 QUINDI HALFADDER LIVELLO {i} BIT {j}')
                    text_generated=('\n'
                    f'CoL{i}D{j} = AND({A}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, {A})\n')
        else:
            if j==0:
                #primo giro ho un halfadder
                f.write(f'\n# HALFADDER LIVELLO {i} BIT {j}')
                text_generated=('\n'
                f'SL{i}D{j} = XOR(W{j}{a}, SL{c}D{b})\n'
                f'CoL{i}D{j} = AND(W{j}{a}, SL{c}D{b})\n'
                f'OUTPUT(SL{i}D{j})\n')
            else:
                if j!=int(bit)-1:
                    f.write(f'\n# FULLADDER LIVELLO {i} BIT {j}')
                    A=f'W{j}{a}'
                    B=f'SL{c}D{b}'
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
                else:
                    f.write(f'\n# FULLADDER LIVELLO {i} BIT {j}')
                    A=f'W{j}{a}'
                    B=f'CoL{c}D{j}'
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
        f.write(text_generated)


# f.write(text_generated)
f.close()
