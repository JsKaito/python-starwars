import random as rd
import socket
from clases.nave import Nave
from clases.mandaloriano import Mandaloriano

UMBRAL_VELOCIDAD_ATAQUE = 60


def correr_servidor_tcp_basico():
    '''Servidor TCP básico para pruebas de conexión.

    Returns:
        None
    '''
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_servidor = "127.0.0.1"
    puerto = 8000

    servidor.bind((ip_servidor, puerto))
    servidor.listen(1)
    print(f"Escuchando en {ip_servidor}:{puerto}")

    socket_cliente, direccion_cliente = servidor.accept()
    print(f"Conexión aceptada de {direccion_cliente[0]}:{direccion_cliente[1]}")

    while True:
        solicitud = socket_cliente.recv(1024).decode("utf-8")
        if solicitud.lower() == "close":
            socket_cliente.send("closed".encode("utf-8"))
            break

        print(f"Recibido: {solicitud}")
        socket_cliente.send("accepted".encode("utf-8"))

    socket_cliente.close()
    servidor.close()


def mostrar_menu_principal():
    '''Muestra el menú principal del servidor y solicita una opción al usuario.

    Returns:
        bool: True si la opción es válida, False en caso contrario.
    '''
    print("Simulación de Batalla (Ejemplo)")
    print("=== SERVIDOR - LA GUERRA DE LAS GALAXIAS (2026) ===")
    print("1. Iniciar Guerra")
    print("2. Finalizar Servidor")
    opcion = input("Seleccionar opción para continuar: ").strip()

    return opcion in {"1", "3"}


def esperar_conexion_reino(numero_reino):
    '''Espera la conexión de un reino específico.

    Args:
        numero_reino (int): Número identificador del reino a esperar.

    Returns:
        None
    '''
    print(f"Esperando conexión de Reino {numero_reino}... [CONECTADO]")


def generar_cantidades(cantidad_tipos, minimo, maximo):
    '''Genera una lista de cantidades aleatorias entre un mínimo y máximo para cada tipo.

    Args:
        cantidad_tipos (int): Número de tipos a generar.
        minimo (int): Valor mínimo por tipo.
        maximo (int): Valor máximo por tipo.

    Returns:
        list[int]: Lista de cantidades generadas.
    '''
    return [rd.randint(minimo, maximo) for _ in range(cantidad_tipos)]


def calcular_coste_total(cantidades_naves, cantidades_mandalorianos, catalogo_naves, catalogo_mandalorianos):
    '''Calcula el coste total de naves y mandalorianos según sus cantidades y catálogos.

    Args:
        cantidades_naves (list[int]): Cantidades de cada tipo de nave.
        cantidades_mandalorianos (list[int]): Cantidades de cada tipo de mandaloriano.
        catalogo_naves (list[Nave]): Catálogo de objetos Nave.
        catalogo_mandalorianos (list[Mandaloriano]): Catálogo de objetos Mandaloriano.

    Returns:
        int: Coste total.
    '''
    coste_naves = 0
    for indice, cantidad in enumerate(cantidades_naves):
        coste_naves += cantidad * catalogo_naves[indice].price

    coste_mandalorianos = 0
    for indice, cantidad in enumerate(cantidades_mandalorianos):
        coste_mandalorianos += cantidad * catalogo_mandalorianos[indice].price

    return coste_naves + coste_mandalorianos


def configurar_reino(nombre_reino, catalogo_naves, catalogo_mandalorianos):
    '''Configura un reino generando cantidades y coste total de naves y mandalorianos.

    Args:
        nombre_reino (str): Nombre del reino.
        catalogo_naves (list[Nave]): Catálogo de naves.
        catalogo_mandalorianos (list[Mandaloriano]): Catálogo de mandalorianos.

    Returns:
        dict: Configuración del reino.
    '''
    cantidades_naves = generar_cantidades(len(catalogo_naves), 8, 20)
    cantidades_mandalorianos = generar_cantidades(len(catalogo_mandalorianos), 10, 35)

    coste_total = calcular_coste_total(
        cantidades_naves,
        cantidades_mandalorianos,
        catalogo_naves,
        catalogo_mandalorianos,
    )

    return {
        "nombre": nombre_reino,
        "cantidades_naves": cantidades_naves,
        "cantidades_mandalorianos": cantidades_mandalorianos,
        "coste_total": coste_total,
    }


