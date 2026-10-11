import pygame
from ui.slider import Slider
from ui.plotter import PanelGraficos

class Renderer:
    def __init__(self, ventana, ancho_sim, alto_ventana):
        self.ventana = ventana
        self.ancho_sim = ancho_sim
        self.alto_ventana = alto_ventana
        self.fuente = pygame.font.SysFont("Arial", 16)

        # Sliders en el panel derecho superior (adaptados para el péndulo)
        panel_x = ancho_sim + 30
        self.slider_masa = Slider(panel_x, 70, 220, 8, 0.5, 10.0, 2.0, "Masa Punta (kg)")
        self.slider_longitud = Slider(panel_x, 140, 220, 8, 50.0, 250.0, 150.0, "Longitud Brazo (px)")
        self.slider_friccion = Slider(panel_x, 210, 220, 8, 0.0, 0.2, 0.05, "Fricción Articulación")
        self.sliders = [self.slider_masa, self.slider_longitud, self.slider_friccion]

        # Panel de gráficos inferior
        self.panel_graficos = PanelGraficos(x=20, y=470, ancho=1010, alto=160)

    def manejar_eventos_sliders(self, evento):
        for slider in self.sliders:
            slider.manejar_evento(evento)

    def actualizar_fisica_desde_sliders(self, fisica):
        fisica.masa = self.slider_masa.valor
        fisica.longitud_brazo = self.slider_longitud.valor
        fisica.friccion = self.slider_friccion.valor

    def dibujar(self, fisica):
        self.ventana.fill((25, 25, 30))

        # 1. Área de simulación física (Arriba a la izquierda)
        alto_sim_caja = 430
        pygame.draw.rect(self.ventana, (40, 40, 48), (20, 20, self.ancho_sim - 40, alto_sim_caja), 2)
        
        # Dibujar pivote fijo central
        pivote_x, pivote_y = int(fisica.centro_pivote[0]), int(fisica.centro_pivote[1])
        pygame.draw.circle(self.ventana, (150, 150, 150), (pivote_x, pivote_y), 8)

        # Dibujar eslabón (brazo del robot)
        extremo_x, extremo_y = int(fisica.pos[0]), int(fisica.pos[1])
        pygame.draw.line(self.ventana, (200, 200, 200), (pivote_x, pivote_y), (extremo_x, extremo_y), 4)

        # Dibujar masa en la punta
        pygame.draw.circle(self.ventana, (0, 160, 255), (extremo_x, extremo_y), 20)
        pygame.draw.circle(self.ventana, (255, 255, 255), (extremo_x, extremo_y), 4)

        # 2. Panel de control / Sliders (Arriba a la derecha)
        panel_x = self.ancho_sim + 20
        pygame.draw.line(self.ventana, (70, 70, 80), (self.ancho_sim, 0), (self.ancho_sim, 450), 2)
        
        titulo = self.fuente.render("--- BRAZO ROBÓTICO (1-DOF) ---", True, (255, 255, 255))
        self.ventana.blit(titulo, (panel_x, 25))

        for slider in self.sliders:
            slider.dibujar(self.ventana)

        # Telemetría en texto
        textos = [
            f"Ángulo (θ): {fisica.angulo:.2f} rad",
            f"Vel. Angular (ω): {fisica.velocidad_angular:.2f} rad/s",
            f"Acel. Angular (α): {fisica.ultima_aceleracion_angular:.2f} rad/s²",
            "",
            "[ESPACIO]: Dar golpe/impulso"
        ]
        for i, texto in enumerate(textos):
            superficie_texto = self.fuente.render(texto, True, (200, 200, 200))
            self.ventana.blit(superficie_texto, (panel_x, 270 + (i * 22)))

        # 3. Separador horizontal para los gráficos
        pygame.draw.line(self.ventana, (70, 70, 80), (20, 450), (1030, 450), 2)

        # 4. Dibujar Gráficas Temporales (Abajo)
        _, ang_hist, vel_ang_hist, acel_ang_hist = fisica.obtener_telemetria()
        self.panel_graficos.dibujar_grafico(self.ventana, ang_hist, "Ángulo θ (rad)", (0, 160, 255), 0)
        self.panel_graficos.dibujar_grafico(self.ventana, vel_ang_hist, "Velocidad Angular ω (rad/s)", (255, 165, 0), 1)
        self.panel_graficos.dibujar_grafico(self.ventana, acel_ang_hist, "Aceleración Angular α (rad/s²)", (0, 255, 128), 2)