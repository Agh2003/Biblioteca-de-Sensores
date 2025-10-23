Guia de Início Rápido
=====================

Este guia mostra como começar a usar a Biblioteca de Sensores rapidamente.

Primeiro Exemplo
----------------

Vamos criar um exemplo simples que lê dados de um sensor de cor:

.. code-block:: python

   from sensores import TCS34725, Porta
   
   # Inicializar o sensor de cor
   sensor = TCS34725(mux_channel=Porta.I2C1)
   
   # Ler valores RGB
   r, g, b, c = sensor.read_colors()
   print(f"R={r}, G={g}, B={b}, Clear={c}")
   
   # Obter nome da cor
   nome_cor = sensor.get_color_name()
   print(f"Cor detectada: {nome_cor}")
   
   # Fechar conexão
   sensor.close()

Exemplo com Múltiplos Sensores
-------------------------------

Aqui está um exemplo mais completo usando vários sensores:

.. code-block:: python

   import time
   from sensores import TCS34725, VL53L0X, Botao, Porta
   
   def main():
       # Inicializar sensores
       sensor_cor = TCS34725(mux_channel=Porta.I2C1)
       sensor_distancia = VL53L0X(mux_channel=Porta.I2C1)
       botao = Botao(portas=("P2",))
       
       print("Sensores inicializados!")
       
       try:
           while True:
               # Ler sensor de cor
               r, g, b, c = sensor_cor.read_colors()
               cor = sensor_cor.get_color_name()
               
               # Ler sensor de distância
               distancia = sensor_distancia.read_distance()
               
               # Verificar botão
               if botao.esta_pressionado("P2"):
                   print("Botão pressionado!")
               
               # Exibir dados
               print(f"Cor: {cor} | Distância: {distancia}mm")
               time.sleep(0.5)
               
       except KeyboardInterrupt:
           print("Encerrando...")
       finally:
           sensor_cor.close()
           sensor_distancia.close()
   
   if __name__ == "__main__":
       main()

Calibração de Sensores
----------------------

Para obter leituras precisas, você precisa calibrar os sensores:

Calibração do Sensor de Cor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import TCS34725, Porta
   
   sensor = TCS34725(mux_channel=Porta.I2C1)
   
   # Calibrar para cor preta
   print("Coloque um objeto preto sobre o sensor e pressione Enter...")
   input()
   sensor.calibrar_preto()
   
   # Calibrar para cor branca
   print("Coloque um objeto branco sobre o sensor e pressione Enter...")
   input()
   sensor.calibrar_branco()
   
   print("Calibração concluída!")
   sensor.close()

Calibração do Sensor de Distância
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import VL53L0X, Porta
   
   sensor = VL53L0X(mux_channel=Porta.I2C1)
   
   # Calibrar com objeto conhecido
   print("Coloque um objeto a 100mm do sensor e pressione Enter...")
   input()
   sensor.calibrar_distancia(100)
   
   print("Calibração concluída!")
   sensor.close()

Controle de Servomotores
------------------------

Exemplo de controle de servomotor:

.. code-block:: python

   from sensores import MG90S, PCA9685, Porta
   import time
   
   # Inicializar controlador PWM
   pwm = PCA9685(mux_channel=Porta.I2C1)
   
   # Inicializar servomotor no canal 0
   servo = MG90S(pwm, canal=0)
   
   # Mover servo para diferentes posições
   servo.mover(0)      # Posição mínima
   time.sleep(1)
   
   servo.mover(90)     # Posição central
   time.sleep(1)
   
   servo.mover(180)    # Posição máxima
   time.sleep(1)
   
   # Fechar conexões
   servo.close()
   pwm.close()

Próximos Passos
---------------

Agora que você conhece o básico, explore:

* :doc:`api/index` - Documentação completa da API
* :doc:`examples/index` - Mais exemplos práticos
* :doc:`installation` - Configuração detalhada do sistema

Dicas Importantes
-----------------

* **Sempre feche as conexões** usando ``.close()`` quando terminar
* **Calibre os sensores** para obter leituras precisas
* **Use try/except** para tratamento de erros
* **Verifique as conexões I2C** antes de usar os sensores
