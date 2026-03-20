import socket
from clases.Nave import Nave
from clases.mandaloriano import Mandaloriano


def run_client():
    """
    Cliente para un servidor TCP.
    Envía conexiones a un servidor, envía mensajes y espera respuestas.
    Si envía 'close', cierra la conexión. 
    """
    # Crea un socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  
    server_port = 8000  
    
    # Establece la conexión con el servidor
    client.connect((server_ip, server_port))

    while True:
        msg = input("Introduce el mensaje: ")
        client.send(msg.encode("utf-8")[:1024])

        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            break

        print(f"Recibido: {response}")

    # Cierra la conexión con el servidor
    client.close()
    print("Conexión con el servidor cerrada.")


def run_client_batalla():
    """
    Cliente para la batalla del Imperio Galáctico.
    Se conecta al servidor, solicita configuración de reino, naves y mandalorianos,
    y recibe actualizaciones en tiempo real de la batalla.
    """
    # Crea un socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  
    server_port = 8000  
    
    # Establece la conexión con el servidor
    try:
        client.connect((server_ip, server_port))
        print("=== CLIENTE - REINO IMPERIAL ===")
        print("Conectando al servidor... ✓\n")
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor.")
        return

    # Solicitar nombre del reino
    response = client.recv(1024).decode("utf-8")
    print(f"SERVIDOR: \"{response}\"")
    nombre_reino = input("> ")
    client.send(nombre_reino.encode("utf-8"))

    # Crear flota de naves
    print("\nSERVIDOR: 🏟️ CREAMOS LA FLOTA DE NAVES 🏟️")
    nave = Nave(0, "", 0, 0, 0, (0, 0), 0)
    naves_lista = nave.crearNaves()
    
    flota = {}
    for ship in naves_lista:
        response = client.recv(1024).decode("utf-8")
        print(f"SERVIDOR: \"{response}\"")
        cantidad = int(input("> "))
        flota[ship.nombre] = cantidad
        client.send(str(cantidad).encode("utf-8"))

    # Crear legión de mandalorianos
    print("\nSERVIDOR: ⚔️ CREAMOS LA LEGIÓN DE MANDALORIANOS ⚔️")
    mandaloriano = Mandaloriano(0, "", 0, 0, 0, 0, 0)
    mandos_lista = mandaloriano.crearMandatorianos()
    
    legion = {}
    for mando in mandos_lista:
        response = client.recv(1024).decode("utf-8")
        print(f"SERVIDOR: \"{response}\"")
        cantidad = int(input("> "))
        legion[mando.nombre] = cantidad
        client.send(str(cantidad).encode("utf-8"))

    # Configuración enviada, esperando batalla
    print("\n✅ Configuración enviada. Esperando inicio batalla...")
    print("=== RECIBIENDO ACTUALIZACIONES EN TIEMPO REAL ===\n")

    # Recibir actualizaciones de la batalla
    while True:
        try:
            response = client.recv(1024).decode("utf-8")
            if not response:
                break
            print(f"SERVIDOR: \"{response}\"")
            
            if "BATALLA TERMINADA" in response:
                break
        except:
            break

    # Cierra la conexión con el servidor
    client.close()
    print("\nConexión con el servidor cerrada.")

run_client()
