# coding=utf-8
#sys serve per usare gli argomenti
import sys

#controllo che sia stato dato un argomento che è il numero di bit
if len(sys.argv) != 2:
    raise ValueError("Specifica i bit degli ingressi del circuto come argomento!")

#l'argomento è visto come una stringa quindi lo converto in intero
bit = int(sys.argv[1])

#assegno un nome al file, parametrico coi bit, estensione .bench per essere usato con hope
file_name = ('mac_{}.bench'.format(bit))

#apertura del file in scrittura
f = open(file_name, "w")

#scrivo il nome del circuto, cosa che serve ad hope
f.write('# multiply_and_accumulate_unit\n\n# Input\n')

#genero gli input separatamente per avere più ordine nei file generati da hope che dovrò poi manipolare per gli studi statistici, generando gli input con un solo ciclo si mischierebbero
#generazione del input X, chiaro ciclo for parametrico con il numero di bit
for i in range(bit):
    text_generated = ('\n'
    'INPUT(X{})'.format(bit-i-1))
    f.write(text_generated)
#generazione del input Y, chiaro ciclo for parametrico con il numero di bit
for i in range(bit):
    text_generated = ('\n'
    'INPUT(Y{})'.format(bit-i-1))
    f.write(text_generated)

#commento e costruisco la prima parte del moltiplicatore (i vari AND che originano i segnali W) come da documentazione
f.write('\n\n# 1) Prima parte del moltiplicatore: AND che generano i segnali W\n')
#Ogni X va in AND con ogni Y, credo sia ovvio il doppio ciclo for
for i in range(bit):
    for j in range(bit):
        text_generated = ('\n'
        'W_X{}Y{} = AND(X{}, Y{})'.format(j,i,j,i))
        f.write(text_generated)

#commento e costruisco la seconda parte del moltiplicatore (rca in cascata) come da documentazione
f.write('\n\n# 2) Seconda parte del moltiplicatore: cascata di rca shiftati\n')