def imprimir_configuracion_reino(numero_reino, configuracion_reino, catalogo_naves, catalogo_mandalorianos):
    '''Imprime la configuración de un reino, mostrando cantidades y coste total.

    Args:
        numero_reino (int): Número identificador del reino.
        configuracion_reino (dict): Configuración del reino.
        catalogo_naves (list[Nave]): Catálogo de naves.
        catalogo_mandalorianos (list[Mandaloriano]): Catálogo de mandalorianos.

    Returns:
        None
    '''
    print("=" * 40)
    print(f"CONFIGURACIÓN REINO {numero_reino}")
    print("=" * 40)
    print(f"Nombre del Reino: {configuracion_reino['nombre']}")

    for indice, nave in enumerate(catalogo_naves):
        cantidad = configuracion_reino["cantidades_naves"][indice]
        print(f"Número de Naves ({nave.name}): {cantidad}")

    for indice, mandaloriano in enumerate(catalogo_mandalorianos):
        cantidad = configuracion_reino["cantidades_mandalorianos"][indice]
        print(f"Número de Mandalorianos (Nivel {mandaloriano.id}): {cantidad}")

    print(f"Coste total: {configuracion_reino['coste_total']} Créditos")


def velocidad_base_unidad(unidad_base):
    '''Calcula la velocidad base de una unidad (aleatoria si es un rango).

    Args:
        unidad_base (Nave | Mandaloriano): Objeto base de la unidad.

    Returns:
        int: Velocidad base calculada.
    '''
    if isinstance(unidad_base.speed, tuple):
        return rd.randint(unidad_base.speed[0], unidad_base.speed[1])
    return int(unidad_base.speed)


def crear_unidades_reino(nombre_reino, cantidades_naves, cantidades_mandalorianos, catalogo_naves, catalogo_mandalorianos):
    '''Crea la lista de unidades (naves y mandalorianos) para un reino.

    Args:
        nombre_reino (str): Nombre del reino.
        cantidades_naves (list[int]): Cantidades de cada tipo de nave.
        cantidades_mandalorianos (list[int]): Cantidades de cada tipo de mandaloriano.
        catalogo_naves (list[Nave]): Catálogo de naves.
        catalogo_mandalorianos (list[Mandaloriano]): Catálogo de mandalorianos.

    Returns:
        list[dict]: Lista de unidades generadas.
    '''
    unidades = []
    contador_naves = 1
    contador_mandalorianos = 1

    for indice, cantidad in enumerate(cantidades_naves):
        nave_base = catalogo_naves[indice]
        for _ in range(cantidad):
            unidades.append(
                {
                    "reino": nombre_reino,
                    "categoria": "Nave",
                    "nombre": nave_base.name,
                    "ataque": nave_base.attack,
                    "defensa": nave_base.defense,
                    "vida_maxima": nave_base.hp,
                    "vida_actual": nave_base.hp,
                    "velocidad_base": velocidad_base_unidad(nave_base),
                    "velocidad_acumulada": 0,
                    "id_nave": contador_naves,
                }
            )
            contador_naves += 1

    for indice, cantidad in enumerate(cantidades_mandalorianos):
        mandaloriano_base = catalogo_mandalorianos[indice]
        for _ in range(cantidad):
            unidades.append(
                {
                    "reino": nombre_reino,
                    "categoria": "Mandaloriano",
                    "nombre": mandaloriano_base.name,
                    "ataque": mandaloriano_base.attack,
                    "defensa": mandaloriano_base.defense,
                    "vida_maxima": mandaloriano_base.hp,
                    "vida_actual": mandaloriano_base.hp,
                    "velocidad_base": velocidad_base_unidad(mandaloriano_base),
                    "velocidad_acumulada": 0,
                }
            )
            contador_mandalorianos += 1

    return unidades


def unidades_vivas(unidades):
    '''Devuelve una lista de unidades vivas (vida_actual > 0).

    Args:
        unidades (list[dict]): Lista de unidades.

    Returns:
        list[dict]: Unidades vivas.
    '''
    return [unidad for unidad in unidades if unidad["vida_actual"] > 0]


