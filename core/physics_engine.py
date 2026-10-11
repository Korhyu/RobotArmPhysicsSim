import collections
import numpy as np

class MotorFisico2D:
    def __init__(self, ancho_sim, alto_sim, max_historial=300):
        self.ancho_sim = ancho_sim
        self.alto_sim = alto_sim

        # Parámetros físicos editables
        self.masa = 2.5          # kg
        self.elasticidad = 0.8   # Coeficiente de restitución (0 a 1)
        self.friccion = 0.05     # Resistencia al movimiento
        self.gravedad = 9.81 * 20 # Escalada a píxeles/s^2

        # Estado del objeto (Posición x, y y Velocidad vx, vy)
        self.pos = np.array([100.0, 100.0], dtype=np.float64)
        self.vel = np.array([50.0, 0.0], dtype=np.float64)
        self.ultima_aceleracion = np.array([0.0, 0.0], dtype=np.float64)
        
        self.radio_objeto = 25

        # --- OBSERVADOR / SENSOR INTEGRADO ---
        self.max_historial = max_historial
        self.tiempos = collections.deque(maxlen=max_historial)
        self.historial_pos_y = collections.deque(maxlen=max_historial)
        self.historial_vel_y = collections.deque(maxlen=max_historial)
        self.historial_acel_y = collections.deque(maxlen=max_historial)
        self.tiempo_acumulado = 0.0

    def aplicar_impulso(self, vector_impulso):
        """Permite aplicar fuerzas externas o impulsos puntuales."""
        self.vel += vector_impulso

    def actualizar(self, dt):
        """Ejecuta un paso de integración numérica (Euler), resuelve colisiones y registra telemetría."""
        # 1. Aceleraciones (Gravedad y Fricción)
        aceleracion = np.array([0.0, self.gravedad], dtype=np.float64)
        aceleracion -= self.friccion * self.vel
        self.ultima_aceleracion = aceleracion.copy()

        # 2. Integración
        self.vel += aceleracion * dt
        self.pos += self.vel * dt

        # 3. Colisiones con los límites de la caja
        limite_suelo = self.alto_sim - 40
        if self.pos[1] + self.radio_objeto >= limite_suelo:
            self.pos[1] = limite_suelo - self.radio_objeto
            self.vel[1] = -self.vel[1] * self.elasticidad
            self.vel[0] *= 0.95

        if self.pos[0] + self.radio_objeto >= self.ancho_sim:
            self.pos[0] = self.ancho_sim - self.radio_objeto
            self.vel[0] = -self.vel[0] * self.elasticidad

        if self.pos[0] - self.radio_objeto <= 40:
            self.pos[0] = 40 + self.radio_objeto
            self.vel[0] = -self.vel[0] * self.elasticidad

        # --- REGISTRO DEL OBSERVADOR ---
        self.tiempo_acumulado += dt
        self.tiempos.append(self.tiempo_acumulado)
        self.historial_pos_y.append(self.pos[1])
        self.historial_vel_y.append(self.vel[1])
        self.historial_acel_y.append(self.ultima_aceleracion[1])

    def obtener_telemetria(self):
        return (
            list(self.tiempos),
            list(self.historial_pos_y),
            list(self.historial_vel_y),
            list(self.historial_acel_y)
        )