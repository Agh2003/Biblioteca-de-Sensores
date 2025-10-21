# Porta
Classe que define as portas disponíveis na Banana Pi M4 Zero para utilização nos projetos.  
Agrupa portas **GPIO** e portas **I2C** em uma única classe, facilitando o acesso pelos demais módulos.

---

## Funcionalidades
- Fornece valores constantes para portas **GPIO** utilizadas para botões, LEDs ou outros periféricos digitais.
- Fornece valores constantes para os canais do **multiplexador I2C** TCA9548A (de 0 a 7).

---

## Constantes
### Portas GPIO
- **`P1`**: GPIO 267  
- **`P2`**: GPIO 266  
- **`P3`**: GPIO 265  
- **`P4`**: GPIO 234  

### Portas I2C (canais do multiplexador TCA9548A)
- **`I2C1`**: Canal 0  
- **`I2C2`**: Canal 1  
- **`I2C3`**: Canal 2  
- **`I2C4`**: Canal 3  
- **`I2C5`**: Canal 4  
- **`I2C6`**: Canal 5  
- **`I2C7`**: Canal 6  
- **`I2C8`**: Canal 7  

---

## Exemplo

```python
from portas import Porta

# Acessando uma porta GPIO
gpio = Porta.P1
print(f"Porta GPIO selecionada: {gpio}")

# Selecionando canal I2C do multiplexador
canal = Porta.I2C3
print(f"Canal I2C selecionado: {canal}")
