import random as rd
import socket
import threading
from clases.nave import Nave
from clases.mandaloriano import Mandaloriano

UMBRAL_VELOCIDAD_ATAQUE = 60


def recibirEnteroNoNegativo(sock):
    '''Recibe un entero no negativo desde un socket.

    Args:
        sock (socket.socket): Socket conectado al cliente.

    Returns:
        int: Valor entero no negativo recibido.
    '''
    try:
        valor = int(sock.recv(1024).decode("utf-8").strip())
        return max(0, valor)
    except (ValueError, TypeError):
        return 0


def recibirConfiguracionReino(sock, indiceReino, reinos, catalogoNaves, catalogoMandalorianos):
    '''Recibe la configuracion completa de un reino en paralelo.

    Args:
        sock (socket.socket): Socket conectado al cliente.
        indiceReino (int): Posicion del reino en la lista compartida.
        reinos (list[dict | None]): Lista de configuraciones de reinos.
        catalogoNaves (list[Nave]): Catalogo de naves disponibles.
        catalogoMandalorianos (list[Mandaloriano]): Catalogo de mandalorianos disponibles.

    Returns:
        None
    '''
    nombre = sock.recv(1024).decode("utf-8")

    cantidadesNaves = []
    for nave in catalogoNaves:
        pregunta = f"PREGUNTA_NAVE|{nave.name}|{nave.price}"
        sock.send(pregunta.encode("utf-8"))
        cantidad = recibirEnteroNoNegativo(sock)
        cantidadesNaves.append(cantidad)

    cantidadesMandalorianos = []
    for mandaloriano in catalogoMandalorianos:
        pregunta = (
            f"PREGUNTA_MANDALORIANO|{mandaloriano.name}|"
            f"{mandaloriano.id}|{mandaloriano.price}"
        )
        sock.send(pregunta.encode("utf-8"))
        cantidad = recibirEnteroNoNegativo(sock)
        cantidadesMandalorianos.append(cantidad)

    costeTotal = calcularCosteTotal(
        cantidadesNaves,
        cantidadesMandalorianos,
        catalogoNaves,
        catalogoMandalorianos,
    )

    reinos[indiceReino] = {
        "nombre": nombre,
        "cantidadesNaves": cantidadesNaves,
        "cantidadesMandalorianos": cantidadesMandalorianos,
        "costeTotal": costeTotal,
    }

    sock.send(f"COSTE_{costeTotal}".encode("utf-8"))
    sock.send(b"ESPERANDO_RIVAL")


