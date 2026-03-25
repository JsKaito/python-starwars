import socket


def solicitar_cantidad(texto):
    valor = input(texto).strip()
    while not valor.isdigit():
        valor = input("   Por favor ingrese un numero: ").strip()
    return valor

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 8000))
        print("Conectado al servidor")

        nombre = input("Nombre del Reino: ")
        s.send(nombre.encode())

        print("\nCREANDO FLOTA DE NAVES")
        for _ in range(5):
            mensaje = s.recv(1024).decode("utf-8")
            _, nombre_nave, precio = mensaje.split("|")
            cant = solicitar_cantidad(f"   {nombre_nave} (precio {precio}): ")
            s.send(cant.encode())

        print("\nCREANDO LEGION MANDALORIANA")
        for _ in range(5):
            mensaje = s.recv(1024).decode("utf-8")
            _, nombre_mandaloriano, nivel, precio = mensaje.split("|")
            cant = solicitar_cantidad(
                f"   {nombre_mandaloriano} (Nivel {nivel}, precio {precio}): "
            )
            s.send(cant.encode())

        mensaje = s.recv(1024).decode()
        if mensaje.startswith("COSTE_"):
            coste = mensaje.split("_")[1]
            print(f"\nReino configurado. Coste total: {coste} creditos")

        while True:
            estado = s.recv(1024).decode("utf-8")
            if estado == "ESPERANDO_RIVAL":
                print("Esperando a que el otro cliente termine su seleccion...")
            elif estado == "INICIANDO_BATALLA":
                print("Ambos clientes listos. Iniciando batalla...")
                break

        print("\nDatos enviados. Esperando resultado de la batalla en el servidor...")
        resultado = s.recv(1024).decode("utf-8")
        if resultado.startswith("RESULTADO|"):
            _, ganador, turnos = resultado.split("|")
            print(f"Resultado final: ganador {ganador} en {turnos} turnos")

        s.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
