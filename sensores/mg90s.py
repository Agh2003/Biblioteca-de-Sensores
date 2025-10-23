import time

class MG90S:
    def __init__(self, pca, channel, min_ms=500, max_ms=2500, freq=50):
        """
        Inicializa o servo MG90S
        """
        self.pca = pca              # instância de PCA9685 que controla o PWM
        self.channel = channel      # Canal do PCA9685 onde o servo está conectado
        self.min_ms = min_ms        # Pulso mínimo (em ms) correspondente ao ângulo 0°
        self.max_ms = max_ms        # Pulso máximo (em ms) correspondente ao ângulo 180°
        self.freq = freq            # Frequência de operação do PWM (50 Hz)
        self._last_angle = None      # Armazena o último ângulo definido

        # Configura a frequência do PCA9685 (necessário para que os cálculos de duty cycle fiquem corretos)
        self.pca.set_pwm_freq(freq)

    def angle_to_duty_cycle(self, angle):
        """
        Converte ângulo (0° a 180°) para duty cycle (0.0 a 1.0)
        Calcula o tempo de pulso necessário e divide pelo período para obter a fração
        """
        angle = max(0, min(180, angle))  # Garante que o ângulo esteja entre 0° e 180°
        pulse_ms = self.min_ms + (self.max_ms - self.min_ms) * (angle / 180.0)  # Calcula pulso em ms
        period_ms = 1_000_000 / self.freq  # Calcula período em ms (ex.: 50 Hz → 20000 ms)
        duty_cycle = pulse_ms / period_ms  # Fração do período que o sinal ficará em nível alto
        return duty_cycle

    def set_angle(self, angle):
        """
        Move o servo para o ângulo especificado
        Converte o ângulo em duty cycle e envia para o PCA9685
        """
        duty = self.angle_to_duty_cycle(angle)              # Converte ângulo para duty cycle
        self.pca.set_pwm_duty_cycle(self.channel, duty)     # Aplica duty cycle no canal correto
        self.last_angle = angle                              # Atualiza o último ângulo definido
        time.sleep(0.3)

    @property
    def last_angle(self):
        """Retorna o último ângulo definido"""
        return self._last_angle