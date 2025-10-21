import time
from smbus2 import SMBus
from sensores.configuracao import Configuracao

# ===== ENDEREÇOS =====
I2C_DEVICE = 1            # Número do barramento I2C (/dev/i2c-1)
TCA9548A_ADDR = 0x70      # Endereço do multiplexador TCA9548A
TCS34725_ADDR = 0x29      # Endereço I2C do sensor TCS34725
COMMAND_BIT = 0x80        # Bit de comando para acessar os registradores do sensor


class TCS34725:
    def __init__(self, canal_mux, chave_sensor: str = "sensor_tcs34725"):
        """
        Inicializa o sensor TCS34725:
        """
        self.bus = SMBus(I2C_DEVICE)            # Abre comunicação I2C
        self._selecionar_canal_mux(canal_mux)   # Seleciona o canal ativo no MUX
        self._habilitar_sensor()                # Liga o sensor
        self._tempo_integracao(24)              # Tempo de integração = 24 ms
        self._ganho(4)                          # Ganho = 4x (valor padrão)

        # Configuração para salvar e recuperar calibração
        self.chave_sensor = chave_sensor
        self.config = Configuracao("calibracao_tcs34725")  # cria/abre arquivo .pkl
        self.CHAVE_PRETO = f"{self.chave_sensor}_preto"
        self.CHAVE_BRANCO = f"{self.chave_sensor}_branco"

        # Carrega valores de calibração salvos, se existirem
        self.valores_min = self.config.obtem(self.CHAVE_PRETO)
        self.valores_max = self.config.obtem(self.CHAVE_BRANCO)

    # ---------------- MULTIPLEXADOR ----------------
    def _selecionar_canal_mux(self, canal):
        """Ativa apenas o canal especificado no multiplexador TCA9548A"""
        self.bus.write_byte(TCA9548A_ADDR, 1 << canal)

    # ---------------- CONFIGURAÇÃO DO SENSOR ----------------
    def _write8(self, reg, valor):
        """Escreve 1 byte no registrador indicado do TCS34725"""
        self.bus.write_byte_data(TCS34725_ADDR, COMMAND_BIT | reg, valor)

    def _read8(self, reg):
        """Lê 1 byte de um registrador do TCS34725"""
        return self.bus.read_byte_data(TCS34725_ADDR, COMMAND_BIT | reg)

    def _read16(self, reg):
        """Lê 2 bytes (word) de um registrador do TCS34725 e combina em inteiro de 16 bits"""
        dados = self.bus.read_i2c_block_data(TCS34725_ADDR, COMMAND_BIT | reg, 2)
        return dados[1] << 8 | dados[0]

    def _habilitar_sensor(self):
        """Liga o sensor: Power ON + habilita RGBC (cor)"""
        self._write8(0x00, 0x01)  # Liga o sensor (PON)
        time.sleep(0.01)
        self._write8(0x00, 0x03)  # Liga a leitura de cores (PON + AEN)

    def _tempo_integracao(self, ms):
        """Configura o tempo de integração do sensor (ATIME)"""
        atime = 256 - int(ms / 2.4)  # Conversão do tempo em ms para valor do registrador
        self._write8(0x01, atime)

    def _ganho(self, ganho):
        """Configura o ganho do sensor (CONTROL)"""
        ganhos = {1: 0x00, 4: 0x01, 16: 0x02, 60: 0x03}
        self._write8(0x0F, ganhos.get(ganho, 0x01))

    # ---------------- LEITURA ----------------
    def ler_cores(self):
        """Retorna os valores brutos dos canais (R, G, B, C)"""
        c = self._read16(0x14)  # Canal Clear (luz total)
        r = self._read16(0x16)  # Vermelho
        g = self._read16(0x18)  # Verde
        b = self._read16(0x1A)  # Azul
        return r, g, b, c

    # ---------------- CALIBRAÇÃO ----------------
    def calibrar(self, amostras):
        """
        Realiza calibração do sensor para branco e preto
        Salva os valores no arquivo de calibração para uso posterior
        """
        print("Coloque o sensor sobre uma superfície BRANCA e pressione ENTER.")
        input()
        branco = self._media(amostras)
        print(f"Leitura BRANCO: {branco}")

        print("Coloque o sensor sobre uma superfície PRETA e pressione ENTER.")
        input()
        preto = self._media(amostras)
        print(f"Leitura PRETO: {preto}")

        self.valores_max = branco
        self.valores_min = preto

        # Salva valores no arquivo de calibração
        self.config.insere(self.CHAVE_BRANCO, branco)
        self.config.insere(self.CHAVE_PRETO, preto)

        print("Calibração concluída.")

    def _media(self, amostras):
        """Faz a média de N leituras (R, G, B, C)"""
        sr = sg = sb = sc = 0
        for _ in range(amostras):
            r, g, b, c = self.ler_cores()
            sr += r; sg += g; sb += b; sc += c
        return sr // amostras, sg // amostras, sb // amostras, sc // amostras

    # ---------------- NORMALIZAÇÃO ----------------
    def cores_normalizadas(self):
        """Normaliza valores R,G,B,C para escala 0–255 usando os valores de calibração"""
        if self.valores_min is None or self.valores_max is None:
            raise RuntimeError("É necessário calibrar o sensor antes de normalizar.")

        bruto = self.ler_cores()
        normalizado = []
        for i, valor in enumerate(bruto):
            min_v, max_v = self.valores_min[i], self.valores_max[i]
            if max_v == min_v:
                normalizado.append(0)
            else:
                perc = (valor - min_v) / (max_v - min_v)  # Percentual entre preto e branco
                perc = max(0.0, min(1.0, perc))          # Garante que está no intervalo [0, 1]
                normalizado.append(int(perc * 255))
        return tuple(normalizado)

    def nome_cor(self):
        """Retorna o nome da cor predominante com base nos valores normalizados"""
        r, g, b, c = self.cores_normalizadas()
        if r < 20 and g < 20 and b < 20:
            return "Preto"
        if r > 220 and g > 220 and b > 220:
            return "Branco"
        if r > g and r > b:
            return "Vermelho"
        elif g > r and g > b:
            return "Verde"
        elif b > r and b > g:
            return "Azul"
        return "Indefinido"

    def close(self):
        """Fecha o barramento I2C."""
        self.bus.close()

# # ===== TESTE =====
# if __name__ == "__main__":
#     sensor = TCS34725(canal_mux=1)
#     # sensor.calibrar(amostras=100) #caso eu queira fazer uma nova calibracao, descomentar

#     try:
#         if sensor.valores_min is None or sensor.valores_max is None:
#             print("Nenhuma calibração salva. Iniciando calibração...")
#             sensor.calibrar(amostras=100)
#         else:
#             print("Calibração carregada do arquivo.")

#         while True:
#             cores = sensor.cores_normalizadas()
#             cor_nome = sensor.nome_cor()
#             print(f"Normalizado: {cores} -> {cor_nome}")
#             time.sleep(0.5)
#     except KeyboardInterrupt:
#         print("Encerrando...")
#     finally:
#         sensor.close()