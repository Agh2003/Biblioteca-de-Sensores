Instalação e Configuração
==========================

Requisitos do Sistema
---------------------

A Biblioteca de Sensores foi desenvolvida para funcionar em sistemas Linux, especialmente em placas como Raspberry Pi. Os seguintes requisitos são necessários:

* **Python 3.6+**
* **Linux** (testado em Raspberry Pi OS)
* **Acesso I2C** habilitado no sistema
* **Permissões de hardware** adequadas

Dependências
------------

A biblioteca requer as seguintes dependências Python:

.. code-block:: bash

   smbus2>=0.4.0
   RPi.GPIO>=0.7.0

Instalação das Dependências
---------------------------

Para instalar as dependências necessárias:

.. code-block:: bash

   pip install smbus2 RPi.GPIO

Ou usando requirements.txt (se disponível):

.. code-block:: bash

   pip install -r requirements.txt

Configuração do Sistema
-----------------------

Habilitar I2C
~~~~~~~~~~~~~

No Raspberry Pi, você precisa habilitar o I2C:

1. Execute ``sudo raspi-config``
2. Vá para "Interfacing Options" → "I2C"
3. Selecione "Yes" para habilitar
4. Reinicie o sistema

Verificar I2C
~~~~~~~~~~~~~

Para verificar se o I2C está funcionando:

.. code-block:: bash

   sudo i2cdetect -y 1

Você deve ver uma tabela com endereços dos dispositivos conectados.

Permissões de Hardware
~~~~~~~~~~~~~~~~~~~~~~

Certifique-se de que o usuário tem permissões adequadas:

.. code-block:: bash

   sudo usermod -a -G i2c $USER
   sudo usermod -a -G gpio $USER

Reinicie a sessão após adicionar os grupos.

Estrutura de Arquivos
---------------------

Após a instalação, a biblioteca criará automaticamente os seguintes diretórios:

::

   Biblioteca-de-Sensores/
   ├── sensores/           # Módulos principais da biblioteca
   ├── data/              # Arquivos de calibração (.pkl)
   ├── exemplo/           # Exemplos de uso
   └── docs/              # Documentação

Arquivos de Calibração
~~~~~~~~~~~~~~~~~~~~~~

A biblioteca salva automaticamente os arquivos de calibração em ``data/``:

* ``calibracao_tcs34725.pkl`` - Calibração do sensor de cor
* ``calibracao_vl53l0x.pkl`` - Calibração do sensor de distância

Teste de Instalação
-------------------

Para verificar se a instalação foi bem-sucedida, execute um teste simples:

.. code-block:: python

   from sensores import Porta
   print("Biblioteca de Sensores instalada com sucesso!")
   print(f"Portas I2C disponíveis: {Porta.I2C0}, {Porta.I2C1}")

Solução de Problemas
--------------------

Problema: "Permission denied" ao acessar I2C
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solução**: Adicione o usuário aos grupos necessários e reinicie:

.. code-block:: bash

   sudo usermod -a -G i2c,gpio $USER
   logout
   # Faça login novamente

Problema: "ModuleNotFoundError: No module named 'smbus2'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solução**: Instale as dependências:

.. code-block:: bash

   pip install smbus2 RPi.GPIO

Problema: Sensores não são detectados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solução**: Verifique as conexões e endereços I2C:

.. code-block:: bash

   sudo i2cdetect -y 1

Problema: Arquivos de calibração corrompidos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Solução**: Delete os arquivos de calibração para recriar:

.. code-block:: bash

   rm data/*.pkl
