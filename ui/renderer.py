import pygame
from ui.slider import Slider
from ui.plotter import PanelGraficos

class Renderer:
    def __init__(self, ventana, ancho_sim, alto_ventana):
        self.ventana = ventana
        self.ancho_sim = ancho_sim
        self.alto_ventana = alto_ventana
        self.fuente = pygame.font.SysFont("Arial", 16)

        # Sliders en el panel derecho superior
        panel_x = ancho_sim + 30
        self.slider_masa = Slider(panel_x, 70, 220, 8, 0.5, 20.0, 2.5, "Masa (kg)")
        self.slider_elasticidad = Slider(panel_x, 140, 220, 8, 0.0, 1.0, 0.8, "Elasticidad")
        self.slider_friccion = Slider(panel_x, 210, 220, 8, 0.0, 0.2, 0.05, "Fricción")
        self.sliders = [self.slider_masa, self.slider_elasticidad, self.slider_friccion]

        # Panel de gráficos inferior (ocupa el ancho total de la ventana)
        self.panel_graficos = PanelGraficos(x=20, y=470, ancho=1010, alto=160)

    def manejar_eventos_sliders(self, evento):
        for slider in self.sliders:
            slider.manejar_evento(evento)

    def actualizar_fisica_desde_sliders(self, fisica):
        fisica.masa = self.slider_masa.valor
        fisica.elasticidad = self.slider_elasticidad.valor
        fisica.friccion = self.slider_friccion.valor

    def dibujar(self, fisica):
        self.ventana.fill((25, 25, 30))

        # 1. Área de simulación física (Arriba a la izquierda)
        alto_sim_caja = 430
        pygame.draw.rect(self.ventana, (40, 40, 48), (20, 20, self.ancho_sim - 40, alto_sim_caja), 2)
        
        pos_x, pos_y = int(fisica.pos[0]), int(fisica.pos[1])
        pygame.draw.circle(self.ventana, (0, 160, 255), (pos_x, pos_y), fisica.radio_objeto)
        pygame.draw.circle(self.ventana, (255, 255, 255), (pos_x, pos_y), 5)

        # 2. Panel de control / Sliders (Arriba a la derecha)
        panel_x = self.ancho_sim + 20
        pygame.draw.line(self.ventana, (70, 70, 80), (self.ancho_sim, 0), (self.ancho_sim, 450), 2)
        
        titulo = self.fuente.render("--- PANEL DE CONTROL ---", True, (255, 255, 255))
        self.ventana.blit(titulo, (panel_x, 25))

        for slider in self.sliders:
            slider.dibujar(self.ventana)

        # Telemetría en texto
        textos = [
            f"Pos Y: {fisica.pos[1]:.1f} px",
            f"Vel Y: {fisica.vel[1]:.1f} px/s",
            f"Acel Y: {fisica.ultima_aceleracion[1]:.1f} px/s²",
            "",
            "[ESPACIO]: Impulso"
        ]
        for i, texto in enumerate(textos):
            superficie_texto = self.fuente.render(texto, True, (200, 200, 200))
            self.ventana.blit(superficie_texto, (panel_x, 270 + (i * 22)))

        # 3. Separador horizontal para los gráficos
        pygame.draw.line(self.ventana, (70, 70, 80), (20, 450), (1030, 450), 2)

        # 4. Dibujar Gráficas Temporales (Abajo)
        _, pos_y_hist, vel_y_hist, acel_y_hist = fisica.obtener_telemetria()
        self.panel_graficos.dibujar_grafico(self.ventana, pos_y_hist, "Posición Y (px)", (0, 160, 255), 0)
        self.panel_graficos.dibujar_grafico(self.ventana, vel_y_hist, "Velocidad Y (px/s)", (255, 165, 0), 1)
        self.panel_graficos.dibujar_grafico(self.ventana, acel_y_hist, "Aceleración Y (px/s²)", (0, 255, 128), 2)