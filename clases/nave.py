class Nave:
    '''Representa una nave de combate.

    Args:
        naveId (int): Identificador de la nave.
        name (str): Nombre de la nave.
        attack (int): Poder de ataque.
        defense (int): Poder de defensa.
        hp (int): Puntos de vida.
        speed (int | tuple[int, int]): Velocidad o rango de velocidad.
        price (int): Precio de la nave.
    '''

    def __init__(self, naveId, name, attack, defense, hp, speed, price):
        '''Inicializa una instancia de nave.

        Args:
            naveId (int): Identificador de la nave.
            name (str): Nombre de la nave.
            attack (int): Poder de ataque.
            defense (int): Poder de defensa.
            hp (int): Puntos de vida.
            speed (int | tuple[int, int]): Velocidad o rango de velocidad.
            price (int): Precio de la nave.

        Returns:
            None
        '''
        self.id = naveId
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.speed = speed
        self.price = price

    @staticmethod
    def crearNaves():
        '''Crea el catalogo predefinido de naves.

        Returns:
            list[Nave]: Lista de naves disponibles.
        '''
        return [
            Nave(1, "Estrella de la Muerte", 80, 90, 1500, (20, 30), 4500),
            Nave(2, "Ejecutor", 70, 80, 1200, (35, 50), 4000),
            Nave(3, "Halcon Milenario", 60, 50, 800, (70, 70), 2500),
            Nave(4, "Nave Real de Naboo", 40, 60, 600, (50, 50), 2000),
            Nave(5, "Caza Estelar Jedi", 50, 40, 400, (80, 80), 1500),
        ]
