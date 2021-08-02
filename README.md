## Progetto per l'esame di Progetto Automatico di Sistemi Digitali (PASD)

La documentazione è in \documentazione\documentazione.pdf, consiglio di scaricare il file poiché alle volte non è correttamente visibile da github.

IN BREVE: 
Devo costruire un circuito multiply and accumulate (mac) nel formato .bench e fare un analisi statistica di esso in presenza di guasti.

Per fare questo uso HOPE, un simulatore di guasto e scrivo degli script in Python (al momento ho la versione 3.8.10).

Lo script "mac_generator.py" serve a compilare un file .bench per un circuito mac di dimensioni arbitrarie.
Per generare un mac 4 bit basta scrivere in console: "python3 mac_generator.py 4".

Non condivido HOPE perché non so se sia liberamente condivisibile.
In ogni caso ho lasciato nella cartella i vari file generati.

Una volta generato con "./hope -F mac -r 16 -0" il file mac (come detto è già presente), lo si può analizzare con "getvectors.py": "python3 getvectors.py mac".