Configuracao - Sistema de Configuração
======================================

O módulo ``Configuracao`` fornece um sistema para salvar e carregar configurações persistentes.

.. autoclass:: sensores.configuracao.Configuracao
   :members:
   :undoc-members:
   :show-inheritance:

Exemplo de Uso
--------------

.. code-block:: python

   from sensores import Configuracao
   
   # Criar/abrir arquivo de configuração
   config = Configuracao("minha_config")
   
   # Salvar valores
   config.insere("nome", "Gabriel")
   config.insere("idade", 25)
   config.insere("ativo", True)
   
   # Ler valores
   nome = config.obtem("nome")
   idade = config.obtem("idade")
   ativo = config.obtem("ativo")
   
   print(f"Nome: {nome}, Idade: {idade}, Ativo: {ativo}")
   
   # Limpar todas as configurações
   config.limpa()

Métodos Principais
------------------

.. method:: insere(chave, valor)
   :noindex:

   Insere ou atualiza um valor de configuração.
   
   :param chave: Nome da configuração
   :type chave: str
   :param valor: Valor a ser salvo
   :type valor: any

.. method:: obtem(chave)
   :noindex:

   Obtém um valor de configuração salvo.
   
   :param chave: Nome da configuração
   :type chave: str
   :returns: Valor salvo ou None se não encontrado
   :rtype: any

.. method:: limpa()
   :noindex:

   Remove todas as configurações salvas.

.. method:: salva()
   :noindex:

   Salva as configurações no arquivo.

.. method:: carrega()
   :noindex:

   Carrega as configurações do arquivo.

Notas Técnicas
--------------

* **Formato**: Arquivos .pkl (pickle)
* **Localização**: Diretório ``data/``
* **Persistência**: Configurações mantidas entre execuções
* **Thread-safe**: Não recomendado para uso concorrente