#distinguo rca per livelli
#i livelli sono 'bit - 1' per come è strutturato il circuito
#la variabile "i" indica il livello
for i in range(bit-1):
    #commento per segnalare i livelli
    f.write('\n# RCA LIVELLO {}:\n'.format(i))
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
                f.write('\n# HALFADDER LIV {} BIT {}'.format(i,j))
                text_generated=('\n'
                #S è l'uscita come da documentazione, per esempio S0
                #L sta per "Level" cioè il livello 
                #D sta per "Depth" cioè profondità, indica la posizione del bit
                #esempio: al livello 0 abbiamo S0, nel file sarà SL0D0
                #esempio: S0 è lo XOR di W01 e W10 -> SL0D0 = W_X0Y1 e W_X1Y0
                'SL{}D{} = XOR(W_X{}Y{}, W_X{}Y{})\n'.format(i,j,j,a,b,i)+
                #"Co" è il Carry-Out, L e D hanno lo stesso significato di prima
		'CoL{}D{} = AND(W_X{}Y{}, W_X{}Y{})\n'.format(i,j,j,a,b,i))
            #gli altri sono fulladder tranne l'ultimo che ha un ingresso 0 quindi è un halfadder
            else:
                #variabili per risparmiarmi un po' di scrittura, coincidono con gli A e B degli schemi
                A='W_X{}Y{}'.format(j,a)
                B='W_X{}Y{}'.format(b,i)
                #se non è l'ultimo ho dei fulladder
                if j!=bit-1:
                    f.write('\n# FULLADDER LIV {} BIT {}'.format(i,j))
                    text_generated=('\n'
                    #1,2,3 indicano i segnali interni del fulladder, come riportato nei miei schemi
                    '1L{}D{} = XOR({}, {})\n'.format(i,j,A,B)+
                    '2L{}D{} = AND({}, {})\n'.format(i,j,A,B)+
                    '3L{}D{} = AND(1L{}D{}, CoL{}D{})\n'.format(i,j,i,j,i,d)+
                    'SL{}D{} = XOR(CoL{}D{}, 1L{}D{})\n'.format(i,j,i,d,i,j)+
                    'CoL{}D{} = OR(3L{}D{}, 2L{}D{})\n'.format(i,j,i,j,i,j))
                #l'ultimo in questo caso è un halfadder perché l'ultimo fulladder al livello 0 ha un ingresso a 0
                else:
                    f.write('\n# Al livello 0 l\'ultimo fulladder avrebbe ingresso 0 quindi metto un halfadder\n# HALFADDER LIV {} BIT {}'.format(i,j))
                    text_generated=('\n'
                    'CoL{}D{} = AND({}, CoL{}D{})\n'.format(i,j,A,i,d)+
                    'SL{}D{} = XOR(CoL{}D{}, {})\n'.format(i,j,i,d,A))
        #se non sono al primo livello dovrò prendere alcuni segnali dal livello precedente e cambiare qualche condizione
        #Ad esempio un ingresso è il segnale W succesivo mentre l'altro è l'uscita del rca al livello precedente
        else:
            if j==0:
                f.write('\n# HALFADDER LIV {} BIT {}'.format(i,j))
                text_generated=('\n'
                #come si vede qui prendo l'uscita precedente S
                'SL{}D{} = XOR(W_X{}Y{}, SL{}D{})\n'.format(i,j,j,a,c,b)+
                'CoL{}D{} = AND(W_X{}Y{}, SL{}D{})\n'.format(i,j,j,a,c,b))
            else:
                if j!=bit-1:
                    f.write('\n# FULLADDER LIV {} BIT {}'.format(i,j))
                    A='W_X{}Y{}'.format(j,a)
                    #anche qui uscita precedente S
                    B='SL{}D{}'.format(c,b)
                    text_generated=('\n'
                    '1L{}D{} = XOR({}, {})\n'.format(i,j,A,B)+
                    '2L{}D{} = AND({}, {})\n'.format(i,j,A,B)+
                    '3L{}D{} = AND(1L{}D{}, CoL{}D{})\n'.format(i,j,i,j,i,d)+
                    'SL{}D{} = XOR(CoL{}D{}, 1L{}D{})\n'.format(i,j,i,d,i,j)+
                    'CoL{}D{} = OR(3L{}D{}, 2L{}D{})\n'.format(i,j,i,j,i,j))
                else:
                    #se ho l'ultimo full-adder in un livello diverso dal primo prendo il CO dal livello precedente
                    f.write('\n# FULLADDER LIV {} BIT {}'.format(i,j))
                    A='W_X{}Y{}'.format(j,a)
                    B='CoL{}D{}'.format(c,j)
                    text_generated=('\n'
                    '1L{}D{} = XOR({}, {})\n'.format(i,j,A,B)+
                    '2L{}D{} = AND({}, {})\n'.format(i,j,A,B)+
                    '3L{}D{} = AND(1L{}D{}, CoL{}D{})\n'.format(i,j,i,j,i,d)+
                    'SL{}D{} = XOR(CoL{}D{}, 1L{}D{})\n'.format(i,j,i,d,i,j)+
                    'CoL{}D{} = OR(3L{}D{}, 2L{}D{})\n'.format(i,j,i,j,i,j))
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
        f.write('\n# HALFADDER RCA BIT {}'.format(j))
        text_generated=('\n'
        #R è l'uscita del registro
        'S{} = XOR(W_X{}Y{}, R{})\n'.format(j,0,0,j)+
        'Co{} = AND(W_X{}Y{}, R{})\n'.format(j,0,0,j))
        f.write(text_generated)
    else:
        # i successivi devo prendere i bit a 0 dei livelli precedenti l'ultimo
        # qui j = 1 indica il primo livello, j=2 il secondo e così via, per questo i livelli sono bit-1 (invece che bit-2)
        if j<bit-1:
            f.write('\n# FULLADDER RCA BIT {} (Livello precedente)'.format(j))
            text_generated=('\n'
            '1{} = XOR(SL{}D{}, R{})\n'.format(j,d,0,j)+
            '2{} = AND(SL{}D{}, R{})\n'.format(j,d,0,j)+
            '3{} = AND(1{}, Co{})\n'.format(j,j,d)+
            'S{} = XOR(Co{}, 1{})\n'.format(j,d,j)+
            'Co{} = OR(3{}, 2{})\n'.format(j,j,j))
            f.write(text_generated)
        else:
            #qui prendo le uscite dell'ultimo rca nel moltiplicatore 
            if j!=(2*bit-1):
                f.write('\n# FULLADDER RCA INGRESSO BIT {} (Ultimo livello)'.format(j))
                text_generated=('\n'
                '1{} = XOR(SL{}D{}, R{})\n'.format(j,bit-2,s,j)+
                '2{} = AND(SL{}D{}, R{})\n'.format(j,bit-2,s,j)+
                '3{} = AND(1{}, Co{})\n'.format(j,j,d)+
                'S{} = XOR(Co{}, 1{})\n'.format(j,d,j)+
                'Co{} = OR(3{}, 2{})\n'.format(j,j,j))
                f.write(text_generated)
            else:
                #l'ultimo però avrebbe un carry out floating quindi lo faccio diventare un halfadder
                f.write('\n# Visto che il carry out sarebbe floating metto un halfadder\n# HALFADDER RCA INGRESSO BIT {}'.format(j))
                text_generated=('\n'
                '1{} = XOR(CoL{}D{}, R{})\n'.format(j,bit-2,s-1,j)+
                # f'2{j} = AND(CoL{u-2}D{s-1}, R{j})\n'
                # f'3{j} = AND(1{j}, Co{d})\n'
                'S{} = XOR(Co{}, 1{})\n'.format(j,d,j))
                # f'Co{j} = OR(3{j}, 2{j})\n')
                f.write(text_generated)
#costruisco il registro
f.write('\n# 4) Registro R di {} bit'.format(2*bit))
#ovviamente di grandezza 2n
for j in range(2*bit):
    text_generated=('\n'
    #semplicemente prendo le uscite e le metto in un flip flop d
    'R{} = DFF(S{})\n'.format(j,j)+
    'OUTPUT(R{})'.format(2*bit-j-1))
    f.write(text_generated)
f.close()
