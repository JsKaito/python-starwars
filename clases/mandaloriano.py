import random as rd

class Mandaloriano:
    """Representa un Mandaloriano en el universo Star Wars."""

    def __init__(self, id, name, attack, defense, hp, speed, price):
        """Inicializa mandalorianos."""
        self.id = id
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.speed = speed
        self.price = price

    @staticmethod
    def crearMandalorianos():
        return [
            Mandaloriano(1, "Mandaloriano 1", 20, 15, 100, 60, 800),
            Mandaloriano(2, "Mandaloriano 2", 25, 20, 120, 50, 1000),
            Mandaloriano(3, "Mandaloriano 3", 30, 25, 140, 40, 1200),
            Mandaloriano(4, "Mandaloriano 4", 35, 30, 160, 30, 1500),
            Mandaloriano(5, "Mandaloriano 5", 40, 35, 180, 20, 2000)
        ]