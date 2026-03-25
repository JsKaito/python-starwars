from .Nave import Nave
from .Mandaloriano import Mandaloriano


class Reino:
    '''Representa un reino con naves y mandalorianos.

    Args:
        nombre (str): Nombre del reino.
    '''

    COSTE_MAX = 100000

    def __init__(self, nombre):
        '''Inicializa una instancia de reino.

        Args:
            nombre (str): Nombre del reino.

        Returns:
            None
        '''
        self.nombre = nombre
        self.naves = []
        self.mandos = []
        self.coste = 0

    def aniadirNave(self, tipoNaveId, cantidad):
        '''Aniade naves al reino segun el tipo y la cantidad.

        Args:
            tipoNaveId (int): Identificador del tipo de nave.
            cantidad (int): Cantidad de naves a agregar.

        Returns:
            None
        '''
        catalogoNaves = Nave.crearNaves()
        naveBase = next((nave for nave in catalogoNaves if nave.id == tipoNaveId), None)
        if naveBase is None:
            return

        for _ in range(cantidad):
            if self.coste + naveBase.price <= self.COSTE_MAX:
                self.naves.append(
                    Nave(
                        naveBase.id,
                        naveBase.name,
                        naveBase.attack,
                        naveBase.defense,
                        naveBase.hp,
                        naveBase.speed,
                        naveBase.price,
                    )
                )
                self.coste += naveBase.price

    def aniadirMandaloriano(self, nivelMandaloriano, cantidad):
        '''Aniade mandalorianos al reino segun el nivel y la cantidad.

        Args:
            nivelMandaloriano (int): Nivel del tipo de mandaloriano.
            cantidad (int): Cantidad de mandalorianos a agregar.

        Returns:
            None
        '''
        catalogoMandalorianos = Mandaloriano.crearMandalorianos()
        mandalorianoBase = next(
            (
                mandaloriano
                for mandaloriano in catalogoMandalorianos
                if mandaloriano.id == nivelMandaloriano
            ),
            None,
        )
        if mandalorianoBase is None:
            return

        for _ in range(cantidad):
            if self.coste + mandalorianoBase.price <= self.COSTE_MAX:
                self.mandos.append(
                    Mandaloriano(
                        mandalorianoBase.id,
                        mandalorianoBase.name,
                        mandalorianoBase.attack,
                        mandalorianoBase.defense,
                        mandalorianoBase.hp,
                        mandalorianoBase.speed,
                        mandalorianoBase.price,
                    )
                )
                self.coste += mandalorianoBase.price

    def unidadesActivas(self):
        '''Devuelve las unidades activas del reino.

        Returns:
            list[tuple[str, Nave | Mandaloriano]]: Unidades actualmente activas.
        '''
        resultado = []
        for nave in self.naves:
            if getattr(nave, "activa", True):
                resultado.append(("Nave", nave))
        for mandaloriano in self.mandos:
            if getattr(mandaloriano, "activo", True):
                resultado.append(("Mandaloriano", mandaloriano))
        return resultado

    def estaDerrotado(self):
        '''Indica si el reino se encuentra derrotado.

        Returns:
            bool: True cuando no hay unidades activas.
        '''
        return len(self.unidadesActivas()) == 0
