import sys
import pygame
import numpy as np
from core.physics_engine import MotorFisico2D
from ui.renderer import Renderer

def main():
    pygame.init()

    ANCHO_VENTANA = 1050
    ALTO_VENTANA = 650
    ANCHO_SIM = 700

    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulador Físico - Brazo / Péndulo 1-DOF")
    reloj = pygame.time.Clock()

    fisica = MotorFisico2D(ancho_sim=ANCHO_SIM, alto_sim=450)
    renderizador = Renderer(ventana=ventana, ancho_sim=ANCHO_SIM, alto_ventana=ALTO_VENTANA)

    corriendo = True
    while corriendo:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    # Aplicar un golpe angular aleatorio al presionar espacio
                    fisica.aplicar_impulso(np.random.uniform(-3.0, 3.0))
            
            renderizador.manejar_eventos_sliders(evento)

        renderizador.actualizar_fisica_desde_sliders(fisica)
        fisica.actualizar(dt)

        renderizador.dibujar(fisica)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()