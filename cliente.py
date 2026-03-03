"""
Cliente TCP básico para pruebas de conexión.
Se conecta al servidor, muestra la bienvenida y permite enviar mensajes.
Finaliza si se envía 'salir'.
"""
import socket


HOST = "127.0.0.1"
PORT = 5050

def iniciar_cliente(host=HOST, port=PORT):
	"""
	Inicia el cliente TCP, se conecta al servidor y permite enviar mensajes.
	Finaliza si el usuario escribe 'salir'.
	"""
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
		client.connect((host, port))
		# Recibir y mostrar mensaje de bienvenida
		bienvenida = client.recv(1024).decode("utf-8", errors="ignore").strip()
		print(bienvenida)

		while True:
			# Pedir mensaje al usuario
			mensaje = input("Mensaje para servidor (escribí 'salir' para terminar): ").strip()
			client.sendall((mensaje + "\n").encode("utf-8"))  # Enviar mensaje

			respuesta = client.recv(1024)
			if not respuesta:
				print("Servidor desconectado.")
				break

			# Mostrar respuesta del servidor
			print(respuesta.decode("utf-8", errors="ignore").strip())

			if mensaje.lower() == "salir":
				break


if __name__ == "__main__":
	iniciar_cliente()
