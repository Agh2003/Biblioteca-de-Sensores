from sensores import PCA9685, MG90S, TCS34725
import time

def pegarObjeto(initial_angle):
    pca = PCA9685(mux_channel=5)

    servo1 = MG90S(pca, channel=0)    

    servo1.set_angle(initial_angle) 

    #tudo reto
    servo2 = MG90S(pca, channel=4)
    servo2.set_angle(50)

    servo4 = MG90S(pca, channel=12)
    # abrir
    servo4.set_angle(0)

    # abaixar 
    print("Movendo o servo2 de 0° a 180°...")
    for angle in range(50, 110, 5):
        print(f"Ângulo: {angle}°")
        servo2.set_angle(angle)
        #time.sleep(0.1)
    
    #fechar
    servo4.set_angle(25)

    #subir
    servo2.set_angle(50)

    #direcao deposito
    for angle in range(initial_angle, 0, -7):
        servo1.set_angle(angle)

    #abrir
    servo4.set_angle(0)

    
if __name__ == "__main__":
    # Inicializa PCA9685 no canal 0 do multiplexador
    pca = PCA9685(mux_channel=5)

    while(True):
        print('Coloque o objeto para leitura e pressione enter.')        
        input()

        cor = TCS34725(canal_mux=1).nome_cor()
        print(cor)
        
        if cor == 'Vermelho':
            pegarObjeto(180)
        elif cor == 'Verde':
            pegarObjeto(130)
        elif cor == 'Azul':
            pegarObjeto(80)
        else:
            print('Cor invalida')
            input()

        MG90S(pca, 0).set_angle(130) 
