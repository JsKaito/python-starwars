import socket
import time

class Cliente:
    def __init__(self):
        self.socket = None
    
    def conectar(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('localhost', 5555))
            print("Conectado al servidor")
            
            # Recibir bienvenida
            self.socket.recv(1024).decode()
            
            # Nombre del reino
            nombre = input("Nombre del Reino: ")
            self.socket.send(nombre.encode())
            
            # Configurar naves
            print("\nCREANDO FLOTA DE NAVES")
            tipos_naves = ["Estrella Muerte", "Ejecutor", "Halcon", "Naboo", "Caza Jedi"]
            for tipo in tipos_naves:
                mensaje = self.socket.recv(1024).decode()
                print(f"   {tipo}: ", end="")
                cant = input()
                while not cant.isdigit():
                    print("   Por favor ingrese un numero: ", end="")
                    cant = input()
                self.socket.send(cant.encode())
            
            # Configurar mandalorianos
            print("\nCREANDO LEGION MANDALORIANA")
            for nivel in range(1, 6):
                mensaje = self.socket.recv(1024).decode()
                print(f"   Mandaloriano Nivel {nivel}: ", end="")
                cant = input()
                while not cant.isdigit():
                    print("   Por favor ingrese un numero: ", end="")
                    cant = input()
                self.socket.send(cant.encode())
            
            # Recibir confirmacion de coste
            mensaje = self.socket.recv(1024).decode()
            if mensaje.startswith("COSTE_"):
                coste = mensaje.split("_")[1]
                print(f"\nReino configurado. Coste total: {coste} creditos")
            
            print("\nEsperando inicio de batalla...")
            print("(Los combates se muestran en el servidor)")
            print()
            
            # Recibir actualizaciones de la batalla
            while True:
                try:
                    self.socket.settimeout(1)
                    datos = self.socket.recv(1024).decode()
                    
                    if not datos:
                        break
                    
                    if datos == "INICIO_BATALLA":
                        print("LA BATALLA HA COMENZADO!")
                    elif datos.startswith("TURNO_"):
                        partes = datos.split("_")
                        turno = partes[1]
                        mis_unidades = partes[2]
                        enemigo_unidades = partes[3]
                        print(f"\n--- TURNO {turno} ---")
                        print(f"   Mis unidades: {mis_unidades}")
                        print(f"   Unidades enemigas: {enemigo_unidades}")
                    elif datos.startswith("RESULTADO_"):
                        resultado = datos.split("_")[1]
                        if resultado == "VICTORIA":
                            print("\n" + "="*40)
                            print("VICTORIA! Has ganado la guerra!")
                            print("="*40)
                        elif resultado == "DERROTA":
                            print("\n" + "="*40)
                            print("DERROTA! Has perdido la guerra!")
                            print("="*40)
                        elif resultado == "EMPATE":
                            print("\n" + "="*40)
                            print("EMPATE! Ambos reinos han sido aniquilados!")
                            print("="*40)
                        else:
                            print("\nLa batalla ha terminado.")
                        break
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    break
                    
        except ConnectionRefusedError:
            print("Error: No se pudo conectar al servidor. Asegurate de que el servidor este ejecutandose.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.socket:
                self.socket.close()
            print("\nPresiona Enter para salir...")
            input()

if __name__ == "__main__":
    print("=== CLIENTE - LA GUERRA DE LAS GALAXIAS ===\n")
    Cliente().conectar()