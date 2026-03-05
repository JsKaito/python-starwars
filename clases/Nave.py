import random as rd
class Nave:
    """Representa una nave en el universo Star Wars."""

    def __init__(self, id, nombre, ataque, defensa, vida, velocidad, coste):
        """Inicializa una nave."""
        self.id = id
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida = vida
        self.velocidad = velocidad
        self.coste = coste

    def crearNaves(self):
        nave1 = Nave(1, "Estrella de la Muerte", 80, 90, 1500, rd.randint(20, 30), 4500)
        nave2 = Nave(2, "Ejecutor", 70, 80, 1200, rd.randint(35, 50), 4000)
        nave3 = Nave(3, "Halcón Milenario", 60, 50, 800, 70, 2500)
        nave4 = Nave(4, "Nave Real de Naboo", 40, 60, 600, 50, 2000)
        nave5 = Nave(5, "Caza Estelar Jedi", 50, 40, 400, 80, 1500)