def correrServidorTcpBasico():
    '''Inicia el servidor TCP basico y ejecuta la batalla final.

    Returns:
        None
    '''
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipServidor = "127.0.0.1"
    puerto = 8000
    servidor.bind((ipServidor, puerto))
    servidor.listen(2)
    print(f"Escuchando en {ipServidor}:{puerto}")

    clientes = []
    for _ in range(2):
        sock, addr = servidor.accept()
        print(f"Conexion aceptada de {addr[0]}:{addr[1]}")
        clientes.append(sock)

    catalogoNaves = Nave.crearNaves()
    catalogoMandalorianos = Mandaloriano.crearMandalorianos()
    reinos = [None, None]
    hilos = []

    for indice, sock in enumerate(clientes):
        hilo = threading.Thread(
            target=recibirConfiguracionReino,
            args=(sock, indice, reinos, catalogoNaves, catalogoMandalorianos),
        )
        hilo.start()
        hilos.append(hilo)

    for hilo in hilos:
        hilo.join()

    for sock in clientes:
        sock.send(b"INICIANDO_BATALLA")

    print("Ambos reinos recibidos desde los clientes. Iniciando batalla...")
    imprimirConfiguracionReino(1, reinos[0], catalogoNaves, catalogoMandalorianos)
    print("=" * 40)
    imprimirConfiguracionReino(2, reinos[1], catalogoNaves, catalogoMandalorianos)

    unidadesReino1 = crearUnidadesReino(
        reinos[0]["nombre"],
        reinos[0]["cantidadesNaves"],
        reinos[0]["cantidadesMandalorianos"],
        catalogoNaves,
        catalogoMandalorianos,
    )
    unidadesReino2 = crearUnidadesReino(
        reinos[1]["nombre"],
        reinos[1]["cantidadesNaves"],
        reinos[1]["cantidadesMandalorianos"],
        catalogoNaves,
        catalogoMandalorianos,
    )

    estadoInicialReino1 = contarEstado(unidadesReino1)
    estadoInicialReino2 = contarEstado(unidadesReino2)

    turno = 0
    while not reinoDerrotado(unidadesReino1) and not reinoDerrotado(unidadesReino2):
        turno += 1
        procesarTurno(unidadesReino1, unidadesReino2)

    navesFinal1, mandalFinal1 = contarEstado(unidadesReino1)
    navesFinal2, mandalFinal2 = contarEstado(unidadesReino2)
    navesInicial1, mandalInicial1 = estadoInicialReino1
    navesInicial2, mandalInicial2 = estadoInicialReino2
    perdidasNaves1 = navesInicial1 - navesFinal1
    perdidasMandal1 = mandalInicial1 - mandalFinal1
    perdidasNaves2 = navesInicial2 - navesFinal2
    perdidasMandal2 = mandalInicial2 - mandalFinal2

    if reinoDerrotado(unidadesReino1) and reinoDerrotado(unidadesReino2):
        ganador = "EMPATE"
    elif reinoDerrotado(unidadesReino2):
        ganador = reinos[0]["nombre"]
    else:
        ganador = reinos[1]["nombre"]

    print("=== RESULTADO FINAL DE LA GUERRA ===")
    print(f"GANADOR: {ganador}")
    print(
        f"Perdidas {reinos[0]['nombre']}: {perdidasNaves1} naves y {perdidasMandal1} mandalorianos"
    )
    print(
        f"Perdidas {reinos[1]['nombre']}: {perdidasNaves2} naves y {perdidasMandal2} mandalorianos"
    )

    mensajeResultado = f"RESULTADO|{ganador}|{turno}"
    for sock in clientes:
        sock.send(mensajeResultado.encode("utf-8"))

    for sock in clientes:
        sock.close()
    servidor.close()


def mostrarMenuPrincipal():
    '''Muestra el menu principal del servidor y solicita una opcion.

    Returns:
        bool: True si la opcion es valida.
    '''
    print("Simulacion de Batalla")
    print("=== SERVIDOR - LA GUERRA DE LAS GALAXIAS (2026) ===")
    print("1. Iniciar Guerra")
    print("2. Finalizar Servidor")
    opcion = input("Seleccionar opcion para continuar: ").strip()
    return opcion in {"1", "3"}


def esperarConexionReino(numeroReino):
    '''Muestra el estado de espera de conexion de un reino.

    Args:
        numeroReino (int): Numero del reino esperado.

    Returns:
        None
    '''
    print(f"Esperando conexion de Reino {numeroReino}... [CONECTADO]")


def generarCantidades(cantidadTipos, minimo, maximo):
    '''Genera cantidades aleatorias para cada tipo de unidad.

    Args:
        cantidadTipos (int): Cantidad de tipos a generar.
        minimo (int): Valor minimo por tipo.
        maximo (int): Valor maximo por tipo.

    Returns:
        list[int]: Cantidades generadas.
    '''
    return [rd.randint(minimo, maximo) for _ in range(cantidadTipos)]


def calcularCosteTotal(cantidadesNaves, cantidadesMandalorianos, catalogoNaves, catalogoMandalorianos):
    '''Calcula el coste total de la configuracion de un reino.

    Args:
        cantidadesNaves (list[int]): Cantidades por tipo de nave.
        cantidadesMandalorianos (list[int]): Cantidades por tipo de mandaloriano.
        catalogoNaves (list[Nave]): Catalogo de naves.
        catalogoMandalorianos (list[Mandaloriano]): Catalogo de mandalorianos.

    Returns:
        int: Coste total calculado.
    '''
    costeNaves = 0
    for indice, cantidad in enumerate(cantidadesNaves):
        costeNaves += cantidad * catalogoNaves[indice].price

    costeMandalorianos = 0
    for indice, cantidad in enumerate(cantidadesMandalorianos):
        costeMandalorianos += cantidad * catalogoMandalorianos[indice].price

    return costeNaves + costeMandalorianos


