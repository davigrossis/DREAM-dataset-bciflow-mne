import numpy as np
from dataset_bci import DreamsDataset
from bciflow.modules.tf.bandpass.chebyshevII import chebyshevII
from bciflow.modules.fe.logpower import logpower
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda
from bciflow.modules.core.kfold import kfold

dataset = DreamsDataset(
    "../DatabaseREMs/excerpt4.edf",
    "../DatabaseREMs/Hypnogram_excerpt4.txt"
)

dataset.criar_trials(tamanho_janela=5, sobreposicao=2.5)
data = dataset.montar_dicionario_bciflow()

print("EEG signals shape:", data['X'].shape)
print("Labels:", data['y'])
print("Class dictionary:", data["y_dict"])
print("Events:", np.array(data["events"]))
print("Events dict", data["events_dict"])
print("Channel names:", data["ch_names"])
print("Sampling frequency (Hz):", data["sfreq"])
print("Start time (s):", data["tmin"])


#
#5 = vigília (wake),
#4 = REM,(Estagio dos sonhos)
#3, 2, 1, 0 (s1,s2,s3,s4Sono profundo) = estágios de sono (variam entre R&K e AASM),