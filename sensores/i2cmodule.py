from smbus2 import SMBus

I2C_DEVICE = 1  
TCA9548A_ADDR = 0x70     # Endereço do multiplexador TCA9548A

class I2CModule: 
    def __init__(self, address, canal_mux):
        self.bus = SMBus(I2C_DEVICE)
        self.address = address
        self._selecionar_canal_mux(canal_mux)

    def _selecionar_canal_mux(self, canal_mux):
        """Ativa apenas o canal especificado no multiplexador TCA9548A"""
        self.bus.write_byte(TCA9548A_ADDR, 1 << canal_mux)

    def __del__(self):
        """Fecha o barramento I2C ao destruir o objeto"""
        self.bus.close()