def configurarReino(nombreReino, catalogoNaves, catalogoMandalorianos):
    '''Construye una configuracion de reino con cantidades aleatorias.

    Args:
        nombreReino (str): Nombre del reino.
        catalogoNaves (list[Nave]): Catalogo de naves.
        catalogoMandalorianos (list[Mandaloriano]): Catalogo de mandalorianos.

    Returns:
        dict: Configuracion del reino.
    '''
    cantidadesNaves = generarCantidades(len(catalogoNaves), 8, 20)
    cantidadesMandalorianos = generarCantidades(len(catalogoMandalorianos), 10, 35)
    costeTotal = calcularCosteTotal(
        cantidadesNaves,
        cantidadesMandalorianos,
        catalogoNaves,
        catalogoMandalorianos,
    )

    return {
        "nombre": nombreReino,
        "cantidadesNaves": cantidadesNaves,
        "cantidadesMandalorianos": cantidadesMandalorianos,
        "costeTotal": costeTotal,
    }


def imprimirConfiguracionReino(numeroReino, configuracionReino, catalogoNaves, catalogoMandalorianos):
    '''Imprime la configuracion de un reino.

    Args:
        numeroReino (int): Numero identificador del reino.
        configuracionReino (dict): Configuracion del reino.
        catalogoNaves (list[Nave]): Catalogo de naves.
        catalogoMandalorianos (list[Mandaloriano]): Catalogo de mandalorianos.

    Returns:
        None
    '''
    print("=" * 40)
    print(f"CONFIGURACION REINO {numeroReino}")
    print("=" * 40)
    print(f"Nombre del Reino: {configuracionReino['nombre']}")

    for indice, nave in enumerate(catalogoNaves):
        cantidad = configuracionReino["cantidadesNaves"][indice]
        print(f"Numero de Naves ({nave.name}): {cantidad}")

    for indice, mandaloriano in enumerate(catalogoMandalorianos):
        cantidad = configuracionReino["cantidadesMandalorianos"][indice]
        print(f"Numero de Mandalorianos (Nivel {mandaloriano.id}): {cantidad}")

    print(f"Coste total: {configuracionReino['costeTotal']} Creditos")


def velocidadBaseUnidad(unidadBase):
    '''Calcula la velocidad base de una unidad.

    Args:
        unidadBase (Nave | Mandaloriano): Unidad base a evaluar.

    Returns:
        int: Velocidad base de la unidad.
    '''
    if isinstance(unidadBase.speed, tuple):
        return rd.randint(unidadBase.speed[0], unidadBase.speed[1])
    return int(unidadBase.speed)


def crearUnidadesReino(nombreReino, cantidadesNaves, cantidadesMandalorianos, catalogoNaves, catalogoMandalorianos):
    '''Crea todas las unidades de un reino para la batalla.

    Args:
        nombreReino (str): Nombre del reino.
        cantidadesNaves (list[int]): Cantidades por tipo de nave.
        cantidadesMandalorianos (list[int]): Cantidades por tipo de mandaloriano.
        catalogoNaves (list[Nave]): Catalogo de naves.
        catalogoMandalorianos (list[Mandaloriano]): Catalogo de mandalorianos.

    Returns:
        list[dict]: Lista de unidades creadas.
    '''
    unidades = []
    contadorNaves = 1

    for indice, cantidad in enumerate(cantidadesNaves):
        naveBase = catalogoNaves[indice]
        for _ in range(cantidad):
            unidades.append(
                {
                    "reino": nombreReino,
                    "categoria": "Nave",
                    "nombre": naveBase.name,
                    "ataque": naveBase.attack,
                    "defensa": naveBase.defense,
                    "vidaMaxima": naveBase.hp,
                    "vidaActual": naveBase.hp,
                    "velocidadBase": velocidadBaseUnidad(naveBase),
                    "velocidadAcumulada": 0,
                    "idNave": contadorNaves,
                }
            )
            contadorNaves += 1

    for indice, cantidad in enumerate(cantidadesMandalorianos):
        mandalorianoBase = catalogoMandalorianos[indice]
        for _ in range(cantidad):
            unidades.append(
                {
                    "reino": nombreReino,
                    "categoria": "Mandaloriano",
                    "nombre": mandalorianoBase.name,
                    "ataque": mandalorianoBase.attack,
                    "defensa": mandalorianoBase.defense,
                    "vidaMaxima": mandalorianoBase.hp,
                    "vidaActual": mandalorianoBase.hp,
                    "velocidadBase": velocidadBaseUnidad(mandalorianoBase),
                    "velocidadAcumulada": 0,
                }
            )

    return unidades


