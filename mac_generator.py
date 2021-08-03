#qui nel file per python 2.7 metto l'encoding
#sys serve per usare gli argomenti
import sys

#controllo che sia stato dato un argomento che è il numero di bit
if len(sys.argv) != 2:
    raise ValueError("Specifica i bit degli ingressi del circuto come argomento!")

#l'argomento è visto come una stringa quindi lo converto in intero
bit = int(sys.argv[1])

#assegno un nome al file, parametrico coi bit, estensione .bench per essere usato con hope
file_name = (f'mac_{bit}.bench')

#apertura del file in scrittura, non uso il with open perché qui preferisco risparmiare una tabulazione
f = open(file_name, "w")

#scrivo il nome del circuto, cosa che serve ad hope
f.write('# multiply_and_accumulate_unit\n\n# Input\n')

#genero gli input separatamente per avere più ordine nei file generati da hope che dovrò poi manipolare per gli studi statistici, generando gli input con un solo ciclo si mischierebbero
#generazione del input X, chiaro ciclo for parametrico con il numero di bit
for i in range(bit):
    text_generated = ('\n'
    f'INPUT(X{bit-i-1})')
    f.write(text_generated)
#generazione del input Y, chiaro ciclo for parametrico con il numero di bit
for i in range(bit):
    text_generated = ('\n'
    f'INPUT(Y{bit-i-1})')
    f.write(text_generated)

#commento e costruisco la prima parte del moltiplicatore (i vari AND che originano i segnali W) come da documentazione
f.write('\n\n# 1) Prima parte del moltiplicatore: AND che generano i segnali W\n')
#Ogni X va in AND con ogni Y, credo sia ovvio il doppio ciclo for
for i in range(bit):
    for j in range(bit):
        text_generated = ('\n'
        f'W_X{j}Y{i} = AND(X{j}, Y{i})')
        f.write(text_generated)

#commento e costruisco la seconda parte del moltiplicatore (rca in cascata) come da documentazione
f.write('\n\n# 2) Seconda parte del moltiplicatore: cascata di rca shiftati\n')

#distinguo rca per livelli
#i livelli sono 'bit - 1' per come è strutturato il circuito
#la variabile "i" indica il livello
for i in range(bit-1):
    #commento per segnalare i livelli
    f.write(f'\n# RCA LIVELLO {i}:\n')
    #distinguo i bit su cui vado a lavorare
    for j in range(bit):
        #scrivo queste variabili per aiutarmi a gestire la combinazione dei vari segnali che possono essere di un livello o posizione prima o dopo.
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
                #S è l'uscita come da documentazione, per esempio S0
                #L sta per "Level" cioè il livello 
                #D sta per "Depth" cioè profondità, indica la posizione del bit
                #esempio: al livello 0 abbiamo S0, nel file sarà SL0D0
                #esempio: S0 è lo XOR di W01 e W10 -> SL0D0 = W_X0Y1 e W_X1Y0
                f'SL{i}D{j} = XOR(W_X{j}Y{a}, W_X{b}Y{i})\n'
                #"Co" è il Carry-Out, L e D hanno lo stesso significato di prima
                f'CoL{i}D{j} = AND(W_X{j}Y{a}, W_X{b}Y{i})\n')
            #gli altri sono fulladder tranne l'ultimo che ha un ingresso 0 quindi è un halfadder
            else:
                #variabili per risparmiarmi un po' di scrittura, coincidono con gli A e B degli schemi
                A=f'W_X{j}Y{a}'
                B=f'W_X{b}Y{i}'
                #se non è l'ultimo ho dei fulladder
                if j!=bit-1:
                    f.write(f'\n# FULLADDER LIV {i} BIT {j}')
                    text_generated=('\n'
                    #1,2,3 indicano i segnali interni del fulladder, come riportato nei miei schemi
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
                #l'ultimo in questo caso è un halfadder perché l'ultimo fulladder al livello 0 ha un ingresso a 0
                else:
                    f.write(f'\n# Al livello 0 l\'ultimo fulladder avrebbe ingresso 0 quindi metto un halfadder\n# HALFADDER LIV {i} BIT {j}')
                    text_generated=('\n'
                    f'CoL{i}D{j} = AND({A}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, {A})\n')
        #se non sono al primo livello dovrò prendere alcuni segnali dal livello precedente e cambiare qualche condizione
        #Ad esempio un ingresso è il segnale W succesivo mentre l'altro è l'uscita del rca al livello precedente
        else:
            if j==0:
                f.write(f'\n# HALFADDER LIV {i} BIT {j}')
                text_generated=('\n'
                #come si vede qui prendo l'uscita precedente S
                f'SL{i}D{j} = XOR(W_X{j}Y{a}, SL{c}D{b})\n'
                f'CoL{i}D{j} = AND(W_X{j}Y{a}, SL{c}D{b})\n')
            else:
                if j!=bit-1:
                    f.write(f'\n# FULLADDER LIV {i} BIT {j}')
                    A=f'W_X{j}Y{a}'
                    #anche qui uscita precedente S
                    B=f'SL{c}D{b}'
                    text_generated=('\n'
                    f'1L{i}D{j} = XOR({A}, {B})\n'
                    f'2L{i}D{j} = AND({A}, {B})\n'
                    f'3L{i}D{j} = AND(1L{i}D{j}, CoL{i}D{d})\n'
                    f'SL{i}D{j} = XOR(CoL{i}D{d}, 1L{i}D{j})\n'
                    f'CoL{i}D{j} = OR(3L{i}D{j}, 2L{i}D{j})\n')
                else:
                    #se ho l'ultimo full-adder in un livello diverso dal primo prendo il CO dal livello precedente
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
        #R è l'uscita del registro
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
#costruisco il registro
f.write(f'\n# 4) Registro R di {2*bit} bit')
#ovviamente di grandezza 2n
for j in range(2*bit):
    text_generated=('\n'
    #semplicemente prendo le uscite e le metto in un flip flop d
    f'R{j} = DFF(S{j})\n'
    f'OUTPUT(R{2*bit-j-1})')
    f.write(text_generated)
f.close()
