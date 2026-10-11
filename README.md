# Manifesto del Simulador Físico para Control e IA

Este documento describe la arquitectura modular del proyecto, indicando la responsabilidad de cada componente para mantener un código limpio, escalable y fácil de traducir a C/C++ en el futuro.

## Estructura y Responsabilidades de los Archivos

- **`main.py` (Punto de Entrada / Orquestador)**
  - **Responsabilidad:** Inicializa la aplicación, gestiona el bucle principal de tiempo (`delta time`), procesa los eventos globales (teclado, cierre de ventana) y coordina la comunicación entre el motor físico y la interfaz gráfica.

- **`core/physics_engine.py` (Modelo Físico)**
  - **Responsabilidad:** Contiene las ecuaciones puramente matemáticas y físicas (leyes de Newton, gravedad, fricción, fuerzas externas y colisiones). 
  - **Característica clave:** Es totalmente independiente de la interfaz gráfica. Esto permite extraer esta lógica fácilmente en el futuro para compilarla en C/C++ para hardware real.

- **`ui/renderer.py` (Interfaz Gráfica)**
  - **Responsabilidad:** Se encarga de todo el renderizado visual (dibujar objetos, paredes, vectores) y de mostrar el panel de control lateral con las variables de estado en tiempo real.