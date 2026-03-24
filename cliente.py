import socket


def run_client():
    '''Cliente para un servidor TCP.

    Envía conexiones a un servidor, envía mensajes y espera respuestas.
    Si envía 'close', cierra la conexión.

    Returns:
        None
    '''
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

run_client()
