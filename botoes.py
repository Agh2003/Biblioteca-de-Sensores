import time
import gpiod
from gpiod.line import Direction, Value
from portas import Porta  # Importa sua biblioteca de portas

class Botao:
    """
    Classe para gerenciar botões conectados na Banana Pi M4 Zero via GPIO.
    Cada botão retorna apenas dois estados: pressionado (0) ou liberado (1).
    """

    def __init__(self, portas):
        """
        Inicializa o driver dos botões para as portas desejadas.

        :param portas: tupla ou lista com as portas a serem utilizadas (ex: (Porta.P2, Porta.P3))
        """
        self.chip_name = "/dev/gpiochip0"
        self.chip = gpiod.Chip(self.chip_name)

        # Cria um dicionário para armazenar os objetos de cada botão
        self.botoes = {}
        for p in portas:
            self.botoes[p] = gpiod.request_lines(
                self.chip_name,
                config={p: gpiod.LineSettings(direction=Direction.INPUT)}
            )

        # Estados lógicos do botão
        self.LIBERADO = Value.ACTIVE
        self.APERTADO = Value.INACTIVE

    def ler_estado(self, porta):
        """
        Lê o estado do botão e já retorna True (pressionado) ou False (liberado).
        """
        if porta not in self.botoes:
            raise ValueError(f"Porta {porta} não foi inicializada.")

        # linha = self.PINOS[porta]
        estado = self.botoes[porta].get_value(porta)
        return estado == self.APERTADO  # True se pressionado, False se liberado

# ===== TESTE =====
if __name__ == "__main__":
    botoes = Botao(portas=(Porta.P2, Porta.P4))  # Inicializa dois botões (P2 e P4)

    print("Pressione Ctrl+C para sair.")
    try:
        while True:
            estado_p2 = "PRESSIONADO" if botoes.ler_estado(Porta.P2) else "LIBERADO"
            estado_p4 = "PRESSIONADO" if botoes.ler_estado(Porta.P4) else "LIBERADO"

            print(f"[P2] {estado_p2} | [P4] {estado_p4}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nEncerrando leitura dos botões.")
