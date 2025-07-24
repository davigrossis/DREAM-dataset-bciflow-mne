import mne
import numpy as np
import os


class DreamsDataset:
    def __init__(self, caminho_arquivo, caminho_hypnograma=None):
        self.caminho_arquivo = caminho_arquivo
        self.caminho_hypnograma = caminho_hypnograma
        self.data = None
        self.labels = None
        self.canais = None
        self.sfreq = None
        self.eventos = None
        self.y = None

        self.load_data()

    def load_data(self):

        raw = mne.io.read_raw_edf(self.caminho_arquivo, preload=True)


        self.sfreq = raw.info['sfreq']
        self.canais = raw.ch_names

        sinais = raw.get_data()  # canais e amostras
        sinais = sinais.T  # amostras, canais


        self.data = sinais

        # Se tiver o arquivo do hypnograma, carrega os y
        if self.caminho_hypnograma and os.path.exists(self.caminho_hypnograma):
            self.labels = self.carregar_hypnograma(self.caminho_hypnograma)
            self.y = self.hypnograma_para_y(self.labels, self.sfreq)
        else:
            self.labels = np.array([0])
            self.y = None

    def carregar_hypnograma(self, caminho):

        with open(caminho, 'r') as file:
            linhas = file.readlines()

        estagios = [int(linha.strip()) for linha in linhas[1:]] 
        estagios = np.array(estagios)

        return estagios

    def hypnograma_para_y(self, estagios, sfreq):
        y = []
        duracao_epoca = 5

        for idx, estagio in enumerate(estagios):
            tempo_inicio = idx * duracao_epoca
            amostra_inicio = int(tempo_inicio * sfreq)

            y.append(estagio)

        y = np.array(y)

        return y

    def criar_trials(self, tamanho_janela=5, sobreposicao=0):
        amostras_por_janela = int(tamanho_janela * self.sfreq)
        passo = amostras_por_janela - int(sobreposicao * self.sfreq)

        total_amostras = self.data.shape[0]

        trials = []
        for inicio in range(0, total_amostras - amostras_por_janela + 1, passo):
            fim = inicio + amostras_por_janela
            janela = self.data[inicio:fim, :].T 
            trials.append(janela)

        self.trials = np.array(trials)  
        self.labels_trials = np.zeros((self.trials.shape[0],)) 

    def montar_dicionario_bciflow(self):
        X = self.data.T[np.newaxis, np.newaxis, :, :]

        y_dict = { 
            0: "Unknown",
            1: "Stage 1",
            2: "Stage 2",
            3: "Stage 3",
            4: "REM",
            5: "Awake"
        }

        dataset = {
            'X': X,
            'y': self.y,
            'sfreq': self.sfreq,
            'y_dict': y_dict,
            'events': None,
            'ch_names': self.canais,
            'tmin': 0.0
        }
        
        return dataset