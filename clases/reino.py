from .nave import Nave, tiposNave
from .mandaloriano import Mandaloriano, tiposMandaloriano

class Reino:
    costeMaximo = 100000
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.naves = []
        self.mandos = []
        self.coste = 0
    
    def añadirNave(self, tipo, cantidad):
        if tipo in tiposNave:
            ataque, defensa, vida, coste = tiposNave[tipo]
            for _ in range(cantidad):
                if self.coste + coste <= self.COSTE_MAX:
                    self.naves.append(Nave(tipo, ataque, defensa, vida, coste))
                    self.coste += coste
    
    def añadirMandaloriano(self, nivel, cantidad):
        if nivel in tiposMandaloriano:
            ataque, defensa, vida, coste = tiposMandaloriano[nivel]
            for _ in range(cantidad):
                if self.coste + coste <= self.COSTE_MAX:
                    self.mandos.append(Mandaloriano(nivel, ataque, defensa, vida, coste))
                    self.coste += coste
    
    def unidades_activas(self):
        resultado = []
        for n in self.naves:
            if n.activa:
                resultado.append(("Nave", n))
        for m in self.mandos:
            if m.activo:
                resultado.append(("Mandaloriano", m))
        return resultado
    
    def derrotado(self):
        return len(self.unidades_activas()) == 0