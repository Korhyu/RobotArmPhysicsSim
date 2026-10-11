import pygame

class Slider:
    def __init__(self, x, y, ancho, alto, valor_min, valor_max, valor_inicial, etiqueta):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.valor_min = valor_min
        self.valor_max = valor_max
        self.valor = valor_inicial
        self.etiqueta = etiqueta
        self.fuente = pygame.font.SysFont("Arial", 14)
        
        # Calcular posición inicial del círculo del slider (handle)
        self.handle_x = self.valor_a_pixel(valor_inicial)
        self.arrastrando = False

    val_min_px = property(lambda self: self.rect.x)
    val_max_px = property(lambda self: self.rect.x + self.rect.width)

    def valor_a_pixel(self, val):
        porcentaje = (val - self.valor_min) / (self.valor_max - self.valor_min)
        return self.rect.x + (porcentaje * self.rect.width)

    def pixel_a_valor(self, px):
        px = max(self.rect.x, min(px, self.rect.x + self.rect.width))
        porcentaje = (px - self.rect.x) / self.rect.width
        return self.valor_min + (porcentaje * (self.valor_max - self.valor_min))

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evento.pos) or pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, self.rect.height + 20).collidepoint(evento.pos):
                self.arrastrando = True
                self.handle_x = evento.pos[0]
                self.valor = self.pixel_a_valor(self.handle_x)
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.arrastrando = False
        elif evento.type == pygame.MOUSEMOTION:
            if self.arrastrando:
                self.handle_x = evento.pos[0]
                self.valor = self.pixel_a_valor(self.handle_x)

    def dibujar(self, superficie):
        # Etiqueta y valor actual
        texto = f"{self.etiqueta}: {self.valor:.2f}"
        sup_texto = self.fuente.render(texto, True, (220, 220, 220))
        superficie.blit(sup_texto, (self.rect.x, self.rect.y - 22))

        # Barra de fondo
        pygame.draw.rect(superficie, (70, 70, 80), self.rect, border_radius=4)
        
        # Círculo deslizante
        pygame.draw.circle(superficie, (0, 160, 255), (int(self.handle_x), self.rect.centery), 8)