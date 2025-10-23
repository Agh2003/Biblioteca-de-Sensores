# Guia do Desenvolvedor - Biblioteca de Sensores

Este guia é destinado a desenvolvedores que querem contribuir ou entender melhor a estrutura da biblioteca.

## 🏗️ Estrutura do Projeto

```
Biblioteca-de-Sensores/
├── sensores/                 # Módulos principais da biblioteca
│   ├── __init__.py          # Exports principais
│   ├── configuracao.py      # Sistema de configuração persistente
│   ├── i2cmodule.py         # Classe base para módulos I2C
│   ├── tcs34725.py          # Sensor de cor RGB
│   ├── vl53l0x.py           # Sensor de distância
│   ├── mg90s.py             # Servomotor
│   ├── pca9685.py           # Controlador PWM
│   ├── botoes.py            # Interface para botões
│   └── portas.py            # Gerenciamento de portas I2C
├── exemplo/                  # Exemplos de uso
│   ├── botaoSensores.py     # Exemplo com botão e sensores
│   └── garraSensorCor.py    # Exemplo de garra com sensor de cor
├── data/                    # Arquivos de calibração
│   ├── calibracao_tcs34725.pkl
│   └── calibracao_vl53l0x.pkl
├── docs/                    # Documentação
│   ├── source/              # Código-fonte da documentação
│   │   ├── conf.py          # Configuração do Sphinx
│   │   ├── index.rst        # Página principal
│   │   ├── installation.rst  # Guia de instalação
│   │   ├── quickstart.rst   # Início rápido
│   │   ├── changelog.rst    # Histórico de versões
│   │   ├── api/             # Documentação da API
│   │   └── examples/        # Exemplos documentados
│   └── build/               # Documentação HTML (gerada)
├── requirements.txt         # Dependências Python
├── build_docs.sh           # Script para gerar documentação
├── README.md               # Documentação principal
└── .gitignore              # Arquivos ignorados pelo Git
```

## 🔧 Desenvolvimento

### Adicionando Novos Sensores

1. **Crie o módulo** em `sensores/novo_sensor.py`
2. **Herde de I2CModule**:
   ```python
   from sensores.i2cmodule import I2CModule
   
   class NovoSensor(I2CModule):
       def __init__(self, endereco, canal_mux):
           super().__init__(endereco, canal_mux)
           # Configurações específicas
   ```
3. **Adicione ao __init__.py**:
   ```python
   from .novo_sensor import NovoSensor
   
   __all__ = [
       # ... outros módulos
       "NovoSensor",
   ]
   ```
4. **Documente a API** em `docs/source/api/novo_sensor.rst`
5. **Adicione exemplos** em `docs/source/examples/`

### Padrões de Código

- **Docstrings**: Use formato Google/NumPy
- **Nomes**: Português para métodos públicos, inglês para internos
- **Tratamento de erros**: Sempre feche conexões em `finally`
- **Calibração**: Use sistema de configuração persistente

### Testando Mudanças

```bash
# Teste básico
python3 -c "from sensores import *; print('Import OK')"

# Teste com hardware (se disponível)
python3 exemplo/botaoSensores.py

# Gere documentação para verificar
./build_docs.sh
```

## 📚 Documentação

### Atualizando a Documentação

1. **Modifique arquivos .rst** em `docs/source/`
2. **Regenere a documentação**:
   ```bash
   ./build_docs.sh
   ```
3. **Verifique o resultado** em `docs/build/index.html`

### Estrutura da Documentação

- **index.rst**: Página principal com visão geral
- **installation.rst**: Guia de instalação e configuração
- **quickstart.rst**: Exemplos básicos para começar
- **api/**: Documentação detalhada de cada módulo
- **examples/**: Exemplos práticos com código
- **changelog.rst**: Histórico de versões

### Adicionando Nova Documentação

1. **Crie arquivo .rst** em `docs/source/`
2. **Adicione ao toctree** em `docs/source/index.rst`:
   ```rst
   .. toctree::
      :maxdepth: 2
      
      novo_arquivo
   ```
3. **Regenere** com `./build_docs.sh`

## 🚀 Deploy

### Preparando para GitHub

1. **Verifique .gitignore**:
   - ✅ `docs/build/` (documentação compilada)
   - ✅ `venv/` (ambiente virtual)
   - ✅ `data/*.pkl` (arquivos de calibração)
   - ✅ `__pycache__/` (cache Python)

2. **Teste o script de documentação**:
   ```bash
   ./build_docs.sh
   ```

3. **Verifique o README**:
   - Instruções claras de instalação
   - Tutorial de geração de documentação
   - Exemplos práticos

### Versionamento

- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Changelog**: Atualize `docs/source/changelog.rst`
- **Tags**: Marque releases importantes

## 🐛 Debugging

### Problemas Comuns

1. **ImportError**: Verifique dependências em `requirements.txt`
2. **Permission denied**: Usuário precisa estar nos grupos `i2c` e `gpio`
3. **Documentação não gera**: Verifique se Sphinx está instalado
4. **Sensores não detectados**: Use `sudo i2cdetect -y 1`

### Logs e Debug

```python
# Habilitar debug no código
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar conexões I2C
from sensores.i2cmodule import I2CModule
# Adicione prints para debug
```

## 🤝 Contribuindo

1. **Fork** o repositório
2. **Clone** seu fork
3. **Crie branch** para sua feature
4. **Desenvolva** e teste
5. **Documente** suas mudanças
6. **Commit** com mensagem clara
7. **Push** para seu fork
8. **Abra Pull Request**

### Checklist para PR

- [ ] Código testado
- [ ] Documentação atualizada
- [ ] Exemplos funcionando
- [ ] README atualizado (se necessário)
- [ ] Changelog atualizado
- [ ] Sem erros de lint

---

**Dúvidas? Consulte a documentação completa gerada com `./build_docs.sh`**
