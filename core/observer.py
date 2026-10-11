import collections
import numpy as np

class ObservadorFisico:
    def __init__(self, max_historial=300):
        self.max_historial = max_historial
        
        # Buffers circulares o colas para almacenar el tiempo y las variables
        self.tiempos = collections.deque(maxlen=max_historial)
        self.posiciones_y = collections.deque(maxlen=max_historial)
        self.velocidades_y = collections.deque(maxlen=max_historial)
        self.aceleraciones_y = collections.deque(maxlen=max_historial)
        
        self.tiempo_acumulado = 0.0

    def registrar(self, dt, fisica):
        self.tiempo_acumulado += dt
        
        # Extraer variables del cuerpo físico
        pos_y = fisica.pos[1]
        vel_y = fisica.vel[1]
        
        # Calcular aceleración aproximada por derivada numérica si no se expone directo
        # (o podemos registrar la aceleración neta del motor físico)
        acel_y = fisica.ultima_aceleracion[1] if hasattr(fisica, 'ultima_aceleracion') else 0.0

        # Guardar en el historial
        self.tiempos.append(self.tiempo_acumulado)
        self.posiciones_y.append(pos_y)
        self.velocidades_y.append(vel_y)
        self.aceleraciones_y.append(acel_y)

    def obtener_datos(self):
        return list(self.tiempos), list(self.posiciones_y), list(self.velocidades_y), list(self.aceleraciones_y)