from .Nave import Nave, tiposNave
from .Mandaloriano import Mandaloriano, tiposMandaloriano

class Reino:
    '''Representa un reino con naves y mandalorianos.

    Atributos:
        nombre (str): Nombre del reino.
        naves (list[Nave]): Lista de naves del reino.
        mandos (list[Mandaloriano]): Lista de mandalorianos del reino.
        coste (int): Coste total del reino.
    '''
    COSTE_MAX = 100000

    def __init__(self, nombre):
        '''Inicializa un reino.

        Args:
            nombre (str): Nombre del reino.
        '''
        self.nombre = nombre
        self.naves = []
        self.mandos = []
        self.coste = 0

    def añadirNave(self, tipo, cantidad):
        '''Añade naves al reino.

        Args:
            tipo: Tipo de nave (clave en tiposNave).
            cantidad (int): Número de naves a añadir.
        '''
        if tipo in tiposNave:
            ataque, defensa, vida, coste = tiposNave[tipo]
            for _ in range(cantidad):
                if self.coste + coste <= self.COSTE_MAX:
                    self.naves.append(Nave(tipo, ataque, defensa, vida, coste))
                    self.coste += coste

    def añadirMandaloriano(self, nivel, cantidad):
        '''Añade mandalorianos al reino.

        Args:
            nivel: Nivel del mandaloriano (clave en tiposMandaloriano).
            cantidad (int): Número de mandalorianos a añadir.
        '''
        if nivel in tiposMandaloriano:
            ataque, defensa, vida, coste = tiposMandaloriano[nivel]
            for _ in range(cantidad):
                if self.coste + coste <= self.COSTE_MAX:
                    self.mandos.append(Mandaloriano(nivel, ataque, defensa, vida, coste))
                    self.coste += coste

    def unidades_activas(self):
        '''Devuelve las unidades activas del reino.

        Returns:
            list[tuple[str, Nave|Mandaloriano]]: Lista de tuplas con tipo y objeto activo.
        '''
        resultado = []
        for n in self.naves:
            if n.activa:
                resultado.append(("Nave", n))
        for m in self.mandos:
            if m.activo:
                resultado.append(("Mandaloriano", m))
        return resultado

    def derrotado(self):
        '''Indica si el reino está derrotado (sin unidades activas).

        Returns:
            bool: True si el reino está derrotado.
        '''
        return len(self.unidades_activas()) == 0
