from pca9685 import PCA9685
from mg90s import MG90S
import time

def pegarObjeto():
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

    MG90S(pca, channel=0).set_angle(80)

    #abrir
    servo4.set_angle(0)

    
if __name__ == "__main__":
    # Inicializa PCA9685 no canal 0 do multiplexador
    pca = PCA9685(mux_channel=5)

    servo1 = MG90S(pca, channel=0)    

    servo1.set_angle(180) 
    pegarObjeto()

    servo1.set_angle(130) 
    pegarObjeto()

    servo1.set_angle(100) 
    pegarObjeto()

    servo1.set_angle(130) 