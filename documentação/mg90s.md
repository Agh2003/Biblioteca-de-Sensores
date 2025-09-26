# MG90S
Classe para controle de servomotores **MG90S** utilizando o driver PCA9685 como gerador de sinal PWM.  
Permite converter ângulos para duty cycles e posicionar o servo em ângulos de 0° a 180°.

---

## Requisitos
- [time](https://docs.python.org/3/library/time.html)
- Uma instância da classe `PCA9685` (presente em `pca9685.py`) para controlar o PWM.

---

## Funcionalidades
- Configuração automática da frequência do PCA9685 para 50 Hz.
- Conversão de ângulo (0° a 180°) para duty cycle proporcional.
- Controle simples de posição do servo em graus.
- Suporte a ajustes de pulsos mínimos e máximos para calibração do movimento.

---

## Atributos da Classe
- **`pca`**: Instância de `PCA9685` usada para controlar o canal PWM.
- **`channel`**: Número do canal do PCA9685 ao qual o servo está conectado.
- **`min_ms`**: Pulso mínimo em milissegundos (padrão: `500 ms`, correspondente a 0°).
- **`max_ms`**: Pulso máximo em milissegundos (padrão: `2500 ms`, correspondente a 180°).
- **`freq`**: Frequência de operação do PWM em Hz (padrão: `50 Hz`).

---

## Métodos da Classe

### `__init__(self, pca, channel, min_us=500, max_us=2500, freq=50)`
Construtor da classe. Inicializa o controle do servo configurando os limites de pulso e ajustando a frequência do PCA9685.

- **Parâmetros**:
    - `pca`: instância de `PCA9685` usada para controlar o PWM.
    - `channel` (int): canal do PCA9685 ao qual o servo está conectado.
    - `min_ms` (int): largura mínima do pulso em milissegundos (padrão: `500 ms`).
    - `max_ms` (int): largura máxima do pulso em milissegundos (padrão: `2500 ms`).
    - `freq` (int): frequência do PWM em Hz (padrão: `50`).

---

### `angle_to_duty_cycle(self, angle)`
Converte um ângulo (0° a 180°) para um duty cycle correspondente (0.0 a 1.0).

- **Parâmetros**:
    - `angle` (float): ângulo desejado em graus.

- **Retorno**:
    - `float`: duty cycle correspondente (fração do período em nível alto).

- **Comportamento**:
    - Limita o ângulo ao intervalo [0, 180].
    - Calcula o pulso em milissegundos proporcional ao ângulo.
    - Converte o pulso em fração do período (duty cycle).

---

### `set_angle(self, angle)`
Move o servo para o ângulo especificado.

- **Parâmetros**:
    - `angle` (float): ângulo desejado em graus.

- **Comportamento**:
    - Converte o ângulo para duty cycle usando `angle_to_duty_cycle`.
    - Envia o duty cycle para o canal correto usando `pca.set_pwm_duty_cycle`.
    - Aguarda 0,3 s para permitir que o servo se mova.

---

## Exemplo

```python
from pca9685 import PCA9685
from mg90s import MG90S
import time

# Inicializa PCA9685 e o servo no canal 0
pca = PCA9685(mux_channel=0)
servo = MG90S(pca, channel=0)

try:
    while True:
        print("Movendo para 0°")
        servo.set_angle(0)
        time.sleep(1)

        print("Movendo para 90°")
        servo.set_angle(90)
        time.sleep(1)

        print("Movendo para 180°")
        servo.set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nMovimentação encerrada")
