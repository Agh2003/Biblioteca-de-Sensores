I2CModule - Classe Base para Módulos I2C
=========================================

O módulo ``I2CModule`` é a classe base para todos os módulos que utilizam comunicação I2C.

.. autoclass:: sensores.i2cmodule.I2CModule
   :members:
   :undoc-members:
   :show-inheritance:

Exemplo de Uso
--------------

Esta classe é usada internamente pelos outros módulos. Exemplo de implementação:

.. code-block:: python

   from sensores.i2cmodule import I2CModule
   from smbus2 import SMBus
   
   class MeuSensor(I2CModule):
       def __init__(self, endereco, canal_mux):
           super().__init__(endereco, canal_mux)
           # Configurações específicas do sensor
       
       def ler_dados(self):
           # Implementar leitura específica
           dados = self.bus.read_byte_data(self.endereco, 0x00)
           return dados
       
       def close(self):
           # Fechar conexão
           super().close()

Métodos Principais
------------------

.. method:: __init__(endereco, canal_mux)
   :noindex:

   Inicializa a conexão I2C.
   
   :param endereco: Endereço I2C do dispositivo
   :type endereco: int
   :param canal_mux: Canal do multiplexador I2C
   :type canal_mux: int

.. method:: close()
   :noindex:

   Fecha a conexão I2C.

Notas Técnicas
--------------

* **Herança**: Classe base para todos os sensores I2C
* **Multiplexador**: Suporte automático a multiplexadores I2C
* **Gerenciamento**: Conexão automática e fechamento
