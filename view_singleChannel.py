import mne
import matplotlib.pyplot as plt
import os

caminho = os.path.join("DatabaseREMs", "excerpt3.edf")
raw = mne.io.read_raw_edf(caminho, preload=True)

data, times = raw[:] #obter dados e tempos

for i, canal in enumerate(raw.ch_names):
    plt.figure(figsize=(20, 4))  
    plt.plot(times, data[i], color='blue')
    plt.title(f"Canal: {canal}")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude (uV)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
