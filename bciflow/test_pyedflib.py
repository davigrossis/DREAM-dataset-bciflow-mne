import pyedflib

arquivo = "../DatabaseREMs/excerpt3.edf"

try:
    edf = pyedflib.highlevel.read_edf(arquivo)
    print("Número de sinais:", edf.signals_in_file)
    print("Labels:", edf.getSignalLabels())

    sinal = edf.readSignal(0)
    print("Primeiros valores:", sinal[:10])

    edf.close()

except Exception as e:
    print("Erro:", e)
