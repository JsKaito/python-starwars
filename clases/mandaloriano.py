class Mandaloriano:
    '''Representa una unidad mandaloriana.

    Args:
        mandalorianoId (int): Identificador del mandaloriano.
        name (str): Nombre del mandaloriano.
        attack (int): Poder de ataque.
        defense (int): Poder de defensa.
        hp (int): Puntos de vida.
        speed (int): Velocidad base.
        price (int): Precio del mandaloriano.
    '''

    def __init__(self, mandalorianoId, name, attack, defense, hp, speed, price):
        '''Inicializa una instancia de mandaloriano.

        Args:
            mandalorianoId (int): Identificador del mandaloriano.
            name (str): Nombre del mandaloriano.
            attack (int): Poder de ataque.
            defense (int): Poder de defensa.
            hp (int): Puntos de vida.
            speed (int): Velocidad base.
            price (int): Precio del mandaloriano.

        Returns:
            None
        '''
        self.id = mandalorianoId
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.speed = speed
        self.price = price

    @staticmethod
    def crearMandalorianos():
        '''Crea el catalogo predefinido de mandalorianos.

        Returns:
            list[Mandaloriano]: Lista de mandalorianos disponibles.
        '''
        return [
            Mandaloriano(1, "Mandaloriano 1", 20, 15, 100, 60, 800),
            Mandaloriano(2, "Mandaloriano 2", 25, 20, 120, 50, 1000),
            Mandaloriano(3, "Mandaloriano 3", 30, 25, 140, 40, 1200),
            Mandaloriano(4, "Mandaloriano 4", 35, 30, 160, 30, 1500),
            Mandaloriano(5, "Mandaloriano 5", 40, 35, 180, 20, 2000),
        ]
