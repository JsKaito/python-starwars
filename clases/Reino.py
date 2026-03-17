from Nave import Nave
from Mandaloriano import Mandaloriano
naves = Nave.crearNaves(self=None)
mandaloriano = Mandaloriano.crearMandalorianos(self=None)

cantidadNaves = [0, 2, 2, 4, 10]
cantidadMandalorianos = [0, 2, 2, 4, 10]
precioTotal = 0 

while True:
    for i in range(len(cantidadNaves)):
        precioTotal += cantidadNaves[i] * naves[i].coste
        precioTotal += cantidadMandalorianos[i] * mandaloriano[i].coste
        
    print(f"El precio total es: {precioTotal}")
        
    if precioTotal < 100000:
        break
    print("El precio total supera los 100000 créditos.Vuelve a introducir las cantidades.")
    
    
    
