import pandas as pd
import matplotlib.pyplot as plt

with open("DatabaseREMs/Hypnogram_excerpt3.txt", "r") as f:
    lines = f.readlines()  #le todas as linhas do arquivo
    stages = [int(line.strip()) for line in lines[1:]] 


times = [i * 5 for i in range(len(stages))] # estágios de 5 segundos

plt.figure(figsize=(10, 3))
plt.step(times, stages, where='post')
plt.title("Hipnograma - Estágios do Sono")
plt.xlabel("Tempo (s)")
plt.ylabel("Estágio")
plt.yticks([5, 4, 3, 2, 1, 0, -1], ["Wake", "REM", "S1", "S2", "S3", "S4", "Movimento"])
plt.grid(True)
plt.tight_layout()
plt.show()




#REM(Rapid Eye Movement) — sono dos sonhos
#Stage 1 (S1) transição entre vigília e sono leve
#Stage 2 (S2) sono leve, com fusos do sono e K-complexos
#Stage 3 (S3) sono profundo (delta)
#Stage 4 (S4) sono muito profundo (delta ainda mais intenso)
#Movimento	Movimento do corpo — sem estágio definido
