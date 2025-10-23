MG90S - Servomotor
==================

O módulo ``MG90S`` fornece controle para servomotores MG90S através de sinais PWM.

.. autoclass:: sensores.mg90s.MG90S
   :members:
   :undoc-members:
   :show-inheritance:

Exemplo de Uso
--------------

.. code-block:: python

   from sensores import MG90S, PCA9685, Porta
   import time
   
   # Inicializar controlador PWM
   pwm = PCA9685(mux_channel=Porta.I2C1)
   
   # Inicializar servomotor no canal 0
   servo = MG90S(pwm, canal=0)
   
   # Mover para diferentes posições
   servo.mover(0)      # Posição mínima
   time.sleep(1)
   
   servo.mover(90)     # Posição central
   time.sleep(1)
   
   servo.mover(180)    # Posição máxima
   time.sleep(1)
   
   # Fechar conexões
   servo.close()
   pwm.close()

Métodos Principais
------------------

.. method:: mover(angulo)
   :noindex:

   Move o servo para o ângulo especificado.
   
   :param angulo: Ângulo em graus (0-180)
   :type angulo: int

.. method:: posicao_atual()
   :noindex:

   Retorna a posição atual do servo.
   
   :returns: Ângulo atual em graus
   :rtype: int

Notas Técnicas
--------------

* **Faixa de movimento**: 0-180 graus
* **Resolução**: ~1 grau
* **Frequência PWM**: 50Hz
* **Largura de pulso**: 1-2ms
