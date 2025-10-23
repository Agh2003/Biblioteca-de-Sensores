import pickle

class Configuracao:
    """
    Sistema de configuração persistente para salvar e carregar dados entre execuções.
    
    Esta classe permite salvar configurações em arquivos pickle que persistem
    entre diferentes execuções do programa. Útil para calibrações de sensores,
    configurações de usuário e outros dados que devem ser mantidos.
    
    Args:
        nomeArquivo (str): Nome do arquivo de configuração (sem extensão)
        
    Example:
        >>> config = Configuracao("minha_config")
        >>> config.insere("nome", "Gabriel")
        >>> config.insere("idade", 25)
        >>> nome = config.obtem("nome")
        >>> print(nome)
        Gabriel
    """
    
    def __init__(self, nomeArquivo):
        """
        Inicializa o sistema de configuração.
        
        Args:
            nomeArquivo (str): Nome do arquivo de configuração
        """
        self.nomeArquivo = nomeArquivo
        self.nomeArquivo += ".pkl"
        try:
            self.carrega()
        except: # se nao conseguir carregar, cria um arquivo novo vazio
            self.config = []

    def limpa(self):
        """
        Remove todas as configurações salvas.
        
        Apaga completamente o arquivo de configuração e cria um novo vazio.
        """
        self.config = []
        self.salva()

    def salva(self):
        """
        Salva as configurações atuais no arquivo.
        
        Escreve todas as configurações para o arquivo pickle no diretório 'data/'.
        """
        with open('data/' + self.nomeArquivo, 'wb') as f:
            pickle.dump(self.config, f)

    def carrega(self):
        """
        Carrega as configurações do arquivo.
        
        Lê as configurações salvas do arquivo pickle no diretório 'data/'.
        
        Raises:
            FileNotFoundError: Se o arquivo não existir
            pickle.UnpicklingError: Se o arquivo estiver corrompido
        """
        with open('data/' + self.nomeArquivo, 'rb') as f:
            self.config = pickle.load(f)

    def obtem(self, chave):
        """
        Obtém um valor de configuração salvo.
        
        Args:
            chave (str): Nome da configuração a ser recuperada
            
        Returns:
            any: Valor salvo ou None se não encontrado
            
        Example:
            >>> config = Configuracao("teste")
            >>> config.insere("nome", "Gabriel")
            >>> nome = config.obtem("nome")
            >>> print(nome)
            Gabriel
        """
        for i in self.config:
            if i[0] == chave:
                return i[1]
        return None
    
    def insere(self, chave, valor):
        """
        Insere ou atualiza um valor de configuração.
        
        Se a chave já existir, atualiza o valor. Caso contrário, adiciona uma nova
        configuração. As alterações são salvas automaticamente.
        
        Args:
            chave (str): Nome da configuração
            valor (any): Valor a ser salvo
            
        Example:
            >>> config = Configuracao("teste")
            >>> config.insere("idade", 25)
            >>> config.insere("idade", 26)  # Atualiza valor existente
        """
        for i in self.config:
            if i[0] == chave:
                i[1] = valor
                self.salva()
                return
        self.config.append([chave, valor])
        self.salva()