def unidadesVivas(unidades):
    '''Filtra las unidades que aun tienen vida.

    Args:
        unidades (list[dict]): Unidades del reino.

    Returns:
        list[dict]: Unidades vivas.
    '''
    return [unidad for unidad in unidades if unidad["vidaActual"] > 0]


def contarEstado(unidades):
    '''Cuenta naves y mandalorianos vivos.

    Args:
        unidades (list[dict]): Unidades del reino.

    Returns:
        tuple[int, int]: Cantidad de naves y mandalorianos vivos.
    '''
    naves = sum(
        1 for unidad in unidades if unidad["categoria"] == "Nave" and unidad["vidaActual"] > 0
    )
    mandalorianos = sum(
        1
        for unidad in unidades
        if unidad["categoria"] == "Mandaloriano" and unidad["vidaActual"] > 0
    )
    return naves, mandalorianos


def truncar(texto, largoMaximo):
    '''Devuelve un texto truncado al largo maximo indicado.

    Args:
        texto (str): Texto a truncar.
        largoMaximo (int): Largo maximo permitido.

    Returns:
        str: Texto truncado.
    '''
    if len(texto) <= largoMaximo:
        return texto
    return texto[:largoMaximo]


def imprimirEstadoTabla(nombreReino1, nombreReino2, unidadesReino1, unidadesReino2, titulo):
    '''Imprime una tabla con el estado de ambos reinos.

    Args:
        nombreReino1 (str): Nombre del primer reino.
        nombreReino2 (str): Nombre del segundo reino.
        unidadesReino1 (list[dict]): Unidades del primer reino.
        unidadesReino2 (list[dict]): Unidades del segundo reino.
        titulo (str): Titulo de la tabla.

    Returns:
        None
    '''
    naves1, mandal1 = contarEstado(unidadesReino1)
    naves2, mandal2 = contarEstado(unidadesReino2)

    print(titulo)
    print("+---------------------------+--------------+-----------------+")
    print("| REINO                     |    NAVES     | MANDALORIANOS   |")
    print("+---------------------------+--------------+-----------------+")
    print(f"| {nombreReino1:<25} | {naves1:^12} | {mandal1:^15} |")
    print(f"| {nombreReino2:<25} | {naves2:^12} | {mandal2:^15} |")
    print("+---------------------------+--------------+-----------------+")


def calcularDanio(atacante, objetivo):
    '''Calcula el dano infligido por un atacante.

    Args:
        atacante (dict): Unidad atacante.
        objetivo (dict): Unidad objetivo.

    Returns:
        int: Dano calculado.
    '''
    fuerzaAtaque = atacante["ataque"] * rd.uniform(0.90, 1.25)
    mitigacionDefensa = objetivo["defensa"] * rd.uniform(0.35, 0.55)
    return max(1, int(fuerzaAtaque - mitigacionDefensa))


