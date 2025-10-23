from sensores.i2cmodule import I2CModule
import smbus2
import time

# ===== ENDEREÇOS E CONFIGURAÇÕES =====
PCA9685_ADDR = 0x40      # Endereço I2C do módulo PCA9685 (padrão)

class PCA9685(I2CModule):
    # Registradores importantes do PCA9685
    __MODE1 = 0x00        # Registrador de controle principal (MODE1)
    __PRESCALE = 0xFE     # Registrador para configurar frequência PWM
    __LED0_ON_L = 0x06    # Endereço do primeiro registrador do canal 0

    def __init__(self, mux_channel=0):
        """
        Inicializa o PCA9685
        """
        super().__init__(PCA9685_ADDR, mux_channel)
        self.reset()                         # Reseta PCA9685 para estado padrão

    def reset(self):
        """
        Reseta o PCA9685 para o modo padrão
        """
        self.bus.write_byte_data(self.address, self.__MODE1, 0x00)
        time.sleep(0.01) 

    def set_pwm_freq(self, freq_hz):
        """
        Configura a frequência do PWM para todos os canais
        """
        # Fórmula: prescale = round(25MHz / (4096 * freq)) - 1
        prescaleval = 25000000.0 / 4096.0 / float(freq_hz) - 1.0
        prescale = int(prescaleval + 0.5)

        # Para alterar prescale é necessário colocar o PCA9685 em sleep
        old_mode = self.bus.read_byte_data(self.address, self.__MODE1)
        new_mode = (old_mode & 0x7F) | 0x10  # Ativa bit de SLEEP
        self.bus.write_byte_data(self.address, self.__MODE1, new_mode)
        self.bus.write_byte_data(self.address, self.__PRESCALE, prescale)  # Escreve novo prescale
        self.bus.write_byte_data(self.address, self.__MODE1, old_mode)     # Sai do modo sleep
        time.sleep(0.005)
        # Ativa auto-incremento e reinicia contadores para aplicar nova frequência
        self.bus.write_byte_data(self.address, self.__MODE1, old_mode | 0xA1)

    def set_pwm(self, channel, on, off):
        """
        Configura manualmente os valores ON e OFF de um canal específico
        on  -> valor de início do pulso (0-4095)
        off -> valor de término do pulso (0-4095)
        """
        reg = self.__LED0_ON_L + 4 * channel  # Calcula endereço do registrador do canal
        # Escreve os 4 registradores: ON_L, ON_H, OFF_L, OFF_H
        self.bus.write_byte_data(self.address, reg, on & 0xFF)
        self.bus.write_byte_data(self.address, reg + 1, on >> 8)
        self.bus.write_byte_data(self.address, reg + 2, off & 0xFF)
        self.bus.write_byte_data(self.address, reg + 3, off >> 8)

    def set_pwm_duty_cycle(self, channel, duty_cycle):
        """
        Configura duty cycle de forma simplificada (0.0 a 1.0)
        """
        duty_cycle = max(0.0, min(1.0, duty_cycle))  # Garante intervalo válido
        off_value = int(duty_cycle * 4095)           # Converte fração para valor 12-bit
        self.set_pwm(channel, 0, off_value)          # Pulso começa em 0 e termina em off_value