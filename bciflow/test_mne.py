import pyedflib
import mne
arquivo = "../DatabaseREMs/excerpt4.edf"

raw = mne.io.read_raw_edf(arquivo, preload=True)

# Mostra as informações do arquivo
print(raw.info)
print(dir(raw))

n_amostras = raw.n_times
print(f"Número total de amostras: {n_amostras}")

data = raw.get_data()
print(data.shape)  