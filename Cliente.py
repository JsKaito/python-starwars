import socket

def run_client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000

    try:
        client.connect((server_ip, server_port))
    except:
        print("No se pudo conectar al servidor.")
        return

    print("Conectado al servidor...\n")

    while True:
        try:
            response = client.recv(1024)

            if not response:
                print("Servidor cerró conexión.")
                break

            response = response.decode()
            print(f"SERVIDOR: {response}")

            if "Introduce" in response or "Número" in response:
                msg = input("> ")
                client.send(msg.encode())

            if "Configuración guardada" in response:
                print("Servidor: configuración recibida y guardada. Esperando...")
                continue

            if "BATALLA TERMINADA" in response:
                print("Fin del juego.")
                try:
                    client.send("ACK".encode())
                except Exception:
                    pass
                break

        except ConnectionResetError:
            print("El servidor se ha cerrado inesperadamente.")
            break

        except Exception as e:
            print("Error:", e)
            break

    client.close()
    print("Conexión cerrada.")


run_client()