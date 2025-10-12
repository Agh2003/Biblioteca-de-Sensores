import time
from portas import Porta
from tcs34725 import ColorSensor
from vl53l0x import VL53L0X
from botoes import Botao


def main():
    print("Iniciando sensores...")
    botao = Botao(portas=("P2",))  # Botão físico usado como seletor
    sensor_cor = ColorSensor(mux_channel=Porta.I2C1)
    sensor_dist = VL53L0X(mux_channel=Porta.I2C1)  # Alterar para Porta.I2C0 se existir
    modo = "cor"  # começa no modo sensor de cor

    print("Sistema iniciado. Pressione o botão para alternar entre sensores.")
    print("Modo atual: Sensor de COR")

    try:
        while True:
            # Se o botão for pressionado, alterna o modo
            if botao.esta_pressionado("P2"):
                if modo == "cor":
                    modo = "distancia"
                    print("\n➡ Alterado para modo SENSOR DE DISTÂNCIA\n")
                else:
                    modo = "cor"
                    print("\n➡ Alterado para modo SENSOR DE COR\n")
                time.sleep(0.8)  # debounce (evita múltiplas trocas rápidas)

            # Executa leituras de acordo com o modo atual
            if modo == "cor":
                r, g, b, c = sensor_cor.read_colors()
                nome_cor = sensor_cor.get_color_name()
                print(f"Cor detectada: {nome_cor} | R={r} G={g} B={b} C={c}")
            else:
                distancia = sensor_dist.read_distance()
                print(f"Distância medida: {distancia} mm")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Encerrando o teste...")
    finally:
        sensor_cor.close()
        sensor_dist.close()


if __name__ == "__main__":
    main()
