import sys

if len(sys.argv) != 2:
    raise ValueError("Specifica i bit come argomento!")

#gli argomenti sono stringhe, converto in int
bit = int(sys.argv[1])

#assegno un nome al file parametrico coi bit, estensione .bench per essere usato con hope
file_name = (f'multiplicator_{bit}.bench')

#apertura del file in scrittura
f = open(file_name, "w")

#scrivo il nome del circuto, serve ad hope
f.write('# multiplicator\n\n# Input\n')

#generazione degli input
for i in range(bit):
    text_generated = ('\n'
    f'INPUT(X{i})\n'
    f'INPUT(Y{i})')
    f.write(text_generated)

#commento e costruisco la prima parte del moltiplicatore (i vari and) come da documentazione
f.write('\n\n# 1) Prima parte del moltiplicatore: AND che generano i segnali W\n')
for i in range(bit):
    for j in range(bit):
        text_generated = ('\n'
        f'W_X{j}Y{i} = AND(X{j}, Y{i})')
        f.write(text_generated)

#commento e costruisco la seconda parte del moltiplicatore (rca in cascata) come da documentazione
f.write('\n\n# 2) Seconda parte del moltiplicatore: cascata di rca shiftati\n')

#distinguo rca in livelli, intuitivo guardando la documentazione, livelli sono 'bit - 1'
for i in range(bit-1):
    f.write(f'\n# RCA LIVELLO {i}:\n')
    #distinguo i bit su cui vado a lavorare
    for j in range(bit):
        #scrivo queste variabili per aiutarmi, so che può non piacere avere variabili letterali ma credo sia intuitivo il significato
        a=i+1
        b=j+1
        c=i-1
        d=j-1
        #se sono al primo livello:
        if i==0:
            #al primo bit ho un halfadder perché non ho carry in (uguale a 0 in figura)
            if j==0:
                f.write(f'\n# HALFADDER LIV {i} BIT {j}')
                text_generated=('\n'
                f'SL{i}D{j} = XOR(W_X{j}Y{a}, W_X{b}Y{i})\n'
                f'CoL{i}D{j} = AND(W_X{j}Y{a}, W_X{b}Y{i})\n')
            #gli altri sono fulladder tranne l'ultimo che ha un ingresso 0 quindi è un halfadder
            else:
                #variabili per collegare i segnali W
                A=f'W_X{j}Y{a}'
                B=f'W_X{b}Y{i}'
                if j!=bit-1:
                    f.write(f'\n# FULLADDER LIV {i} BIT {j}')
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
                #l'ultimo in questo caso è un halfadder
                else:
                    f.write(f'\n# Al livello 0 l\'ultimo fulladder avrebbe ingresso 0 quindi metto un halfadder\n# HALFADDER LIV {i} BIT {j}')
                    text_generated=('\n'
                    f'CoL{i}D{j} = AND({A}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, {A})\n')
        #se non sono al primo livello cambio alcuni segnali e condizioni, intuitivo da documentazione
        else:
            if j==0:
                f.write(f'\n# HALFADDER LIV {i} BIT {j}')
                text_generated=('\n'
                f'SL{i}D{j} = XOR(W_X{j}Y{a}, SL{c}D{b})\n'
                f'CoL{i}D{j} = AND(W_X{j}Y{a}, SL{c}D{b})\n')
            else:
                if j!=bit-1:
                    f.write(f'\n# FULLADDER LIV {i} BIT {j}')
                    A=f'W_X{j}Y{a}'
                    B=f'SL{c}D{b}'
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
                else:
                    f.write(f'\n# FULLADDER LIV {i} BIT {j}')
                    A=f'W_X{j}Y{a}'
                    B=f'CoL{c}D{j}'
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
        f.write(text_generated)

#commento file e costruisco il ripple carry adder
f.write('\n# 3) Ripple carry adder in cascata al moltiplicatore\n')
#avrò un halfadder o fulladder per bit (che ora sono il il doppio gli input)
for j in range(2*bit):
    b=j+1
    d=j-1
    #s serve per collegare gli output del rca all'ultimo livello del moltiplicatore
    s=j-(bit-1)
    if j==0:
        #al primo bit ho un halfadder che va a sommare W00 e il primo bit del registro
        f.write(f'\n# HALFADDER RCA BIT {j}')
        text_generated=('\n'
        f'S{j} = XOR(W_X{0}Y{0}, R{j})\n'
        f'Co{j} = AND(W_X{0}Y{0}, R{j})\n')
        f.write(text_generated)
    else:
        # i successivi devo prendere i bit a 0 dei livelli precedenti l'ultimo
        # qui j = 1 indica il primo livello, j=2 il secondo e così via, per questo i livelli sono bit-1 (invece che bit-2)
        if j<bit-1:
            f.write(f'\n# FULLADDER RCA BIT {j} (Livello precedente)')
            text_generated=('\n'
            f'1{j} = XOR(SL{d}D{0}, R{j})\n'
            f'2{j} = AND(SL{d}D{0}, R{j})\n'
            f'3{j} = AND(1{j}, Co{d})\n'
            f'S{j} = XOR(Co{d}, 1{j})\n'
            f'Co{j} = OR(3{j}, 2{j})\n')
            f.write(text_generated)
        else:
            #qui prendo le uscite dell'ultimo rca nel moltiplicatore 
            if j!=(2*bit-1):
                f.write(f'\n# FULLADDER RCA INGRESSO BIT {j} (Ultimo livello)')
                text_generated=('\n'
                f'1{j} = XOR(SL{bit-2}D{s}, R{j})\n'
                f'2{j} = AND(SL{bit-2}D{s}, R{j})\n'
                f'3{j} = AND(1{j}, Co{d})\n'
                f'S{j} = XOR(Co{d}, 1{j})\n'
                f'Co{j} = OR(3{j}, 2{j})\n')
                f.write(text_generated)
            else:
                #l'ultimo però avrebbe un carry out floating quindi lo faccio diventare un halfadder
                f.write(f'\n# Visto che il carry out sarebbe floating metto un halfadder\n# HALFADDER RCA INGRESSO BIT {j}')
                text_generated=('\n'
                f'1{j} = XOR(CoL{bit-2}D{s-1}, R{j})\n'
                # f'2{j} = AND(CoL{u-2}D{s-1}, R{j})\n'
                # f'3{j} = AND(1{j}, Co{d})\n'
                f'S{j} = XOR(Co{d}, 1{j})\n')
                # f'Co{j} = OR(3{j}, 2{j})\n')
                f.write(text_generated)

f.write(f'\n# 4) Registro R di {2*bit} bit')
for j in range(2*bit):
    text_generated=('\n'
    f'R{j} = DFF(S{j})\n'
    f'OUTPUT(R{j})')
    f.write(text_generated)
f.close()