def contar_estado(unidades):
    '''Cuenta cuántas naves y mandalorianos vivos hay en la lista de unidades.

    Args:
        unidades (list[dict]): Lista de unidades.

    Returns:
        tuple[int, int]: (naves vivas, mandalorianos vivos).
    '''
    naves = sum(1 for unidad in unidades if unidad["categoria"] == "Nave" and unidad["vida_actual"] > 0)
    mandalorianos = sum(1 for unidad in unidades if unidad["categoria"] == "Mandaloriano" and unidad["vida_actual"] > 0)
    return naves, mandalorianos


def truncar(texto, largo_maximo):
    '''Trunca un texto a un largo máximo (sin uso actual).

    Args:
        texto (str): Texto a truncar.
        largo_maximo (int): Longitud máxima.

    Returns:
        str: Texto truncado.
    '''
    return texto


def imprimir_estado_tabla(nombre_reino_1, nombre_reino_2, unidades_reino_1, unidades_reino_2, titulo):
    '''Imprime una tabla con el estado actual de ambos reinos (naves y mandalorianos vivos).

    Args:
        nombre_reino_1 (str): Nombre del primer reino.
        nombre_reino_2 (str): Nombre del segundo reino.
        unidades_reino_1 (list[dict]): Unidades del primer reino.
        unidades_reino_2 (list[dict]): Unidades del segundo reino.
        titulo (str): Título de la tabla.

    Returns:
        None
    '''
    naves_1, mandal_1 = contar_estado(unidades_reino_1)
    naves_2, mandal_2 = contar_estado(unidades_reino_2)

    print(titulo)
    print("┌{0}┬{1}┬{2}┐".format("─"*25, "─"*14, "─"*17))
    print("│ {0:<23} │ {1:^12} │ {2:^15} │".format("REINO", "NAVES", "MANDALORIANOS"))
    print("├{0}┼{1}┼{2}┤".format("─"*25, "─"*14, "─"*17))
    print(f"│ {nombre_reino_1:<23} │ {naves_1:^12} │ {mandal_1:^15} │")
    print(f"│ {nombre_reino_2:<23} │ {naves_2:^12} │ {mandal_2:^15} │")
    print("└{0}┴{1}┴{2}┘".format("─"*25, "─"*14, "─"*17))


def calcular_daño(atacante, objetivo):
    '''Calcula el daño infligido por un atacante a un objetivo.

    Args:
        atacante (dict): Unidad atacante.
        objetivo (dict): Unidad objetivo.

    Returns:
        int: Daño calculado.
    '''
    fuerza_ataque = atacante["ataque"] * rd.uniform(0.90, 1.25)
    mitigacion_defensa = objetivo["defensa"] * rd.uniform(0.35, 0.55)
    daño = max(1, int(fuerza_ataque - mitigacion_defensa))
    return daño


def ejecutar_ataque(atacante, objetivo):
    '''Ejecuta un ataque de una unidad a otra y actualiza la vida del objetivo.

    Args:
        atacante (dict): Unidad atacante.
        objetivo (dict): Unidad objetivo.

    Returns:
        str: Descripción del resultado del ataque.
    '''
    daño = calcular_daño(atacante, objetivo)
    objetivo["vida_actual"] = max(0, objetivo["vida_actual"] - daño)

    if atacante["categoria"] == "Nave":
        nombre_atacante = f"{atacante['nombre']} #{atacante['id_nave']}"
    else:
        nombre_atacante = atacante['nombre']

    if objetivo["categoria"] == "Nave" and "id_nave" in objetivo:
        nombre_objetivo = f"{objetivo['nombre']} #{objetivo['id_nave']}"
    else:
        nombre_objetivo = objetivo['nombre']

    texto_base = (
        f"{nombre_atacante} ({atacante['reino']}) -> "
        f"{nombre_objetivo} ({objetivo['reino']}) [DAÑO: {daño}]"
    )

    if objetivo["vida_actual"] == 0:
        return texto_base + " - DESTRUIDO/ELIMINADO"

    return (
        texto_base
        + f" - HERIDO (Vida: {objetivo['vida_actual']}/{objetivo['vida_maxima']})"
    )


