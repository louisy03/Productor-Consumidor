import threading
import time
import random
import keyboard
from collections import deque

class ProductorConsumidor:
    def __init__(self):
        self.buffer = deque(maxlen=25)  # Buffer circular de tamaño 25
        self.buffer.extend(['_'] * 25)  # Inicializar con espacios vacíos
        self.mutex = threading.Semaphore(1)  # Semáforo para exclusión mutua
        self.items = threading.Semaphore(0)  # Semáforo para items disponibles (inicia en 0)
        self.espacios = threading.Semaphore(25)  # Semáforo para espacios disponibles (inicia en 25)
        self.productor_en_buffer = False
        self.consumidor_en_buffer = False
        self.pos_produccion = 0  # Posición actual de producción
        self.pos_consumo = 0  # Posición actual de consumo
        self.running = True

    def imprimir_buffer(self):
        print(" ".join(self.buffer))
        print(" ".join(str(i+1).ljust(2) for i in range(25)))

    def productor(self):
        while self.running:
            # Tiempo aleatorio de "sueño"
            tiempo_dormido = random.uniform(0.5, 2)
            print(f"Productor durmiendo por {tiempo_dormido:.2f} segundos...")
            time.sleep(tiempo_dormido)
            
            # Intentar entrar al buffer
            print("Productor intentando entrar al buffer...")
            
            # Verificar condiciones para entrar (espacio disponible y consumidor no está dentro)
            if self.espacios._value > 0 and not self.consumidor_en_buffer:
                self.espacios.acquire()  # Disminuir espacios disponibles
                self.mutex.acquire()  # Entrar a sección crítica
                
                self.productor_en_buffer = True
                print("Productor entro al buffer")
                
                # Determinar cuántos elementos producir (1-5)
                elementos_a_producir = random.randint(1, 5)
                print(f"Productor intentara producir {elementos_a_producir} elementos")
                
                # Producir elementos
                for _ in range(elementos_a_producir):
                    if self.espacios._value >= 0:  # Asegurar que aún hay espacio
                        # Producir un elemento (usaremos '*' como ejemplo)
                        self.buffer[self.pos_produccion] = '*'
                        self.pos_produccion = (self.pos_produccion + 1) % 25
                        self.items.release()  # Aumentar contador de items disponibles
                    else:
                        break
                
                self.productor_en_buffer = False
                self.mutex.release()  # Salir de sección crítica
                
                # Mostrar estado actual del buffer
                print("\nEstado del buffer:")
                self.imprimir_buffer()
            else:
                print("Productor no pudo entrar al buffer (no hay espacio o consumidor esta dentro)")

    def consumidor(self):
        while self.running:
            # Tiempo aleatorio de "sueño"
            tiempo_dormido = random.uniform(0.5, 2)
            print(f"Consumidor durmiendo por {tiempo_dormido:.2f} segundos...")
            time.sleep(tiempo_dormido)
            
            # Intentar entrar al buffer
            print("Consumidor intentando entrar al buffer...")
            
            # Verificar condiciones para entrar (items disponibles y productor no está dentro)
            if self.items._value > 0 and not self.productor_en_buffer:
                self.items.acquire()  # Disminuir items disponibles
                self.mutex.acquire()  # Entrar a sección crítica
                
                self.consumidor_en_buffer = True
                print("Consumidor entro al buffer")
                
                # Determinar cuántos elementos consumir (1-5)
                elementos_a_consumir = random.randint(1, 5)
                print(f"Consumidor intentara consumir {elementos_a_consumir} elementos")
                
                # Consumir elementos
                for _ in range(elementos_a_consumir):
                    if self.items._value >= 0:  # Asegurar que aún hay items
                        # Consumir un elemento
                        self.buffer[self.pos_consumo] = '_'
                        self.pos_consumo = (self.pos_consumo + 1) % 25
                        self.espacios.release()  # Aumentar contador de espacios disponibles
                    else:
                        break
                
                self.consumidor_en_buffer = False
                self.mutex.release()  # Salir de sección crítica
                
                # Mostrar estado actual del buffer
                print("\nEstado del buffer:")
                self.imprimir_buffer()
            else:
                print("Consumidor no pudo entrar al buffer (no hay items o productor esta dentro)")

    def run(self):
        # Crear hilos
        hilo_productor = threading.Thread(target=self.productor)
        hilo_consumidor = threading.Thread(target=self.consumidor)
        
        # Iniciar hilos
        hilo_productor.start()
        hilo_consumidor.start()
        
        # Esperar a que se presione ESC para terminar
        while self.running:
            if keyboard.is_pressed('esc'):
                self.running = False
                print("\nPrograma terminado por el usuario")
                break
            time.sleep(0.1)
        
        # Esperar a que los hilos terminen
        hilo_productor.join()
        hilo_consumidor.join()

if __name__ == "__main__":
    pc = ProductorConsumidor()
    print("Estado inicial del buffer:")
    pc.imprimir_buffer()
    pc.run()
