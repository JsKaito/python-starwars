import socket


def solicitarCantidad(texto):
    '''Solicita una cantidad numerica al usuario.

    Args:
        texto (str): Texto mostrado al pedir la cantidad.

    Returns:
        str: Cantidad valida ingresada por el usuario.
    '''
    valor = input(texto).strip()
    while not valor.isdigit():
        valor = input("   Por favor ingrese un numero: ").strip()
    return valor


def main():
    '''Ejecuta el cliente de configuracion de reino.

    Returns:
        None
    '''
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("localhost", 8000))
        print("Conectado al servidor")

        nombre = input("Nombre del Reino: ")
        cliente.send(nombre.encode())

        print("\nCREANDO FLOTA DE NAVES")
        for _ in range(5):
            mensaje = cliente.recv(1024).decode("utf-8")
            _, nombreNave, precio = mensaje.split("|")
            cantidad = solicitarCantidad(f"   {nombreNave} (precio {precio}): ")
            cliente.send(cantidad.encode())

        print("\nCREANDO LEGION MANDALORIANA")
        for _ in range(5):
            mensaje = cliente.recv(1024).decode("utf-8")
            _, nombreMandaloriano, nivel, precio = mensaje.split("|")
            cantidad = solicitarCantidad(
                f"   {nombreMandaloriano} (Nivel {nivel}, precio {precio}): "
            )
            cliente.send(cantidad.encode())

        mensajeCoste = cliente.recv(1024).decode()
        if mensajeCoste.startswith("COSTE_"):
            coste = mensajeCoste.split("_")[1]
            print(f"\nReino configurado. Coste total: {coste} creditos")

        while True:
            estado = cliente.recv(1024).decode("utf-8")
            if estado == "ESPERANDO_RIVAL":
                print("Esperando a que el otro cliente termine su seleccion...")
            elif estado == "INICIANDO_BATALLA":
                print("Ambos clientes listos. Iniciando batalla...")
                break

        print("\nDatos enviados. Esperando resultado de la batalla en el servidor...")
        resultado = cliente.recv(1024).decode("utf-8")
        if resultado.startswith("RESULTADO|"):
            _, ganador, turnos = resultado.split("|")
            print(f"Resultado final: ganador {ganador} en {turnos} turnos")

        cliente.close()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
