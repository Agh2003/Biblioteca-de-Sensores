Changelog
=========

Histórico de versões da Biblioteca de Sensores.

Versão 1.0 (2025-01-XX)
------------------------

**Novas funcionalidades:**
* Sensor de cor TCS34725 com detecção RGB
* Sensor de distância VL53L0X com medição por laser
* Controle de servomotor MG90S
* Controlador PWM PCA9685 para múltiplos canais
* Interface para botões físicos
* Sistema de configuração persistente
* Gerenciamento de portas I2C com multiplexador
* Sistema de calibração automática para sensores

**Módulos incluídos:**
* ``sensores.TCS34725`` - Sensor de cor RGB
* ``sensores.VL53L0X`` - Sensor de distância
* ``sensores.MG90S`` - Servomotor
* ``sensores.PCA9685`` - Controlador PWM
* ``sensores.Botao`` - Botões físicos
* ``sensores.Porta`` - Gerenciamento de portas
* ``sensores.Configuracao`` - Sistema de configuração
* ``sensores.I2CModule`` - Classe base I2C

**Exemplos incluídos:**
* ``exemplo/botaoSensores.py`` - Alternância entre sensores
* ``exemplo/garraSensorCor.py`` - Controle de garra por cor

**Documentação:**
* Documentação completa da API
* Guias de instalação e início rápido
* Exemplos práticos de uso
* Notas técnicas para cada módulo

**Dependências:**
* Python 3.6+
* smbus2 >= 0.4.0
* RPi.GPIO >= 0.7.0

**Compatibilidade:**
* Linux (testado em Raspberry Pi OS)
* Comunicação I2C
* Multiplexadores I2C
