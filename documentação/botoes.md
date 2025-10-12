# Botões
Classe para controle de botões conectados na Banana Pi M4 Zero via GPIO, utilizando a biblioteca `gpiod`.  

---

## Requisitos
- [gpiod](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/) (para manipulação de GPIO no Linux)
- [time](https://docs.python.org/3/library/time.html)
- Módulo `portas.py` presente no projeto — contém a enumeração `Porta` com as portas `gpio` disponíveis da Banana Pi M4 Zero.

---

## Funcionalidades
- Inicialização de múltiplos botões em diferentes portas GPIO.
- Leitura do estado lógico de cada botão.
- Uso de constantes para representar estado **LIBERADO** e **APERTADO**.
- Tratamento de erro caso uma porta não tenha sido inicializada.

---

## Constantes
- **`LIBERADO`**: Representa estado lógico 1 (linha inativa → botão liberado).
- **`APERTADO`**: Representa estado lógico 0 (linha ativa → botão pressionado).

> **Observação:** Esses valores são instâncias de `gpiod.line.Value`.

---

## Atributos da Classe
- **`chip_name`**: Caminho para o dispositivo GPIO usado (`/dev/gpiochip0`).
- **`chip`**: Objeto `gpiod.Chip` que representa o chip de GPIO.
- **`botoes`**: Dicionário que mapeia cada porta para seu respectivo objeto de linha GPIO, retornado por `gpiod.request_lines`.

---

## Métodos da Classe

### `__init__(self, portas)`
Construtor da classe. Inicializa o driver dos botões para as portas especificadas.

- **Parâmetros**:
    - `portas` (tuple | list): portas a serem utilizadas.

- **Comportamento**:
    - Cria um dicionário interno `botoes`, onde cada chave é uma porta e o valor é o objeto retornado por `gpiod.request_lines` configurado como entrada (`Direction.INPUT`).
    - Define as constantes `LIBERADO` e `APERTADO` para facilitar comparação de estado.

---

### `ler_estado(self, porta)`
Lê o estado do botão de uma porta específica.

- **Parâmetros**:
    - `porta`: porta previamente inicializada no construtor.

- **Retorno**:
    - `True` se o botão está **pressionado**.
    - `False` se o botão está **liberado**.

- **Exceções**:
    - Lança `ValueError` se a porta informada não foi inicializada.

---

## Exemplo

```python
from botoes import Botao
from portas import Porta
import time

# Inicializa botões nas portas P2 e P4
botoes = Botao(portas=(Porta.P2, Porta.P4))

print("Pressione Ctrl+C para sair.")
try:
    while True:
        estado_p2 = "PRESSIONADO" if botoes.ler_estado(Porta.P2) else "LIBERADO"
        estado_p4 = "PRESSIONADO" if botoes.ler_estado(Porta.P4) else "LIBERADO"

        print(f"[P2] {estado_p2} | [P4] {estado_p4}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nEncerrando leitura dos botões.")
