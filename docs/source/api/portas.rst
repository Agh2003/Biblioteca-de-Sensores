Porta - Gerenciamento de Portas I2C
====================================

O módulo ``Porta`` fornece constantes e utilitários para gerenciamento de portas I2C.

.. autoclass:: sensores.portas.Porta
   :members:
   :undoc-members:
   :show-inheritance:

Constantes Disponíveis
----------------------

.. data:: Porta.I2C0
   :noindex:

   Canal I2C 0 do multiplexador.

.. data:: Porta.I2C1
   :noindex:

   Canal I2C 1 do multiplexador.

Exemplo de Uso
--------------

.. code-block:: python

   from sensores import Porta, TCS34725, VL53L0X
   
   # Usar diferentes canais I2C
   sensor_cor = TCS34725(mux_channel=Porta.I2C0)
   sensor_distancia = VL53L0X(mux_channel=Porta.I2C1)
   
   # Ler dados
   r, g, b, c = sensor_cor.read_colors()
   distancia = sensor_distancia.read_distance()
   
   # Fechar conexões
   sensor_cor.close()
   sensor_distancia.close()

Notas Técnicas
--------------

* **Multiplexador**: Permite múltiplos dispositivos I2C
* **Canais**: I2C0 e I2C1 disponíveis
* **Endereçamento**: Cada canal tem endereços I2C únicos
