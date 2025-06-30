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

        self.load_data()

    def load_data(self):
        print(f"edf carregado: {self.caminho_arquivo}")

        raw = mne.io.read_raw_edf(self.caminho_arquivo, preload=True)

        self.sfreq = raw.info['sfreq']
        self.canais = raw.ch_names
        print(f"canais encontrados: {self.canais}")
        print(f"frequência de amostragem: {self.sfreq} Hz")

        sinais = raw.get_data()  # canais e amostras
        sinais = sinais.T  # amostras, canais

        print(f"shape dos dados: {sinais.shape}")

        self.data = sinais

        # Se tiver o arquivo do hypnograma, carrega os eventos
        if self.caminho_hypnograma and os.path.exists(self.caminho_hypnograma):
            self.labels = self.carregar_hypnograma(self.caminho_hypnograma)
            self.eventos = self.hypnograma_para_eventos(self.labels, self.sfreq)
        else:
            self.labels = np.array([0])
            self.eventos = None

    def carregar_hypnograma(self, caminho):
        print(f"carregando hypnograma: {caminho}")
        with open(caminho, 'r') as file:
            linhas = file.readlines()

        estagios = [int(linha.strip()) for linha in linhas[1:]] 
        estagios = np.array(estagios)
        print(f"hypnograma carregado {len(estagios)} labels")
        return estagios

    def hypnograma_para_eventos(self, estagios, sfreq):
        eventos = []
        duracao_epoca = 5

        for idx, estagio in enumerate(estagios):
            tempo_inicio = idx * duracao_epoca
            amostra_inicio = int(tempo_inicio * sfreq)

            eventos.append(estagio)

        eventos = np.array(eventos)
        print(f"eventos gerados: {eventos.shape[0]}")
        return eventos

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
        print(f"Total de trials gerados: {self.trials.shape[0]}")

    def montar_dicionario_bciflow(self):
        X = self.trials[:, np.newaxis, :, :] 
        eventos_dict = {}
        if self.eventos is not None:
            eventos_dict = {
                "Sleep Stages": self.eventos.tolist()
            }
        else:
            eventos_dict = {
                "Task": [i for i in range(len(self.labels_trials))]
            }

        events_dict = { 
            0: "Unknown",
            1: "Stage 1",
            2: "Stage 2",
            3: "Stage 3",
            4: "REM",
            5: "Awake"
        }

        dataset = {
            'X': X,
            'y': None,
            'sfreq': self.sfreq,
            'y_dict': None,
            'events': eventos_dict,
            'events_dict': events_dict,
            'ch_names': self.canais,
            'tmin': 0.0
        }

        return dataset
#criar eventos_dict