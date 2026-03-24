import random as rd
class Nave:
    """Representa una nave en el universo Star Wars."""

    def __init__(self, id, name, attack, defense, hp, speed, price):
        """Inicializa naves."""
        self.id = id
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.speed = speed
        self.price = price

    @staticmethod
    def crearNaves():
        return [
            Nave(1, "Estrella de la Muerte", 80, 90, 1500, (20, 30), 4500),
            Nave(2, "Ejecutor", 70, 80, 1200, (35, 50), 4000),
            Nave(3, "Halcón Milenario", 60, 50, 800, (70, 70), 2500),
            Nave(4, "Nave Real de Naboo", 40, 60, 600, (50, 50), 2000),
            Nave(5, "Caza Estelar Jedi", 50, 40, 400, (80, 80), 1500)
        ]
