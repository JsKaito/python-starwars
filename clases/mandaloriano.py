import random as rd

class Mandaloriano:
    """Representa un Mandaloriano en el universo Star Wars."""

    def __init__(self, id, nombre, ataque, defensa, vida, velocidad, coste):
        """Inicializa un Mandaloriano."""
        self.id = id
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida = vida
        self.velocidad = velocidad
        self.coste = coste

    def crearMandatorianos(self):
        return [
            Mandaloriano(1, "Mandaloriano 1", 20, 15, 100, 60, 800),
            Mandaloriano(2, "Mandaloriano 2", 25, 20, 120, 50, 1000),
            Mandaloriano(3, "Mandaloriano 3", 30, 25, 140, 40, 1200),
            Mandaloriano(4, "Mandaloriano 4", 35, 30, 160, 30, 1500),
            Mandaloriano(5, "Mandaloriano 5", 40, 35, 180, 20, 2000)
        ]
