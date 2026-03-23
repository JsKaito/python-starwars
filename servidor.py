import random as rd
import socket
from clases.nave import Nave
from clases.mandaloriano import Mandaloriano

UMBRAL_VELOCIDAD_ATAQUE = 60


def correr_servidor_tcp_basico():
    """
    Servidor TCP básico para pruebas de conexión.
    """
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
    print("Simulación de Batalla (Ejemplo)")
    print("=== SERVIDOR - LA GUERRA DE LAS GALAXIAS (2026) ===")
    print("1. Iniciar Guerra")
    print("2. Finalizar Servidor")
    opcion = input("Seleccionar opción para continuar: ").strip()

    return opcion in {"1", "3"}


def esperar_conexion_reino(numero_reino):
    print(f"Esperando conexión de Reino {numero_reino}... [CONECTADO]")


def generar_cantidades(cantidad_tipos, minimo, maximo):
    return [rd.randint(minimo, maximo) for _ in range(cantidad_tipos)]


def calcular_coste_total(cantidades_naves, cantidades_mandalorianos, catalogo_naves, catalogo_mandalorianos):
    coste_naves = 0
    for indice, cantidad in enumerate(cantidades_naves):
        coste_naves += cantidad * catalogo_naves[indice].price

    coste_mandalorianos = 0
    for indice, cantidad in enumerate(cantidades_mandalorianos):
        coste_mandalorianos += cantidad * catalogo_mandalorianos[indice].price

    return coste_naves + coste_mandalorianos


def configurar_reino(nombre_reino, catalogo_naves, catalogo_mandalorianos):
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
    if isinstance(unidad_base.speed, tuple):
        return rd.randint(unidad_base.speed[0], unidad_base.speed[1])
    return int(unidad_base.speed)


def crear_unidades_reino(nombre_reino, cantidades_naves, cantidades_mandalorianos, catalogo_naves, catalogo_mandalorianos):
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
                    # Si quieres también puedes numerar mandalorianos:
                    # "id_mandaloriano": contador_mandalorianos,
                }
            )
            contador_mandalorianos += 1

    return unidades


def unidades_vivas(unidades):
    return [unidad for unidad in unidades if unidad["vida_actual"] > 0]


def contar_estado(unidades):
    naves = sum(1 for unidad in unidades if unidad["categoria"] == "Nave" and unidad["vida_actual"] > 0)
    mandalorianos = sum(1 for unidad in unidades if unidad["categoria"] == "Mandaloriano" and unidad["vida_actual"] > 0)
    return naves, mandalorianos


def truncar(texto, largo_maximo):
    # Ya no truncamos los nombres de los reinos
    return texto


def imprimir_estado_tabla(nombre_reino_1, nombre_reino_2, unidades_reino_1, unidades_reino_2, titulo):
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
    fuerza_ataque = atacante["ataque"] * rd.uniform(0.90, 1.25)
    mitigacion_defensa = objetivo["defensa"] * rd.uniform(0.35, 0.55)
    daño = max(1, int(fuerza_ataque - mitigacion_defensa))
    return daño


def ejecutar_ataque(atacante, objetivo):
    daño = calcular_daño(atacante, objetivo)
    objetivo["vida_actual"] = max(0, objetivo["vida_actual"] - daño)


    # Mostrar identificador si es nave
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

        # Permite múltiples ataques por turno: 120 -> 2 ataques, 180 -> 3, etc.
        while atacante["velocidad_acumulada"] >= UMBRAL_VELOCIDAD_ATAQUE and enemigos:
            objetivo = rd.choice(enemigos)
            eventos_turno.append(ejecutar_ataque(atacante, objetivo))
            atacante["velocidad_acumulada"] -= UMBRAL_VELOCIDAD_ATAQUE
            enemigos = [enemigo for enemigo in enemigos if enemigo["vida_actual"] > 0]

    return eventos_turno


def reino_derrotado(unidades):
    return len(unidades_vivas(unidades)) == 0


def imprimir_resultado_final(nombre_reino_1, nombre_reino_2, unidades_reino_1, unidades_reino_2, total_inicial_1, total_inicial_2, turnos):
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
