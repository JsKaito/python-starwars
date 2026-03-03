import socket


def run_server():
    '''
    Servidor TCP.
    Espera una conexión de cliente, recibe mensajes y responde con 'accepted'.
    Si recibe 'close', cierra la conexión.
    '''

    # Crear el socket del servidor (TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    port = 8000

    # Asociar el socket a una dirección y puerto
    server.bind((server_ip, port))
    # Escuchar conexiones entrantes
    server.listen(0)
    print(f"Escuchando en {server_ip}:{port}")

    # Aceptar una conexión entrante
    client_socket, client_address = server.accept()
    print(f"Conexión aceptada de {client_address[0]}:{client_address[1]}")

    # Recibir datos del cliente
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # Convierte bytes a string
        
        # Si se recibe "close", se cierra la conexión
        if request.lower() == "close":
            # Enviar respuesta de cierre al cliente
            client_socket.send("closed".encode("utf-8"))
            break

        print(f"Recibido: {request}")

        response = "accepted".encode("utf-8") # Convierte string a bytes
        # Enviar respuesta de aceptación al cliente
        client_socket.send(response)

    # Cerrar el socket de conexión con el cliente
    client_socket.close()
    print("Conexión con el cliente cerrada")
    # Cerrar el socket del servidor
    server.close()


run_server()