def ejecutarAtaque(atacante, objetivo):
    '''Ejecuta un ataque y devuelve su descripcion.

    Args:
        atacante (dict): Unidad atacante.
        objetivo (dict): Unidad objetivo.

    Returns:
        str: Texto del resultado del ataque.
    '''
    danio = calcularDanio(atacante, objetivo)
    objetivo["vidaActual"] = max(0, objetivo["vidaActual"] - danio)

    if atacante["categoria"] == "Nave":
        nombreAtacante = f"{atacante['nombre']} #{atacante['idNave']}"
    else:
        nombreAtacante = atacante["nombre"]

    if objetivo["categoria"] == "Nave" and "idNave" in objetivo:
        nombreObjetivo = f"{objetivo['nombre']} #{objetivo['idNave']}"
    else:
        nombreObjetivo = objetivo["nombre"]

    textoBase = (
        f"{nombreAtacante} ({atacante['reino']}) -> "
        f"{nombreObjetivo} ({objetivo['reino']}) [DANO: {danio}]"
    )

    if objetivo["vidaActual"] == 0:
        return textoBase + " - DESTRUIDO/ELIMINADO"
    return textoBase + f" - HERIDO (Vida: {objetivo['vidaActual']}/{objetivo['vidaMaxima']})"


def procesarTurno(unidadesReino1, unidadesReino2):
    '''Procesa un turno de combate entre dos reinos.

    Args:
        unidadesReino1 (list[dict]): Unidades del primer reino.
        unidadesReino2 (list[dict]): Unidades del segundo reino.

    Returns:
        list[str]: Eventos generados en el turno.
    '''
    eventosTurno = []

    for unidad in unidadesVivas(unidadesReino1) + unidadesVivas(unidadesReino2):
        unidad["velocidadAcumulada"] += unidad["velocidadBase"]

    combatientes = unidadesVivas(unidadesReino1) + unidadesVivas(unidadesReino2)
    rd.shuffle(combatientes)
    combatientes.sort(key=lambda unidad: unidad["velocidadAcumulada"], reverse=True)

    for atacante in combatientes:
        if atacante["vidaActual"] <= 0:
            continue

        if atacante["reino"] == unidadesReino1[0]["reino"]:
            enemigos = unidadesVivas(unidadesReino2)
        else:
            enemigos = unidadesVivas(unidadesReino1)

        while atacante["velocidadAcumulada"] >= UMBRAL_VELOCIDAD_ATAQUE and enemigos:
            objetivo = rd.choice(enemigos)
            eventosTurno.append(ejecutarAtaque(atacante, objetivo))
            atacante["velocidadAcumulada"] -= UMBRAL_VELOCIDAD_ATAQUE
            enemigos = [enemigo for enemigo in enemigos if enemigo["vidaActual"] > 0]

    return eventosTurno


def reinoDerrotado(unidades):
    '''Determina si un reino fue derrotado.

    Args:
        unidades (list[dict]): Unidades del reino.

    Returns:
        bool: True si no quedan unidades vivas.
    '''
    return len(unidadesVivas(unidades)) == 0


def imprimirResultadoFinal(
    nombreReino1,
    nombreReino2,
    unidadesReino1,
    unidadesReino2,
    totalInicial1,
    totalInicial2,
    turnos,
):
    '''Imprime el resultado final de la batalla.

    Args:
        nombreReino1 (str): Nombre del primer reino.
        nombreReino2 (str): Nombre del segundo reino.
        unidadesReino1 (list[dict]): Unidades finales del primer reino.
        unidadesReino2 (list[dict]): Unidades finales del segundo reino.
        totalInicial1 (tuple[int, int]): Estado inicial del primer reino.
        totalInicial2 (tuple[int, int]): Estado inicial del segundo reino.
        turnos (int): Turnos jugados.

    Returns:
        None
    '''
    navesFinal1, mandalFinal1 = contarEstado(unidadesReino1)
    navesFinal2, mandalFinal2 = contarEstado(unidadesReino2)

    navesInicial1, mandalInicial1 = totalInicial1
    navesInicial2, mandalInicial2 = totalInicial2

    perdidasNaves1 = navesInicial1 - navesFinal1
    perdidasMandal1 = mandalInicial1 - mandalFinal1
    perdidasNaves2 = navesInicial2 - navesFinal2
    perdidasMandal2 = mandalInicial2 - mandalFinal2

    if reinoDerrotado(unidadesReino1) and reinoDerrotado(unidadesReino2):
        ganador = "EMPATE"
    elif reinoDerrotado(unidadesReino2):
        ganador = nombreReino1
    else:
        ganador = nombreReino2

    print("=== RESULTADO FINAL DE LA GUERRA ===")
    print(f"GANADOR: {ganador}")
    print("ESTADISTICAS DE LA BATALLA:")
    print(
        f"{nombreReino1}: perdidas {perdidasNaves1} N/{perdidasMandal1} M, "
        f"supervivientes {navesFinal1} N/{mandalFinal1} M"
    )
    print(
        f"{nombreReino2}: perdidas {perdidasNaves2} N/{perdidasMandal2} M, "
        f"supervivientes {navesFinal2} N/{mandalFinal2} M"
    )
    costeBatalla = rd.randint(18000, 32000)
    print(f"Coste Total Batalla: {costeBatalla} Creditos Galacticos")
    print(f"Duracion: {turnos} turnos")


