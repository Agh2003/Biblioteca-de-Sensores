VL53L0X - Sensor de Distância
=============================

O módulo ``VL53L0X`` fornece uma interface para o sensor de distância por laser VL53L0X, permitindo medições precisas de distância.

.. autoclass:: sensores.vl53l0x.VL53L0X
   :members:
   :undoc-members:
   :show-inheritance:

Exemplo de Uso
--------------

.. code-block:: python

   from sensores import VL53L0X, Porta
   
   # Inicializar sensor
   sensor = VL53L0X(mux_channel=Porta.I2C1)
   
   # Ler distância
   distancia = sensor.read_distance()
   print(f"Distância: {distancia} mm")
   
   # Fechar conexão
   sensor.close()

Calibração
----------

Para obter medições precisas, calibre o sensor com uma distância conhecida:

.. code-block:: python

   # Calibrar com objeto a 100mm
   sensor.calibrar_distancia(100)
   
   # Verificar se está calibrado
   if sensor.esta_calibrado():
       print("Sensor calibrado!")

Métodos Principais
------------------

.. method:: read_distance()
   :noindex:

   Lê a distância medida pelo sensor.
   
   :returns: Distância em milímetros
   :rtype: float

.. method:: calibrar_distancia(distancia_real)
   :noindex:

   Calibra o sensor com uma distância conhecida.
   
   :param distancia_real: Distância real do objeto em mm
   :type distancia_real: float

.. method:: esta_calibrado()
   :noindex:

   Verifica se o sensor foi calibrado.
   
   :returns: True se calibrado, False caso contrário
   :rtype: bool

Notas Técnicas
--------------

* **Endereço I2C**: 0x29
* **Alcance**: 0-2000mm
* **Precisão**: ±3% (após calibração)
* **Resolução**: 1mm
* **Calibração**: Persistente em arquivo .pkl
