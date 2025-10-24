Biblioteca de Sensores
=====================

Uma biblioteca Python para controle de sensores e dispositivos eletrônicos, especialmente projetada para projetos de robótica e automação.

.. toctree::
   :maxdepth: 2
   :caption: Conteúdo:

   installation
   quickstart
   api/index
   examples/index
   changelog

Visão Geral
-----------

A Biblioteca de Sensores fornece uma interface Python simples e intuitiva para trabalhar com diversos tipos de sensores e dispositivos eletrônicos. A biblioteca inclui suporte para:

* **Sensores de Cor**: TCS34725 para detecção de cores RGB
* **Sensores de Distância**: VL53L0X para medição de distância por laser
* **Servomotores**: MG90S para controle de movimento
* **Controladores PWM**: PCA9685 para múltiplos canais PWM
* **Botões e Entradas Digitais**: Interface simples para botões físicos
* **Gerenciamento de Portas**: Sistema organizado para gerenciar conexões I2C

Características Principais
--------------------------

* **Interface Simples**: API intuitiva e fácil de usar
* **Calibração Automática**: Sistema de calibração persistente para sensores
* **Gerenciamento de Configuração**: Salvamento automático de configurações
* **Suporte I2C**: Comunicação I2C com multiplexadores
* **Documentação Completa**: Exemplos práticos e documentação detalhada

Exemplo Rápido
--------------

.. code-block:: python

   from sensores import TCS34725, VL53L0X, Porta, Botao
   
   # Inicializar sensores
   sensor_cor = TCS34725(mux_channel=Porta.I2C1)
   sensor_distancia = VL53L0X(mux_channel=Porta.I2C1)
   botao = Botao(portas=("P2",))
   
   # Ler dados dos sensores
   r, g, b, c = sensor_cor.read_colors()
   distancia = sensor_distancia.read_distance()
   
   # Verificar botão
   if botao.esta_pressionado("P2"):
       print("Botão pressionado!")
   
   # Fechar conexões
   sensor_cor.close()
   sensor_distancia.close()

Indices e tabelas
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
