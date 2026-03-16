from Nave import Nave
naves = Nave.crearNaves(self=None)

cantidadNaves = [0, 2, 2, 4, 10]
precioTotal = 0 
for i in range(len(cantidadNaves)):
    precioTotal += cantidadNaves[i] * naves[i].coste
    
print(f"El precio total de las naves es: {precioTotal}")