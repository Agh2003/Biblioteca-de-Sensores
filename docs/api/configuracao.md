# Configuração
Classe para gerenciamento de configurações persistentes utilizando arquivos `.pkl`.  
Permite salvar, carregar, inserir, atualizar e limpar valores de configuração que permanecem disponíveis entre execuções do programa.

---

## Requisitos
- [pickle](https://docs.python.org/3/library/pickle.html)

---

## Funcionalidades
- Criação e gerenciamento automático de arquivos de configuração no formato `.pkl`.
- Inserção e atualização de valores de configuração de forma simples.
- Leitura de valores previamente salvos.
- Limpeza completa do arquivo de configuração.
- Carregamento automático no momento da inicialização da classe.

---

## Atributos da Classe
- **`nomeArquivo`**: Nome do arquivo de configuração utilizado, com sufixo `.pkl` adicionado automaticamente.
- **`config`**: Lista interna que armazena os pares `[chave, valor]` das configurações.

---

## Métodos da Classe

### `__init__(self, nomeArquivo)`
Construtor da classe. Define o nome do arquivo de configuração, tenta carregar o conteúdo existente e, caso não seja possível, cria uma lista vazia.

- **Parâmetros**:
    - `nomeArquivo` (str): Nome base do arquivo (sem extensão).

- **Comportamento**:
    - Adiciona a extensão `.pkl` ao nome do arquivo.
    - Tenta chamar `carrega()`. Caso não exista o arquivo ou ocorra erro, cria `self.config` como lista vazia.

---

### `limpa(self)`
Apaga todas as configurações armazenadas e salva o arquivo vazio.

---

### `salva(self)`
Salva o conteúdo atual de `self.config` no arquivo `.pkl` usando `pickle.dump`.

---

### `carrega(self)`
Carrega o conteúdo do arquivo `.pkl` para `self.config` usando `pickle.load`.

---

### `obtem(self, chave)`
Obtém o valor associado a uma chave previamente salva.

- **Parâmetros**:
    - `chave` (str): Nome da chave a ser buscada.

- **Retorno**:
    - Valor correspondente à chave, ou `None` se a chave não existir.

---

### `insere(self, chave, valor)`
Insere um novo valor ou atualiza um valor existente no arquivo de configuração.

- **Parâmetros**:
    - `chave` (str): Nome da chave a ser salva.
    - `valor`: Qualquer objeto serializável pelo `pickle`.

- **Comportamento**:
    - Procura pela chave na lista `config`.  
    - Se encontrada, atualiza o valor.  
    - Se não encontrada, adiciona uma nova entrada `[chave, valor]`.  
    - Salva o arquivo após a modificação.
