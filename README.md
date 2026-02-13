# Radiomics-Pipeline

## Radiomics Extraction Pipeline

Questo repository contiene il codice per l'estrazione di feature radiomiche da qualsiasi immagine medica in formato NIfTI (.nii.gz), utilizzando la libreria [PyRadiomics](https://pyradiomics.readthedocs.io/en/latest/).

La pipeline processa coppie di file (Immagine CT + Maschera Binaria dei polmoni), calcola le caratteristiche morfologiche, statistiche e di texture, e salva i risultati in file CSV individuali e in un CSV riassuntivo contenente le features di tutti i pazienti.

**Prerequisiti**: Il progetto è sviluppato in Python. Per garantire la compatibilità delle dipendenze (specialmente per pyradiomics), si consiglia l'uso di Conda.\\
*Configurazione Ambiente*: 
```bash
conda create --name radiomics_env python=3.9
conda activate radiomics_env
```

*Installare le dipendenze*: installare prima il pacchetto *numpy*.
```bash
conda install numpy
pip install -r requirements.txt

📂 Struttura del Progettoradiomics_extraction.py: Script principale per l'esecuzione da riga di comando.radiomics_notebook.ipynb: Versione Jupyter Notebook per analisi interattiva.params.yml: File di configurazione con i parametri di estrazione (es. binWidth, resampledPixelSpacing, filtri).data/: Cartella suggerita per i dati di input.requirements.txt: Elenco dei pacchetti Python necessari.🚀 Come usare lo scriptLo script radiomics_extraction.py accetta diversi argomenti per gestire i percorsi dei dati e i parametri.Esempio di utilizzo:Bashpython radiomics_extraction.py \
    --data_path ./data/images \
    --mask_path ./data/masks \
    --param_file params.yml \
    --output_dir ./Results \
    --total_csv Final_Features.csv
Argomenti disponibili:ArgomentoDescrizione--data_path(Obbligatorio) Percorso alla cartella con le immagini CT.--mask_path(Obbligatorio) Percorso alla cartella con le maschere (_Lung.nii.gz).--param_file(Obbligatorio) File YAML con i settaggi di PyRadiomics.--output_dirCartella dove verranno salvati i CSV dei singoli soggetti (Default: Features).--total_csvNome del file CSV finale che aggrega tutti i soggetti.--verboseFlag per visualizzare i dettagli dei filtri e delle feature abilitate.🛠 Funzionamento InternoAllineamento: Lo script ordina e accoppia automaticamente immagini e maschere basandosi sulla numerazione presente nel nome del file.Estrazione: Utilizza SimpleITK per leggere i volumi NIfTI.Output: - Genera un file .csv per ogni paziente nella cartella di output scelta.Genera un file CSV globale (Total_features.csv) ideale per analisi statistiche o Machine Learning.[!IMPORTANT]Assicurati che l'immagine e la maschera abbiano la stessa geometria (origine, spaziatura e orientamento), altrimenti PyRadiomics solleverà un errore di Mismatch.📊 Esempio di OutputIl file CSV finale conterrà colonne relative a:Shape features (Volume, Superficie, Sfericità...)First Order statistics (Media, Deviazione Standard, Entropia...)Texture features (GLCM, GLRLM, GLSZM, NgTDM)