def procesar_turno(unidades_reino_1, unidades_reino_2):
    '''Procesa un turno de combate entre dos reinos y devuelve los eventos ocurridos.

    Args:
        unidades_reino_1 (list[dict]): Unidades del primer reino.
        unidades_reino_2 (list[dict]): Unidades del segundo reino.

    Returns:
        list[str]: Eventos del turno.
    '''
    eventos_turno = []

    for unidad in unidades_vivas(unidades_reino_1) + unidades_vivas(unidades_reino_2):
        unidad["velocidad_acumulada"] += unidad["velocidad_base"]

    combatientes = unidades_vivas(unidades_reino_1) + unidades_vivas(unidades_reino_2)
    rd.shuffle(combatientes)
    combatientes.sort(key=lambda unidad: unidad["velocidad_acumulada"], reverse=True)

    for atacante in combatientes:
        if atacante["vida_actual"] <= 0:
            continue

        if atacante["reino"] == unidades_reino_1[0]["reino"]:
            enemigos = unidades_vivas(unidades_reino_2)
        else:
            enemigos = unidades_vivas(unidades_reino_1)

        while atacante["velocidad_acumulada"] >= UMBRAL_VELOCIDAD_ATAQUE and enemigos:
            objetivo = rd.choice(enemigos)
            eventos_turno.append(ejecutar_ataque(atacante, objetivo))
            atacante["velocidad_acumulada"] -= UMBRAL_VELOCIDAD_ATAQUE
            enemigos = [enemigo for enemigo in enemigos if enemigo["vida_actual"] > 0]

    return eventos_turno


def reino_derrotado(unidades):
    '''Determina si un reino ha sido derrotado (sin unidades vivas).

    Args:
        unidades (list[dict]): Unidades del reino.

    Returns:
        bool: True si el reino está derrotado.
    '''
    return len(unidades_vivas(unidades)) == 0


def imprimir_resultado_final(nombre_reino_1, nombre_reino_2, unidades_reino_1, unidades_reino_2, total_inicial_1, total_inicial_2, turnos):
    '''Imprime el resultado final de la guerra, mostrando estadísticas y el ganador.

    Args:
        nombre_reino_1 (str): Nombre del primer reino.
        nombre_reino_2 (str): Nombre del segundo reino.
        unidades_reino_1 (list[dict]): Unidades finales del primer reino.
        unidades_reino_2 (list[dict]): Unidades finales del segundo reino.
        total_inicial_1 (tuple[int, int]): Estado inicial del primer reino.
        total_inicial_2 (tuple[int, int]): Estado inicial del segundo reino.
        turnos (int): Número de turnos de la batalla.

    Returns:
        None
    '''
    naves_final_1, mandal_final_1 = contar_estado(unidades_reino_1)
    naves_final_2, mandal_final_2 = contar_estado(unidades_reino_2)

    naves_inicial_1, mandal_inicial_1 = total_inicial_1
    naves_inicial_2, mandal_inicial_2 = total_inicial_2

    perdidas_naves_1 = naves_inicial_1 - naves_final_1
    perdidas_mandal_1 = mandal_inicial_1 - mandal_final_1
    perdidas_naves_2 = naves_inicial_2 - naves_final_2
    perdidas_mandal_2 = mandal_inicial_2 - mandal_final_2

    if reino_derrotado(unidades_reino_1) and reino_derrotado(unidades_reino_2):
        ganador = "EMPATE"
    elif reino_derrotado(unidades_reino_2):
        ganador = nombre_reino_1
    else:
        ganador = nombre_reino_2

    print("=== RESULTADO FINAL DE LA GUERRA ===")
    print(f"GANADOR: {ganador}")
    print("ESTADÍSTICAS DE LA BATALLA:")
    print("┌{0}┬{1}┬{2}┐".format("─"*27, "─"*15, "─"*17))
    print("│ {0:<25} │ {1:^13} │ {2:^15} │".format("REINO", "PÉRDIDAS", "SUPERVIVIENTES"))
    print("├{0}┼{1}┼{2}┤".format("─"*27, "─"*15, "─"*17))
    print("│ {0:<25} │ {1:^13} │ {2:^15} │".format(
        nombre_reino_1,
        f"{perdidas_naves_1} N/{perdidas_mandal_1} M",
        f"{naves_final_1} N/{mandal_final_1} M"
    ))
    print("│ {0:<25} │ {1:^13} │ {2:^15} │".format(
        nombre_reino_2,
        f"{perdidas_naves_2} N/{perdidas_mandal_2} M",
        f"{naves_final_2} N/{mandal_final_2} M"
    ))
    print("└{0}┴{1}┴{2}┘".format("─"*27, "─"*15, "─"*17))

    coste_batalla = rd.randint(18000, 32000)
    print(f"Coste Total Batalla: {coste_batalla:,} Créditos Galácticos")
    print(f"Duración: {turnos} turnos")


