import socket
from clases.Nave import Nave
from clases.Mandaloriano import Mandaloriano
import random
import time

def safe_send(sock, texto):
    try:
        sock.sendall(texto.encode('utf-8'))
    except Exception as e:
        print('Error send:', e)


def safe_recv(sock):
    try:
        data = sock.recv(1024)
        if not data:
            return None
        return data.decode('utf-8').strip()
    except Exception as e:
        print('Error recv:', e)
        return None


def run_server():

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_ip = "127.0.0.1"
        server_port = 8000

        server.bind((server_ip, server_port))
        server.listen(2)

        print("=== SERVIDOR - LA GUERRA DE LAS GALAXIAS ===")
        print(f"Escuchando en {server_ip}:{server_port}")

        clientes = []

        # Esperar 2 clientes
        while len(clientes) < 2:
            client_socket, addr = server.accept()
            print(f"Cliente conectado desde {addr[0]}:{addr[1]}")
            clientes.append(client_socket)

        print("\n🔥 INICIANDO GUERRA GALÁCTICA 🔥\n")

        # =========================
        # NOMBRES
        # =========================
        for cliente in clientes:
            cliente.send("Introduce nombre de tu Reino:".encode())

        nombres = []
        for cliente in clientes:
            data = cliente.recv(1024)
            print("Recibido nombre RAW:", data)

            nombre_reino = data.decode().strip()
            print(f"Reino conectado: {nombre_reino}")
            nombres.append(nombre_reino)

        # =========================
        # NAVES
        # =========================
        nave = Nave(0, "", 0, 0, 0, (0, 0), 0)
        naves_lista = nave.crearNaves()

        for cliente in clientes:
            safe_send(cliente, "🏟️ CREAMOS LA FLOTA DE NAVES 🏟️")

        for ship in naves_lista:

            for cliente in clientes:
                safe_send(cliente, f"Número de Naves ({ship.nombre}):")

            for i, cliente in enumerate(clientes):
                print("Esperando datos de cliente...")

                data = safe_recv(cliente)
                print("Recibido RAW:", data)

                if data is None or data == "":
                    cantidad = 0
                else:
                    try:
                        cantidad = int(data.strip())
                    except:
                        print("Valor inválido recibido")
                        cantidad = 0

                print(f"{nombres[i]} -> {ship.nombre}: {cantidad}")

        # =========================
        # MANDALORIANOS
        # =========================
        mandaloriano = Mandaloriano(0, "", 0, 0, 0, 0, 0)
        mandos_lista = mandaloriano.crearMandatorianos()

        for cliente in clientes:
            safe_send(cliente, "⚔️ CREAMOS LA LEGIÓN DE MANDALORIANOS ⚔️")

        for mando in mandos_lista:

            for cliente in clientes:
                safe_send(cliente, f"Número de Mandalorianos ({mando.nombre}):")

            for i, cliente in enumerate(clientes):
                print("Esperando datos de cliente...")

                data = safe_recv(cliente)
                print("Recibido RAW:", data)

                if data is None or data == "":
                    cantidad = 0
                else:
                    try:
                        cantidad = int(data.strip())
                    except:
                        print("Valor inválido recibido")
                        cantidad = 0

                print(f"{nombres[i]} -> {mando.nombre}: {cantidad}")

        # =========================
        # FINAL CONFIG
        # =========================
        for cliente in clientes:
            safe_send(cliente, "✅ Configuración guardada. Servidor en espera...")

        print("\n✅ CONFIGURACIÓN GUARDADA\n")
        print("El servidor ahora queda en espera. Presiona Ctrl+C para detener.")

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")
        finally:
            for cliente in clientes:
                try:
                    cliente.close()
                except:
                    pass
            server.close()
            print("Servidor cerrado correctamente.")

    except Exception as e:
        print("❌ ERROR EN SERVIDOR:", e)


run_server()