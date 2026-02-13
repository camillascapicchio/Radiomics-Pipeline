# Radiomics-Pipeline

## Radiomics Extraction Pipeline

Questo repository contiene il codice per l'estrazione di feature radiomiche da qualsiasi immagine medica in formato NIfTI (.nii.gz), utilizzando la libreria [PyRadiomics](https://pyradiomics.readthedocs.io/en/latest/).

La pipeline processa coppie di file (Immagine CT + Maschera Binaria dei polmoni), calcola le caratteristiche morfologiche, statistiche e di texture, e salva i risultati in file CSV individuali e in un CSV riassuntivo contenente le features di tutti i pazienti.

**Prerequisiti**: Il progetto è sviluppato in Python. Per garantire la compatibilità delle dipendenze (specialmente per pyradiomics), si consiglia l'uso di Conda. 

*Configurazione Ambiente*: 
```bash
conda create --name radiomics_env python=3.9
conda activate radiomics_env
```

*Installare le dipendenze*:
```bash
conda install numpy
pip install -r requirements.txt
```

**Struttura del Progetto**:

```extract_radiiomics_features.ipynb```: Versione Jupyter Notebook per analisi interattiva.

```extract_radiiomics_features.py```: Versione in Python per l'esecuzione da riga di comando.

```Params_tol_0_0001.yml```: File di configurazione con i parametri di estrazione (es. binWidth, resampledPixelSpacing, filtri).

```Data/```: Cartella con i dati di input.

```requirements.txt```: Elenco dei pacchetti Python necessari.

**Come usare lo script**

Lo script ```extract_radiiomics_features.py``` accetta diversi argomenti per gestire i percorsi dei dati e i parametri.

*Esempio di utilizzo*:
```bash
python3 extract_radiomics_features.py \
    --data_path Data/CT \
    --mask_path Data/Masks_Lung \
    --param_file Params_tol_0_0001.yaml \
    --output_dir Features \
    --total_csv Total_features.csv \
    --verbose

```
Argomenti disponibili:

```--data_path```(Obbligatorio): Percorso alla cartella con le immagini CT.

```--mask_path```(Obbligatorio): Percorso alla cartella con le maschere (_Lung.nii.gz).

```--param_file```(Obbligatorio): File YAML con i parametri per l'estrazione usati da PyRadiomics.

```--output_dir```: Cartella dove verranno salvati i CSV dei singoli soggetti (Default: Features).

```--total_csv```: Nome del file CSV finale che aggrega tutti i soggetti.

```--verbose```: Flag per visualizzare i dettagli dei filtri e delle feature abilitate.

**Funzionamento**: 

1. Lo script ordina e accoppia automaticamente immagini e maschere basandosi sulla numerazione presente nel nome del file.

2. Utilizza SimpleITK per leggere i volumi NIfTI.

***Importante*** Assicurati che l'immagine e la maschera abbiano la stessa geometria (origine, spaziatura e orientamento), altrimenti PyRadiomics solleverà un errore di Mismatch.

3. Output: - Genera un file .csv per ogni paziente nella cartella di output scelta.

4. Genera un file CSV globale (Total_features.csv) che conterrà colonne relative a: Shape features (Volume, Superficie, Sfericità...), First Order statistics (Media, Deviazione Standard, Entropia...), Texture features (GLCM, GLRLM, GLSZM, NgTDM), dati quantitativi ideali per analisi statistiche o Machine Learning.
