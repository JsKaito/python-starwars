class Nave:
    """Representa una nave en el universo Star Wars."""

    def __init__(self, nombre, ataque, defensa, vida, velocidad, coste):
        """Inicializa una nave."""
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.vida = vida
        self.velocidad = velocidad
        self.coste = coste