def iniciar_guerra():
    print("INICIANDO GUERRA GALÁCTICA")
    esperar_conexion_reino(1)
    esperar_conexion_reino(2)

    catalogo_naves = Nave.crearNaves()
    catalogo_mandalorianos = Mandaloriano.crearMandalorianos()

    configuracion_reino_1 = configurar_reino("IMPERIO GALÁCTICO", catalogo_naves, catalogo_mandalorianos)
    configuracion_reino_2 = configurar_reino("ALIANZA REBELDE", catalogo_naves, catalogo_mandalorianos)

    imprimir_configuracion_reino(1, configuracion_reino_1, catalogo_naves, catalogo_mandalorianos)
    print("=" * 40)
    imprimir_configuracion_reino(2, configuracion_reino_2, catalogo_naves, catalogo_mandalorianos)

    print("Ambos Reinos configurados correctamente. INICIANDO BATALLA")
    print("=== CAMPO DE BATALLA GALÁCTICO ===")
    print(
        f"=== BATALLA: {configuracion_reino_1['nombre']} "
        f"vs {configuracion_reino_2['nombre']} ==="
    )

    unidades_reino_1 = crear_unidades_reino(
        configuracion_reino_1["nombre"],
        configuracion_reino_1["cantidades_naves"],
        configuracion_reino_1["cantidades_mandalorianos"],
        catalogo_naves,
        catalogo_mandalorianos,
    )
    unidades_reino_2 = crear_unidades_reino(
        configuracion_reino_2["nombre"],
        configuracion_reino_2["cantidades_naves"],
        configuracion_reino_2["cantidades_mandalorianos"],
        catalogo_naves,
        catalogo_mandalorianos,
    )

    estado_inicial_reino_1 = contar_estado(unidades_reino_1)
    estado_inicial_reino_2 = contar_estado(unidades_reino_2)

    print("ESTADO INICIAL:")
    imprimir_estado_tabla(
        configuracion_reino_1["nombre"],
        configuracion_reino_2["nombre"],
        unidades_reino_1,
        unidades_reino_2,
        "",
    )

    turno = 0
    while not reino_derrotado(unidades_reino_1) and not reino_derrotado(unidades_reino_2):
        turno += 1
        print("\n" + "="*60)
        print(f"TURNO {turno:02d} - COMBATES")
        print("-"*60)

        eventos = procesar_turno(unidades_reino_1, unidades_reino_2)
        if not eventos:
            print("Sin combates este turno (nadie alcanzó velocidad suficiente).\n")
        else:
            for indice, evento in enumerate(eventos, start=1):
                print(f" {indice:02d}. {evento}")
            print()

        imprimir_estado_tabla(
            configuracion_reino_1["nombre"],
            configuracion_reino_2["nombre"],
            unidades_reino_1,
            unidades_reino_2,
            f"ESTADO DESPUÉS DEL TURNO {turno}",
        )
        print("="*60 + "\n")

    imprimir_resultado_final(
        configuracion_reino_1["nombre"],
        configuracion_reino_2["nombre"],
        unidades_reino_1,
        unidades_reino_2,
        estado_inicial_reino_1,
        estado_inicial_reino_2,
        turno,
    )


def ejecutar_servidor_principal():
    if mostrar_menu_principal():
        iniciar_guerra()
    else:
        print("Servidor finalizado.")


if __name__ == "__main__":
    ejecutar_servidor_principal()