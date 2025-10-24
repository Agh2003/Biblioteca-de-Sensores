Botao - Botões Físicos
=======================

O módulo ``Botao`` fornece interface para leitura de botões físicos conectados às portas GPIO.

.. autoclass:: sensores.botoes.Botao
   :members:
   :undoc-members:
   :show-inheritance:

Exemplo de Uso
--------------

.. code-block:: python

   from sensores import Botao
   import time
   
   # Inicializar botões nas portas P2 e P3
   botao = Botao(portas=("P2", "P3"))
   
   try:
       while True:
           # Verificar se P2 foi pressionado
           if botao.esta_pressionado("P2"):
               print("Botão P2 pressionado!")
           
           # Verificar se P3 foi pressionado
           if botao.esta_pressionado("P3"):
               print("Botão P3 pressionado!")
           
           time.sleep(0.1)
   except KeyboardInterrupt:
       print("Encerrando...")
   finally:
       botao.close()

Métodos Principais
------------------

.. method:: esta_pressionado(porta)
   :noindex:

   Verifica se um botão específico está pressionado.
   
   :param porta: Nome da porta (ex: "P2", "P3")
   :type porta: str
   :returns: True se pressionado, False caso contrário
   :rtype: bool

.. method:: adicionar_porta(porta)
   :noindex:

   Adiciona uma nova porta de botão.
   
   :param porta: Nome da porta a adicionar
   :type porta: str

Notas Técnicas
--------------

* **Portas suportadas**: P2, P3, P4, P5, etc.
* **Pull-up**: Habilitado internamente
* **Debounce**: Implementado para evitar leituras múltiplas
