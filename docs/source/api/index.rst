Documentação da API
===================

Esta seção contém a documentação completa de todas as classes e métodos da Biblioteca de Sensores.

Módulos Principais
------------------

.. toctree::
   :maxdepth: 2

   tcs34725
   vl53l0x
   mg90s
   pca9685
   botoes
   portas
   configuracao
   i2cmodule

Visão Geral das Classes
-----------------------

Sensores
~~~~~~~~

* :class:`sensores.TCS34725` - Sensor de cor RGB
* :class:`sensores.VL53L0X` - Sensor de distância por laser

Atuadores
~~~~~~~~~

* :class:`sensores.MG90S` - Servomotor
* :class:`sensores.PCA9685` - Controlador PWM

Interface
~~~~~~~~~

* :class:`sensores.Botao` - Botões físicos
* :class:`sensores.Porta` - Gerenciamento de portas I2C
* :class:`sensores.Configuracao` - Sistema de configuração
* :class:`sensores.I2CModule` - Classe base para módulos I2C

Exemplos de Uso por Categoria
-----------------------------

Sensores de Cor
~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import TCS34725, Porta
   
   sensor = TCS34725(mux_channel=Porta.I2C1)
   r, g, b, c = sensor.read_colors()
   nome_cor = sensor.get_color_name()
   sensor.close()

Sensores de Distância
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import VL53L0X, Porta
   
   sensor = VL53L0X(mux_channel=Porta.I2C1)
   distancia = sensor.read_distance()
   sensor.close()

Controle de Servomotores
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import MG90S, PCA9685, Porta
   
   pwm = PCA9685(mux_channel=Porta.I2C1)
   servo = MG90S(pwm, canal=0)
   servo.mover(90)
   servo.close()
   pwm.close()

Botões e Entradas
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import Botao
   
   botao = Botao(portas=("P2", "P3"))
   if botao.esta_pressionado("P2"):
       print("Botão P2 pressionado!")
   botao.close()

Configuração e Calibração
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sensores import Configuracao
   
   config = Configuracao("minha_config")
   config.insere("valor", 123)
   valor = config.obtem("valor")
   config.salva()
