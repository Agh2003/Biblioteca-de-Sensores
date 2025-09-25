# VL53L0X
Classe para controle do sensor de distância **VL53L0X** utilizando a Banana Pi M4 Zero, via barramento I2C, com suporte ao multiplexador **TCA9548A**.  
Permite inicialização do sensor, leitura da distância em milímetros, calibração para ajuste de offset e persistência desse offset para uso posterior.

---

## Requisitos
- time
- [smbus2](https://pypi.org/project/smbus2/)
- Módulo `configuracao.py` disponível no projeto — provê a classe Configuracao utilizada para salvar/recuperar os valores de calibração (arquivo .pkl).
---

## Funcionalidades
- Seleção automática do canal do multiplexador TCA9548A.
- Validação de presença do sensor por meio do model_id.
- Leitura da distância em milímetros.
- Calibração para distância conhecida e cálculo automático de offset.
- Armazenamento do offset em arquivo .pkl.
---

## Constantes
- **`I2C_DEVICE`**: Número do barramento I2C (/dev/i2c-1).
- **`VL53L0X_ADDR`**: Endereço I2C do sensor VL53L0X (0x29).
- **`TCA9548A_ADDR`**: Endereço I2C do multiplexador TCA9548A (0x70).
---

## Atributos da Classe
- **`bus`**: Instância `SMBus` para comunicação I2C.
- **`canal_mux`**: Número do canal selecionado no TCA9548A.
- **`config`**: Instância de `Configuracao("calibracao_vl53l0x")`, usada para persistir o offset.
- **`offset`**: Valor do offset de calibração em milímetros (padrão 0 se nenhum valor salvo).
---

## Métodos da Classe
### `__init__(self, canal_mux=0)`
Construtor da classe. Inicializa o barramento I2C, seleciona o canal do multiplexador e verifica se o sensor está presente lendo o registrador de `model_id`.

- **Parâmetros**:
    - `canal_mux` (int): Canal do multiplexador TCA9548A (padrão: 0).

- **Exceções**:
    - Levanta Exception se o ID lido não corresponder ao esperado (`0xEE`), indicando que o sensor não foi encontrado.

---

### `_read_byte(self, reg)`
Lê 1 byte de um registrador do sensor.

- **Parâmetros**:
    - `reg` (int): Endereço do registrador.

- **Retorno**:
    - `int` → valor lido.

---

### `_write_byte(self, reg, valor)`
Escreve 1 byte em um registrador do sensor.

- **Parâmetros**:
    - `reg` (int): Endereço do registrador.
    - `valor` (int): Byte a ser escrito.

---

### `_read_word(self, reg)`
Lê 2 bytes consecutivos a partir do registrador informado e combina em um valor de 16 bits (high byte + low byte).

- **Parâmetros**:
    - `reg` (int): Endereço inicial de leitura.

- **Retorno**:
    - `int`: Valor de 16 bits.

---

### `ler_distancia(self)`
Lê a distância medida pelo sensor (em milímetros), aplicando o offset de calibração.

- **Comportamento**:
    - Seleciona o canal no MUX.
    - Inicia uma medição escrevendo `0x01` no registrador `0x00`.
    - Aguarda o término da medição (bit 0x01 do registrador `0x00` deve ser resetado).
    - Lê a distância a partir do registrador `0x1E`.
    - Aplica o offset e retorna o valor.

- **Retorno**:
    - `int`: Distância em milímetros com ajuste de offset.

---

### `calibrar(self, distancia_real_mm, amostras=100)`
Realiza calibração do sensor para uma distância real conhecida, calculando e salvando o offset.

- **Parâmetros**:
    - `distancia_real_mm` (int): Distância real, em mm, entre o sensor e o objeto para referência.
    - `amostras` (int): Número de leituras usadas para calcular a média.

- **Comportamento**:
    - Solicita ao usuário posicionar um objeto a `distancia_real_mm` mm e pressionar ENTER.
    - Coleta `amostras` leituras, calcula a média.
    - Calcula `offset = distancia_real_mm - media`.
    - Salva o offset via `self.config.insere("offset", self.offset)`.

---

### `close(self)`
Fecha a comunicação com o barramento I2C `(self.bus.close())`.

---

## Exemplo

```python
from vl53l0x import VL53L0X
import time

sensor = VL53L0X(canal_mux=0)

try:
    # Verifica se existe offset salvo
    if sensor.config.obtem("offset") is None:
        print("Nenhuma calibração encontrada, iniciando calibração...")
        sensor.calibrar(100)  # define a distância real usada na calibração
    else:
        print(f"Calibração carregada: offset = {sensor.offset} mm")

    while True:
        distancia = sensor.ler_distancia()
        print(f"Distância medida: {distancia} mm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Encerrando leitura...")

finally:
    sensor.close()
