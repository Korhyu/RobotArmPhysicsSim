import pygame

class PanelGraficos:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.fuente = pygame.font.SysFont("Arial", 11)

    def dibujar_grafico(self, superficie, valores, etiqueta, color, offset_x):
        # Sub-rectángulo para cada una de las 3 gráficas (Pos, Vel, Acel)
        ancho_sub = (self.rect.width - 40) // 3
        alto_sub = self.rect.height - 20
        x_sub = self.rect.x + 10 + offset_x * (ancho_sub + 10)
        y_sub = self.rect.y + 10

        sub_rect = pygame.Rect(x_sub, y_sub, ancho_sub, alto_sub)

        # Fondo del recuadro
        pygame.draw.rect(superficie, (35, 35, 42), sub_rect)
        pygame.draw.rect(superficie, (70, 70, 80), sub_rect, 1)

        # Etiqueta
        sup_texto = self.fuente.render(etiqueta, True, (200, 200, 200))
        superficie.blit(sup_texto, (sub_rect.x + 8, sub_rect.y + 5))

        if len(valores) < 2:
            return

        # Normalización y mapeo de datos
        min_val = min(valores)
        max_val = max(valores)
        rango_val = max_val - min_val if max_val - min_val != 0 else 1.0

        padding_y = 12
        ancho_util = sub_rect.width - 16
        alto_util = sub_rect.height - 25 - (padding_y * 2)

        puntos = []
        n = len(valores)
        for i, val in enumerate(valores):
            px = sub_rect.x + 8 + (i / (n - 1 if n > 1 else 1)) * ancho_util
            normalizado = (val - min_val) / rango_val
            py = sub_rect.y + sub_rect.height - padding_y - (normalizado * alto_util)
            puntos.append((int(px), int(py)))

        if len(puntos) > 1:
            pygame.draw.aalines(superficie, color, False, puntos)

        # Valor numérico actual
        val_actual = f"{valores[-1]:.1f}"
        sup_val = self.fuente.render(val_actual, True, color)
        superficie.blit(sup_val, (sub_rect.right - 45, sub_rect.y + 5))