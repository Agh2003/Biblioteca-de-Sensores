# Biblioteca de Sensores

Uma biblioteca Python completa para controle de sensores e dispositivos eletrônicos, especialmente projetada para projetos de robótica e automação.

## 🚀 Características

- **Sensores de Cor**: TCS34725 para detecção RGB
- **Sensores de Distância**: VL53L0X para medição por laser
- **Servomotores**: MG90S para controle de movimento
- **Controladores PWM**: PCA9685 para múltiplos canais
- **Botões e Entradas**: Interface simples para botões físicos
- **Sistema de Calibração**: Persistente e automático
- **Documentação Completa**: Guias e exemplos práticos

## 📦 Instalação

### Requisitos
- Python 3.6+
- Linux (testado em Raspberry Pi OS)
- Acesso I2C habilitado

### Dependências
```bash
pip install smbus2 RPi.GPIO
```

### Configuração do Sistema
1. Habilite o I2C: `sudo raspi-config`
2. Adicione o usuário aos grupos: `sudo usermod -a -G i2c,gpio $USER`
3. Reinicie a sessão

## 🎯 Uso Rápido

```python
from sensores import TCS34725, VL53L0X, Porta

# Inicializar sensores
sensor_cor = TCS34725(mux_channel=Porta.I2C1)
sensor_distancia = VL53L0X(mux_channel=Porta.I2C1)

# Ler dados
r, g, b, c = sensor_cor.read_colors()
distancia = sensor_distancia.read_distance()

# Fechar conexões
sensor_cor.close()
sensor_distancia.close()
```

## 📚 Gerando a Documentação

A biblioteca inclui documentação completa gerada com Sphinx. Para visualizá-la, siga estes passos:

### Método 1: Script Automático (Recomendado)

```bash
# Torne o script executável (apenas na primeira vez)
chmod +x build_docs.sh

# Execute o script para gerar a documentação
./build_docs.sh
```

O script irá:
- ✅ Criar um ambiente virtual (se não existir)
- ✅ Instalar as dependências necessárias (Sphinx, tema Read the Docs)
- ✅ Gerar a documentação HTML
- ✅ Informar onde encontrar os arquivos

### Método 2: Manual

Se preferir fazer manualmente:

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar dependências
pip install sphinx sphinx-rtd-theme

# 4. Gerar documentação
sphinx-build -b html docs/source docs/build
```

### Visualizando a Documentação

Após gerar a documentação, você pode visualizá-la de duas formas:

#### Opção 1: Servidor Local (Recomendado)
```bash
cd docs/build
python3 -m http.server 8000
```
Depois acesse: **http://localhost:8000**

#### Opção 2: Arquivo Direto
Abra diretamente o arquivo `docs/build/index.html` no seu navegador.

### Estrutura da Documentação

A documentação inclui:

- **🏠 Página Principal**: Visão geral da biblioteca
- **⚙️ Instalação**: Guia completo de configuração
- **🚀 Início Rápido**: Exemplos básicos para começar
- **📖 API**: Documentação completa de todas as classes
- **💡 Exemplos**: Código prático da biblioteca
- **📝 Changelog**: Histórico de versões

### Atualizando a Documentação

Se você fizer mudanças no código ou na documentação:

```bash
# Execute novamente o script
./build_docs.sh

# Ou manualmente
source venv/bin/activate
sphinx-build -b html docs/source docs/build
```

## 🔧 Módulos Disponíveis

### Sensores
- `TCS34725`: Sensor de cor RGB
- `VL53L0X`: Sensor de distância por laser

### Atuadores
- `MG90S`: Servomotor
- `PCA9685`: Controlador PWM

### Interface
- `Botao`: Botões físicos
- `Porta`: Gerenciamento de portas I2C
- `Configuracao`: Sistema de configuração persistente

## 📁 Estrutura do Projeto

```
Biblioteca-de-Sensores/
├── sensores/           # Módulos principais da biblioteca
├── exemplo/            # Exemplos de uso
├── data/              # Arquivos de calibração (.pkl)
├── docs/              # Documentação
│   ├── source/        # Código-fonte da documentação (.rst)
│   └── build/         # Documentação HTML (gerada automaticamente)
├── requirements.txt   # Dependências Python
├── build_docs.sh     # Script para gerar documentação
└── README.md         # Este arquivo
```

## 🎮 Exemplos

### Exemplo 1: Botão com Sensores
```python
import time
from sensores import TCS34725, VL53L0X, Botao, Porta

botao = Botao(portas=("P2",))
sensor_cor = TCS34725(mux_channel=Porta.I2C1)
sensor_dist = VL53L0X(mux_channel=Porta.I2C1)

modo = "cor"
while True:
    if botao.esta_pressionado("P2"):
        modo = "distancia" if modo == "cor" else "cor"
        print(f"Modo: {modo}")
        time.sleep(0.8)
    
    if modo == "cor":
        r, g, b, c = sensor_cor.read_colors()
        print(f"Cor: {sensor_cor.get_color_name()}")
    else:
        print(f"Distância: {sensor_dist.read_distance()}mm")
    
    time.sleep(0.5)
```

### Exemplo 2: Controle de Servomotor
```python
from sensores import MG90S, PCA9685, Porta
import time

pwm = PCA9685(mux_channel=Porta.I2C1)
servo = MG90S(pwm, canal=0)

# Mover servo
servo.mover(0)      # Posição mínima
time.sleep(1)
servo.mover(90)     # Posição central
time.sleep(1)
servo.mover(180)    # Posição máxima

servo.close()
pwm.close()
```

## 🔍 Calibração

Para obter leituras precisas, calibre os sensores:

```python
# Sensor de cor
sensor_cor.calibrar_preto()   # Calibrar para preto
sensor_cor.calibrar_branco()  # Calibrar para branco

# Sensor de distância
sensor_dist.calibrar_distancia(100)  # Calibrar com objeto a 100mm
```

## 🐛 Solução de Problemas

### "Permission denied" ao acessar I2C
```bash
sudo usermod -a -G i2c,gpio $USER
logout  # Faça login novamente
```

### Sensores não detectados
```bash
sudo i2cdetect -y 1  # Verificar dispositivos I2C
```

### Arquivos de calibração corrompidos
```bash
rm data/*.pkl  # Remove arquivos corrompidos
```

### Erro ao gerar documentação
```bash
# Verifique se o ambiente virtual está ativo
source venv/bin/activate

# Reinstale as dependências
pip install --upgrade sphinx sphinx-rtd-theme

# Execute novamente
./build_docs.sh
```

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a documentação completa (gerada com `./build_docs.sh`)
- Verifique os exemplos incluídos
- Abra uma issue no repositório

---

**Desenvolvido com ❤️ para a comunidade de robótica e automação**
