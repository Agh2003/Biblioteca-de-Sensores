import time
from smbus2 import SMBus
from sensores.configuracao import Configuracao 

# ===== ENDEREÇOS =====
I2C_DEVICE = 1            # Número do barramento I2C (/dev/i2c-1)
VL53L0X_ADDR = 0x29       # Endereço do sensor VL53L0X
TCA9548A_ADDR = 0x70      # Endereço do multiplexador TCA9548A

class VL53L0X:
    """Classe para controle do sensor de distância VL53L0X"""
    def __init__(self, canal_mux=0):
        self.bus = SMBus(I2C_DEVICE)
        self.canal_mux = canal_mux

        # Gerencia o arquivo de configuração para salvar offset
        self.config = Configuracao("calibracao_vl53l0x")
        self.offset = self.config.obtem("offset") or 0  # Carrega offset salvo, se existir

        self._selecionar_canal_mux()
        model_id = self._read_byte(0xC0)
        if model_id != 0xEE:
            raise Exception(f"VL53L0X não encontrado (ID lido: {hex(model_id)})")

    # ----- MULTIPLEXADOR -----
    def _selecionar_canal_mux(self):
        """Seleciona o canal ativo no TCA9548A"""
        self.bus.write_byte(TCA9548A_ADDR, 1 << self.canal_mux)

    # ----- MÉTODOS I2C -----
    def _read_byte(self, reg):
        return self.bus.read_byte_data(VL53L0X_ADDR, reg)

    def _write_byte(self, reg, valor):
        self.bus.write_byte_data(VL53L0X_ADDR, reg, valor)

    def _read_word(self, reg):
        high = self._read_byte(reg)
        low = self._read_byte(reg + 1)
        return (high << 8) | low

    # ----- LEITURA DE DISTÂNCIA -----
    def ler_distancia(self):
        """Lê a distância em mm, aplicando o offset de calibração"""
        self._selecionar_canal_mux()
        self._write_byte(0x00, 0x01)

        while (self._read_byte(0x00) & 0x01) != 0:
            time.sleep(0.01)

        distancia = self._read_word(0x14 + 10)
        self._write_byte(0x0B, 0x01)
        return distancia + self.offset

    # ----- CALIBRAÇÃO -----
    def calibrar(self, distancia_real_mm, amostras=100):
        """Calibra o sensor para uma distância real conhecida e salva o offset"""
        print(f"Coloque um objeto a {distancia_real_mm} mm do sensor.")
        input("Pressione ENTER para iniciar a calibração...")

        valores = []
        for _ in range(amostras):
            dist = self.ler_distancia() - self.offset
            valores.append(dist)
            time.sleep(0.02)

        media = sum(valores) / len(valores)
        self.offset = int(distancia_real_mm - media)

        # Salva o novo offset no arquivo de configuração
        self.config.insere("offset", self.offset)
        print(f"Calibração concluída. Offset salvo: {self.offset} mm")

    def close(self):
        self.bus.close()


# # ===== TESTE =====
# if __name__ == "__main__":
#     sensor = VL53L0X(canal_mux=0)
#     # sensor.calibrar(100) #caso eu queira fazer uma nova calibracao, descomentar

#     try:
#         # Verifica se há calibração salva
#         if sensor.config.obtem("offset") is None:
#             print("Nenhuma calibração encontrada, iniciando calibração...")
#             sensor.calibrar(100)  # aqui você define a distância real usada para calibrar
#         else:
#             print(f"Calibração carregada: offset = {sensor.offset} mm")

#         while True:
#             print(f"Distância medida: {sensor.ler_distancia()} mm")
#             time.sleep(0.5)

#     except KeyboardInterrupt:
#         print("Encerrando leitura...")
#     finally:
#         sensor.close()