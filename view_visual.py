import mne
import os

edf_path = os.path.join("DatabaseREMs", "excerpt1.edf")
txt_path = os.path.join("DatabaseREMs", "Visual_scoring1_excerpt1.txt")

raw = mne.io.read_raw_edf(edf_path, preload=True)

annotations = []
with open(txt_path, "r") as f:
    lines = f.readlines()

current_desc = None
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("[") and line.endswith("]"):
        current_desc = line.strip("[]")
    else:
        try:
            start, duration = map(float, line.split())
            # FILTRA duração inválida ou negativa
            if duration > 0:
                annotations.append((start, duration, current_desc))
        except ValueError:
            print(f"Linha ignorada: {line}")


onsets = [a[0] for a in annotations]
durations = [a[1] for a in annotations]
descriptions = [a[2] for a in annotations]

raw.set_annotations(mne.Annotations(onsets, durations, descriptions))

raw.plot(duration=30, n_channels=7, scalings='auto', block=True)
