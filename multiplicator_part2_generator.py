import sys

if len(sys.argv) != 2:
    raise ValueError('Inserire <bit>')

bit = sys.argv[1]

file_name = (f'multiplicator_{bit}.bench')
#formattazione
text_generated = '# multiplicator\n# INPUT'
f = open(file_name, "w")
f.write(text_generated)

#GENERAZIONE INPUT
for i in range(int(bit)):
    text_generated = ('\n'
    f'INPUT(X{i})\n'
    f'INPUT(Y{i})')
    f.write(text_generated)

#formattazione
text_generated = '\n# PRIMA PARTE DEL MOLTIPLICATORE (AND)'
f.write(text_generated)

#PRIMA PARTE DEL MOLTIPLICATORE (AND)
for i in range(int(bit)):
    for j in range(int(bit)):
        text_generated = ('\n'
        f'W{j}{i} = AND(X{j}, Y{i})')
        f.write(text_generated)

# #PRIMO OUTPUT
# text_generated = '\nOUTPUT(W00)'
# f.write(text_generated)

#formattazione
text_generated = '\n# SECONDA PARTE DEL MOLTIPLICATORE (ADDER SHIFTATI IN CASCATA)'
f.write(text_generated)

#SECONDA PARTE DEL MOLTIPLICATORE (ADDER SHIFTATI IN CASCATA)
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
                f'CoL{i}D{j} = AND(W{j}{a}, W{b}{i})\n')
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
                f'CoL{i}D{j} = AND(W{j}{a}, SL{c}D{b})\n')
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

#formattazione
text_generated = '\n# ADDER (DOPO MOLTIPLICATORE)'
f.write(text_generated)

#ADDER (DOPO MOLTIPLICATORE)
#livello
for j in range(2*int(bit)):
    #al primo livello ho una entrata a 0 quindi devo separare
    b=j+1
    d=j-1
    u=int(bit)
    s=j-(u-1)
    if j==0:
        #primo giro ho un halfadder
        f.write(f'\n# HALFADDER RCA BIT {j}')
        text_generated=('\n'
        f'S{j} = XOR(W{0}{j}, R{j})\n'
        f'Co{j} = AND(W{0}{j}, R{j})\n')
        f.write(text_generated)
    else:
        if j<=int(bit)-2:
            f.write(f'\n# FULLADDER RCA BIT {j}')
            text_generated=('\n'
            f'1{j} = XOR(SL{d}D{0}, R{j})\n'
            f'2{j} = AND(SL{d}D{0}, R{j})\n'
            f'3{j} = AND(1{j}, Co{d})\n'
            f'S{j} = XOR(Co{d}, 1{j})\n'
            f'Co{j} = OR(3{j}, 2{j})\n')
            f.write(text_generated)
        else:
            if j!=(2*int(bit)-1):
                f.write(f'\n# FULLADDER RCA INGRESSO BIT {j}')
                text_generated=('\n'
                f'1{j} = XOR(SL{u-2}D{s}, R{j})\n'
                f'2{j} = AND(SL{u-2}D{s}, R{j})\n'
                f'3{j} = AND(1{j}, Co{d})\n'
                f'S{j} = XOR(Co{d}, 1{j})\n'
                f'Co{j} = OR(3{j}, 2{j})\n')
                f.write(text_generated)
            else:
                f.write(f'\n# FULLADDER RCA INGRESSO BIT {j}')
                text_generated=('\n'
                f'1{j} = XOR(CoL{u-2}D{s-1}, R{j})\n'
                # f'2{j} = AND(CoL{u-2}D{s-1}, R{j})\n'
                # f'3{j} = AND(1{j}, Co{d})\n'
                f'S{j} = XOR(Co{d}, 1{j})\n')
                # f'Co{j} = OR(3{j}, 2{j})\n')
                f.write(text_generated)

f.write(f'\n# REGISTRO R DI {2*int(bit)} BIT')
for j in range(2*int(bit)):
    text_generated=('\n'
    f'R{j} = DFF(S{j})\n'
    f'OUTPUT(R{j})\n')
    f.write(text_generated)

# f.write(text_generated)
f.close()
