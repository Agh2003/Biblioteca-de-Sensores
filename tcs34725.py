import time
from smbus2 import SMBus
from configuracao import Configuracao

# ===== ENDEREÇOS =====
I2C_DEVICE = 1
TCA9548A_ADDR = 0x70
TCS34725_ADDR = 0x29
COMMAND_BIT = 0x80


class TCS34725:
    def __init__(self, canal_mux, chave_sensor: str = "sensor_tcs34725"):
        self.bus = SMBus(I2C_DEVICE)
        self._selecionar_canal_mux(canal_mux)
        self._habilitar_sensor()
        self._tempo_integracao(24)
        self._ganho(4)

        # Configuração para salvar a calibração
        self.chave_sensor = chave_sensor
        self.config = Configuracao("calibracao_tcs34725")  # cria arquivo .pkl automático
        self.CHAVE_PRETO = f"{self.chave_sensor}_preto"
        self.CHAVE_BRANCO = f"{self.chave_sensor}_branco"

        self.valores_min = self.config.obtem(self.CHAVE_PRETO)
        self.valores_max = self.config.obtem(self.CHAVE_BRANCO)

    # ---------------- MULTIPLEXADOR ----------------
    def _selecionar_canal_mux(self, canal):
        self.bus.write_byte(TCA9548A_ADDR, 1 << canal)

    # ---------------- CONFIGURAÇÃO DO SENSOR ----------------
    def _write8(self, reg, valor):
        self.bus.write_byte_data(TCS34725_ADDR, COMMAND_BIT | reg, valor)

    def _read8(self, reg):
        return self.bus.read_byte_data(TCS34725_ADDR, COMMAND_BIT | reg)

    def _read16(self, reg):
        dados = self.bus.read_i2c_block_data(TCS34725_ADDR, COMMAND_BIT | reg, 2)
        return dados[1] << 8 | dados[0]

    def _habilitar_sensor(self):
        self._write8(0x00, 0x01)
        time.sleep(0.01)
        self._write8(0x00, 0x03)

    def _tempo_integracao(self, ms):
        atime = 256 - int(ms / 2.4)
        self._write8(0x01, atime)

    def _ganho(self, ganho):
        ganhos = {1: 0x00, 4: 0x01, 16: 0x02, 60: 0x03}
        self._write8(0x0F, ganhos.get(ganho, 0x01))

    # ---------------- LEITURA ----------------
    def ler_cores(self):
        c = self._read16(0x14)
        r = self._read16(0x16)
        g = self._read16(0x18)
        b = self._read16(0x1A)
        return r, g, b, c

    # ---------------- CALIBRAÇÃO ----------------
    def calibrar(self, amostras):
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

        # Salva no arquivo para uso futuro
        self.config.insere(self.CHAVE_BRANCO, branco)
        self.config.insere(self.CHAVE_PRETO, preto)

        print("Calibração concluída e salva.")

    def _media(self, amostras):
        sr = sg = sb = sc = 0
        for _ in range(amostras):
            r, g, b, c = self.ler_cores()
            sr += r; sg += g; sb += b; sc += c
        return sr // amostras, sg // amostras, sb // amostras, sc // amostras

    # ---------------- NORMALIZAÇÃO ----------------
    def cores_normalizadas(self):
        if self.valores_min is None or self.valores_max is None:
            raise RuntimeError("É necessário calibrar o sensor antes de normalizar.")

        bruto = self.ler_cores()
        normalizado = []
        for i, valor in enumerate(bruto):
            min_v, max_v = self.valores_min[i], self.valores_max[i]
            if max_v == min_v:
                normalizado.append(0)
            else:
                perc = (valor - min_v) / (max_v - min_v)
                perc = max(0.0, min(1.0, perc))
                normalizado.append(int(perc * 255))
        return tuple(normalizado)

    def nome_cor(self):
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
        self.bus.close()


# ===== TESTE =====
if __name__ == "__main__":
    sensor = TCS34725(canal_mux=1)
    # sensor.calibrar(amostras=100) #caso eu queira fazer uma nova calibracao, descomentar

    try:
        if sensor.valores_min is None or sensor.valores_max is None:
            print("Nenhuma calibração salva. Iniciando calibração...")
            sensor.calibrar(amostras=100)
        else:
            print("Calibração carregada do arquivo.")

        while True:
            cores = sensor.cores_normalizadas()
            cor_nome = sensor.nome_cor()
            print(f"Normalizado: {cores} -> {cor_nome}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Encerrando...")
    finally:
        sensor.close()