def iniciarGuerra():
    '''Inicia una guerra local con configuraciones aleatorias.

    Returns:
        None
    '''
    print("INICIANDO GUERRA GALACTICA")
    esperarConexionReino(1)
    esperarConexionReino(2)

    catalogoNaves = Nave.crearNaves()
    catalogoMandalorianos = Mandaloriano.crearMandalorianos()

    configuracionReino1 = configurarReino("IMPERIO GALACTICO", catalogoNaves, catalogoMandalorianos)
    configuracionReino2 = configurarReino("ALIANZA REBELDE", catalogoNaves, catalogoMandalorianos)

    imprimirConfiguracionReino(1, configuracionReino1, catalogoNaves, catalogoMandalorianos)
    print("=" * 40)
    imprimirConfiguracionReino(2, configuracionReino2, catalogoNaves, catalogoMandalorianos)

    print("Ambos Reinos configurados correctamente. INICIANDO BATALLA")
    print("=== CAMPO DE BATALLA GALACTICO ===")
    print(f"=== BATALLA: {configuracionReino1['nombre']} vs {configuracionReino2['nombre']} ===")

    unidadesReino1 = crearUnidadesReino(
        configuracionReino1["nombre"],
        configuracionReino1["cantidadesNaves"],
        configuracionReino1["cantidadesMandalorianos"],
        catalogoNaves,
        catalogoMandalorianos,
    )
    unidadesReino2 = crearUnidadesReino(
        configuracionReino2["nombre"],
        configuracionReino2["cantidadesNaves"],
        configuracionReino2["cantidadesMandalorianos"],
        catalogoNaves,
        catalogoMandalorianos,
    )

    estadoInicialReino1 = contarEstado(unidadesReino1)
    estadoInicialReino2 = contarEstado(unidadesReino2)

    print("ESTADO INICIAL:")
    imprimirEstadoTabla(
        configuracionReino1["nombre"],
        configuracionReino2["nombre"],
        unidadesReino1,
        unidadesReino2,
        "",
    )

    turno = 0
    while not reinoDerrotado(unidadesReino1) and not reinoDerrotado(unidadesReino2):
        turno += 1
        print("\n" + "=" * 60)
        print(f"TURNO {turno:02d} - COMBATES")
        print("-" * 60)

        eventos = procesarTurno(unidadesReino1, unidadesReino2)
        if not eventos:
            print("Sin combates este turno.\n")
        else:
            for indice, evento in enumerate(eventos, start=1):
                print(f" {indice:02d}. {evento}")
            print()

        imprimirEstadoTabla(
            configuracionReino1["nombre"],
            configuracionReino2["nombre"],
            unidadesReino1,
            unidadesReino2,
            f"ESTADO DESPUES DEL TURNO {turno}",
        )
        print("=" * 60 + "\n")

    imprimirResultadoFinal(
        configuracionReino1["nombre"],
        configuracionReino2["nombre"],
        unidadesReino1,
        unidadesReino2,
        estadoInicialReino1,
        estadoInicialReino2,
        turno,
    )


def ejecutarServidorPrincipal():
    '''Ejecuta el servidor principal en modo automatico.

    Returns:
        None
    '''
    print("=== SERVIDOR - LA GUERRA DE LAS GALAXIAS (2026) ===")
    print("Iniciando servidor automaticamente...")
    correrServidorTcpBasico()


if __name__ == "__main__":
    ejecutarServidorPrincipal()
