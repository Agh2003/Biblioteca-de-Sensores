Exemplos de Uso
===============

Esta seção contém exemplos práticos de como usar a Biblioteca de Sensores.

Exemplos Básicos
----------------

.. toctree::
   :maxdepth: 2

   botao_sensores
   garra_sensor_cor

Exemplo: Botão com Sensores
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este exemplo mostra como alternar entre diferentes sensores usando um botão físico.

**Arquivo**: ``exemplo/botaoSensores.py``

.. literalinclude:: ../../../exemplo/botaoSensores.py
   :language: python
   :linenos:

**Funcionalidades demonstradas:**
* Uso de botões físicos
* Alternância entre sensores
* Leitura de sensor de cor
* Leitura de sensor de distância
* Tratamento de interrupções

Exemplo: Garra com Sensor de Cor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este exemplo mostra como usar um sensor de cor para controlar uma garra robótica.

**Arquivo**: ``exemplo/garraSensorCor.py``

.. literalinclude:: ../../../exemplo/garraSensorCor.py
   :language: python
   :linenos:

**Funcionalidades demonstradas:**
* Detecção de cores específicas
* Controle de servomotores
* Sistema de calibração
* Lógica de controle baseada em cores

Exemplos Avançados
------------------

Exemplo: Sistema Completo de Robótica
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este exemplo mostra um sistema mais complexo combinando múltiplos sensores e atuadores:

.. code-block:: python

   import time
   from sensores import TCS34725, VL53L0X, MG90S, PCA9685, Botao, Porta
   
   class SistemaRobotico:
       def __init__(self):
           # Inicializar controladores
           self.pwm = PCA9685(mux_channel=Porta.I2C1)
           
           # Inicializar sensores
           self.sensor_cor = TCS34725(mux_channel=Porta.I2C0)
           self.sensor_distancia = VL53L0X(mux_channel=Porta.I2C0)
           
           # Inicializar atuadores
           self.garra = MG90S(self.pwm, canal=0)
           self.base = MG90S(self.pwm, canal=1)
           
           # Inicializar interface
           self.botao = Botao(portas=("P2", "P3"))
           
           print("Sistema robótico inicializado!")
       
       def detectar_objeto(self):
           """Detecta objeto próximo e identifica sua cor"""
           distancia = self.sensor_distancia.read_distance()
           
           if distancia < 100:  # Objeto próximo
               r, g, b, c = self.sensor_cor.read_colors()
               cor = self.sensor_cor.get_color_name()
               return True, cor, distancia
           
           return False, None, distancia
       
       def agarrar_objeto(self):
           """Abre a garra para agarrar objeto"""
           self.garra.mover(0)  # Abrir garra
           time.sleep(1)
           self.garra.mover(90)  # Fechar garra
           time.sleep(1)
       
       def rotacionar_base(self, angulo):
           """Rotaciona a base do robô"""
           self.base.mover(angulo)
           time.sleep(1)
       
       def executar_ciclo(self):
           """Executa um ciclo completo de operação"""
           try:
               while True:
                   # Verificar botões
                   if self.botao.esta_pressionado("P2"):
                       print("Iniciando ciclo de operação...")
                       self.executar_operacao()
                   
                   if self.botao.esta_pressionado("P3"):
                       print("Parando sistema...")
                       break
                   
                   time.sleep(0.1)
                   
           except KeyboardInterrupt:
               print("Sistema interrompido pelo usuário")
           finally:
               self.fechar_sistema()
       
       def executar_operacao(self):
           """Executa operação de pegar objeto"""
           # Detectar objeto
           objeto_detectado, cor, distancia = self.detectar_objeto()
           
           if objeto_detectado:
               print(f"Objeto detectado: {cor} a {distancia}mm")
               
               # Rotacionar base para posição
               self.rotacionar_base(45)
               
               # Agarrar objeto
               self.agarrar_objeto()
               
               # Rotacionar de volta
               self.rotacionar_base(0)
               
               print("Operação concluída!")
           else:
               print("Nenhum objeto detectado")
       
       def fechar_sistema(self):
           """Fecha todas as conexões"""
           self.sensor_cor.close()
           self.sensor_distancia.close()
           self.garra.close()
           self.base.close()
           self.pwm.close()
           self.botao.close()
           print("Sistema fechado com sucesso!")
   
   if __name__ == "__main__":
       sistema = SistemaRobotico()
       sistema.executar_ciclo()

Exemplo: Monitoramento Contínuo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este exemplo mostra como fazer monitoramento contínuo de sensores:

.. code-block:: python

   import time
   import json
   from datetime import datetime
   from sensores import TCS34725, VL53L0X, Porta
   
   class MonitorSensores:
       def __init__(self):
           self.sensor_cor = TCS34725(mux_channel=Porta.I2C1)
           self.sensor_distancia = VL53L0X(mux_channel=Porta.I2C1)
           self.dados = []
       
       def coletar_dados(self):
           """Coleta dados de todos os sensores"""
           timestamp = datetime.now().isoformat()
           
           # Ler sensor de cor
           r, g, b, c = self.sensor_cor.read_colors()
           cor = self.sensor_cor.get_color_name()
           
           # Ler sensor de distância
           distancia = self.sensor_distancia.read_distance()
           
           dados = {
               'timestamp': timestamp,
               'cor': {
                   'nome': cor,
                   'r': r,
                   'g': g,
                   'b': b,
                   'clear': c
               },
               'distancia': distancia
           }
           
           self.dados.append(dados)
           return dados
       
       def salvar_dados(self, arquivo='dados_sensores.json'):
           """Salva dados coletados em arquivo JSON"""
           with open(arquivo, 'w') as f:
               json.dump(self.dados, f, indent=2)
           print(f"Dados salvos em {arquivo}")
       
       def monitorar(self, duracao_minutos=5):
           """Monitora sensores por tempo determinado"""
           inicio = time.time()
           duracao_segundos = duracao_minutos * 60
           
           print(f"Iniciando monitoramento por {duracao_minutos} minutos...")
           
           try:
               while time.time() - inicio < duracao_segundos:
                   dados = self.coletar_dados()
                   print(f"[{dados['timestamp']}] Cor: {dados['cor']['nome']}, "
                         f"Distância: {dados['distancia']}mm")
                   
                   time.sleep(1)  # Coletar dados a cada segundo
                   
           except KeyboardInterrupt:
               print("Monitoramento interrompido pelo usuário")
           finally:
               self.salvar_dados()
               self.sensor_cor.close()
               self.sensor_distancia.close()
   
   if __name__ == "__main__":
       monitor = MonitorSensores()
       monitor.monitorar(duracao_minutos=2)
