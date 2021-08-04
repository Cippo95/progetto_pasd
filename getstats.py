#la libreria sys permette di usare gli argomenti a riga di comando
import sys

#la libreria matplot permette di scrivere i grafici
import matplotlib.pyplot as plt

#coordinate delle x, sono i valori per la posizione delle barre
x_coordinates=[]

#controllo che venga passato al programma il file prodotto da HOPE da analizzare
if len(sys.argv) != 2:
    raise ValueError("Specifica il file da leggere come argomento!")

#assegno a file_name il nome del file prodotto da HOPE
file_name = sys.argv[1]

#nome del file in cui salvo gli ingressi le uscite precedenti e i guasti rivelati per ogni test
fn_array = (f"vectors_{file_name}")

#al fine di fare dei calcoli statistici introduco dei contatori

#contatore per i guasti rivelati
count_fault = 0
#contatore dei test totali (sono guasti iniettati)
count_test = 0
#uso questo contatore per contare il numero di test, per ottenere il numero di x
x_count = 0
#uso questo array per salvare le percentuali di probabilità di errore
error_probabilities = []
#uso questo array per salvare i vari test per poi farne un dump
array = []

#apertura del file in lettura, con with si chiude il file in automatico
with open(file_name) as fp:
    for line in fp:
        if 'test' in line:
            #se sono arrivato al test successivo calcolo le statistiche del test precedente
            #controllo che siano stati iniettati dei guasti per poter fare i calcoli
            if(count_test!=0):
                #aggiungo la coordinata x per il test precedente
                x_coordinates.append(x_count)
                #incremento la coordinata per il test successivo
                x_count +=1
                #copertura di guasto con questo test
                test_fault_coverage=(count_fault/count_test)*100
                #aggiungo il valore all'array delle probabilità di errore
                error_probabilities.append(test_fault_coverage)
                #print delle statistiche a terminale
                print("guasti rivelati: {}".format(count_fault)+
                "\nguasti iniettati: {}".format(count_test)+
                "\npercentuale di rivelazione: {:.5f}%".format(test_fault_coverage))
                #azzero i contatori
                count_fault = 0
                count_test = 0
                array.append(array_test)
            #preparo un array per i risultati di questo test
            array_test = []
            #scrivo il numero di test e gli ingressi e l'uscita precedente
            print("\n{}".format(line.strip()))
            #split separa la stringa in due
            input_output = line.split(':')
            #concateno in una unica riga:
            #1) prendo la seconda parte con gli ingressi e l'uscita precedente
            #2) strip toglie gli spazi intorno
            #3) split separa i vettori considerando lo spazio centrale
            input_output = input_output[1].strip().split()
            #inserisco gli ingressi e l'uscita precedente nel array dei risultati del test corrente
            array_test.append(input_output[0])
            array_test.append(input_output[1])
        else:
            #sono in una linea di test per cui la conto
            count_test += 1
            #se un guasto è rivelato ha l'asterisco
            if '*' in line:
                #conto il guasto rivelato
                count_fault += 1
                #scrivo a terminale
                print("{}".format(line.strip()))
                #recupero il vettore di rivelazione separando la stringa sull'asterisco
                test=line.split('*')
                #prendo la seconda parte (quella col vettore) e tolgo gli spazi
                test=test[1].strip()
                #aggiungo il vettore all'array dei risultati correnti
                array_test.append(test)
            else: 
                #recupero il vettore di rivelazione separando la stringa sul ":"
                test=line.split(':')
                #prendo la seconda parte (quella col vettore) e tolgo gli spazi
                test=test[1].strip()
                #aggiungo il vettore all'array dei risultati correnti
                array_test.append(test)
    #se sono arrivato alla fine calcolo le statistiche del test corrente
    #controllo che siano stati iniettati dei guasti per poter fare i calcoli
    if(count_test!=0):
        #aggiungo la coordinata x per il test
        x_coordinates.append(x_count)
        #copertura di guasto con questo test
        test_fault_coverage=(count_fault/count_test)*100
        #aggiungo il valore all'array delle probabilità di errore
        error_probabilities.append(test_fault_coverage)
        #print delle statistiche a terminale
        print("guasti rivelati: {}".format(count_fault)+
        "\nguasti iniettati: {}".format(count_test)+
        "\npercentuale di rivelazione: {:.5f}%".format(test_fault_coverage))
        #azzero i contatori
        count_fault = 0
        count_test = 0
        array.append(array_test) 
#salvo l'array dei vettori di test, un semplice dump
with open(fn_array, "w") as fp:
    for line in array:
        fp.write(str(line))
#NB:ogni lista ha come primi due elementi gli ingressi e l'uscita precedente e poi le rivelazioni di guasto.

#creo il grafico
#il nome del file sarà quello del file .bench con suffisso stats
graph_name = (f"{file_name}_stats")
#subplots più che altro per mettere la griglia in secondo piano
fig, ax = plt.subplots()
#creo un grafico a barre
ax.bar(x_coordinates, error_probabilities)
#assegno le etichette agli assi e il titolo all'immagine
ax.set(xlabel='test', ylabel='probabilità errore', title=graph_name)
#forzo la y a mostrare sempre dal 0 al 100%, se no si adatterebbe a seconda dei dati
ax.set_ylim([0,100])
#forzo la griglia ad andare sotto al grafico
ax.set_axisbelow(True)
#stile della griglia
ax.grid(linestyle='dashed')
#aggiustamenti ai valori mostrati sull'asse delle y
ax.locator_params(axis='y', nbins=25)
#salvo la figura come svg, importante perché in png (opzione di default) le renderizza male
fig.savefig(graph_name+".svg",format="svg")

