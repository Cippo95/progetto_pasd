#la libreria sys permette di usare gli argomenti a riga di comando
import sys

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
#uso questo array per salvare i vari test
array = []

#apertura del file in lettura 
with open(file_name) as fp:
    for line in fp:
        if 'test' in line:
            #se sono arrivato al test successivo calcolo le statistiche del test precedente
            #controllo che siano stati iniettati dei guasti per poter fare i calcoli
            if(count_test!=0):
                #copertura di guasto con questo test
                test_fault_coverage=(count_fault/count_test)*100
                print("guasti rivelati: {}".format(count_fault),
                "\nguasti iniettati: {}".format(count_test),
                "\npercentuale di rivelazione: {}%".format(test_fault_coverage))
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
            #sono in una linea di test per cui conto
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
#salvo l'array dei vettori di test
with open(fn_array, "w") as fp:
    for line in array:
        fp.write(str(line))
#NB:ogni lista ha come primi due elementi gli ingressi e l'uscita precedente e poi le rivelazioni di guasto.


