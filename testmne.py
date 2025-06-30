import pyedflib
import matplotlib.pyplot as plt
import numpy as np
import mne
import os

print("Script iniciado...") 

caminho = os.path.join("DatabaseREMs", "excerpt2.edf")

try:
    raw = mne.io.read_raw_edf(caminho, preload=True)
    print("Canais:", raw.ch_names)
    
    raw.plot(duration=10, n_channels=10, scalings='auto', block=True)

except Exception as e:
    print("Erro ao carregar com MNE:", e)


