# sensores/__init__.py
from .tcs34725 import TCS34725
from .vl53l0x import VL53L0X
from .mg90s import MG90S
from .pca9685 import PCA9685
from .botoes import Botao
from .portas import Porta
from .i2cmodule import I2CModule

__all__ = [
    "TCS34725",
    "VL53L0X",
    "MG90S",
    "PCA9685",
    "Botao",
    "Porta",
    "I2CModule",
]

