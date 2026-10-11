import collections
import numpy as np

class MotorFisico2D:
    def __init__(self, ancho_sim, alto_sim, max_historial=300):
        self.ancho_sim = ancho_sim
        self.alto_sim = alto_sim

        # Parámetros físicos del brazo / péndulo (1-DOF)
        self.longitud_brazo = 150.0  # L (píxeles)
        self.masa = 2.0              # m (kg)
        self.friccion = 0.05         # b (amortiguamiento)
        self.gravedad = 9.81 * 40    # g escalada

        # --- NUEVO: Actuador (Motor en la articulación) ---
        self.torque_motor = 0.0      # Torque aplicado por el actuador

        # Centro de la articulación (Pivote fijo)
        self.centro_pivote = np.array([ancho_sim / 2.0, alto_sim / 2.0], dtype=np.float64)

        # Estado angular
        self.angulo = np.pi / 4.0    # Posición inicial (45°)
        self.velocidad_angular = 0.0 
        self.ultima_aceleracion_angular = 0.0

        self.pos = np.array([0.0, 0.0], dtype=np.float64)
        self._actualizar_posicion_cartesiana()

        # Observador / Sensor integrado
        self.max_historial = max_historial
        self.tiempos = collections.deque(maxlen=max_historial)
        self.historial_angulo = collections.deque(maxlen=max_historial)
        self.historial_vel_ang = collections.deque(maxlen=max_historial)
        self.historial_acel_ang = collections.deque(maxlen=max_historial)
        self.tiempo_acumulado = 0.0

    def _actualizar_posicion_cartesiana(self):
        x = self.centro_pivote[0] + self.longitud_brazo * np.sin(self.angulo)
        y = self.centro_pivote[1] + self.longitud_brazo * np.cos(self.angulo)
        self.pos = np.array([x, y], dtype=np.float64)

    def aplicar_impulso(self, valor_impulso):
        """Permite aplicar un golpe manual externo."""
        self.velocidad_angular += valor_impulso

    def actualizar(self, dt):
        """Ejecuta un paso de integración numérica considerando la gravedad, fricción y el torque del motor."""
        # 1. Inercia del péndulo simple (I = m * L^2)
        inercia = self.masa * (self.longitud_brazo ** 2)
        if inercia == 0:
            inercia = 1.0

        # 2. Torques que actúan sobre la articulación
        # Torque de gravedad: tau_g = - m * g * L * sin(theta)
        torque_gravedad = -self.masa * self.gravedad * self.longitud_brazo * np.sin(self.angulo)
        
        # Torque de fricción escalado para que se note en la simulación
        torque_friccion = - (self.friccion * 5000.0) * self.velocidad_angular

        # Torque total = Gravedad + Fricción + Torque del Motor
        torque_total = torque_gravedad + torque_friccion + self.torque_motor

        # 3. Aceleración angular (alpha = Torque_total / Inercia)
        aceleracion_angular = torque_total / inercia
        self.ultima_aceleracion_angular = aceleracion_angular

        # 4. Integración numérica
        self.velocidad_angular += aceleracion_angular * dt
        self.angulo += self.velocidad_angular * dt

        self._actualizar_posicion_cartesiana()

        # Registro del observador
        self.tiempo_acumulado += dt
        self.tiempos.append(self.tiempo_acumulado)
        self.historial_angulo.append(self.angulo)
        self.historial_vel_ang.append(self.velocidad_angular)
        self.historial_acel_ang.append(self.ultima_aceleracion_angular)

    def obtener_telemetria(self):
        return (
            list(self.tiempos),
            list(self.historial_angulo),
            list(self.historial_vel_ang),
            list(self.historial_acel_ang)
        )