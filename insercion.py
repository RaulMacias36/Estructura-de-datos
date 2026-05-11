"""
╔══════════════════════════════════════════════════════════════════════╗
║   Visualizador Educativo: Insertion Sort  vs  Bubble Sort           ║
║   Tecnología: Python 3 + Pygame                                     ║
║   Descripción: Animación paso a paso con comparativa de eficiencia  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import pygame
import random
import sys
from typing import List, Optional, Generator
from enum import Enum, auto
from dataclasses import dataclass


# ══════════════════════════════════════════════════════════════════════
# CONSTANTES Y CONFIGURACIÓN GLOBAL
# ══════════════════════════════════════════════════════════════════════

# — Ventana —
ANCHO = 1260
ALTO  = 720
FPS   = 60
TITULO = "Visualizador Educativo — Insertion Sort vs Bubble Sort vs Selection Sort"

# — Paleta de colores —
C_FONDO          = (15,  16,  28)
C_PANEL          = (22,  24,  42)
C_PANEL_BORDE    = (55,  60,  100)
C_TEXTO          = (210, 215, 230)
C_TEXTO_DEST     = (255, 215,  0)
C_BARRA_NORMAL   = (65,  120, 195)
C_BARRA_ACTUAL   = (255, 215,   0)   # Amarillo: elemento "flotante" / clave
C_BARRA_COMP     = (230,  80,  80)   # Rojo: elemento siendo comparado
C_BARRA_SORTED   = (70,  200, 120)   # Verde: ya ordenado
C_BARRA_SOMBRA   = (35,  60,  100)   # Sombra bajo barra elevada
C_BTN            = (50,  52,  85)
C_BTN_HOVER      = (80,  85,  135)
C_BTN_TXT        = (210, 215, 255)
C_SLIDER_FONDO   = (45,  48,  80)
C_SLIDER_ACTIVO  = (90,  170, 255)
C_ACENTO_INS     = (90,  165, 255)   # Azul — Insertion Sort
C_ACENTO_BUB     = (255, 140,  55)   # Naranja — Bubble Sort
C_ACENTO_SEL     = (180,  90, 255)   # Violeta — Selection Sort

# — Layout —
MARGEN           = 14
ANCHO_CTRL       = 258                          # Panel de controles izquierdo
ANCHO_VIZ        = (ANCHO - ANCHO_CTRL - MARGEN * 5) // 3   # Zona de cada algoritmo
ALTO_VIZ         = 300
Y_VIZ            = 130
X_INS            = ANCHO_CTRL + MARGEN * 2
X_BUB            = X_INS + ANCHO_VIZ + MARGEN
X_SEL            = X_BUB + ANCHO_VIZ + MARGEN

# — Barras —
N_ELEMENTOS      = 32
ALTO_MAX_BARRA   = ALTO_VIZ - 30
ELEVACION        = 28    # píxeles que sube la "ficha flotante"
MARGEN_BARRA     = 2

# — Velocidad (frames entre pasos) —
VEL_MIN          = 1
VEL_MAX          = 60
VEL_INICIAL      = 18


# ══════════════════════════════════════════════════════════════════════
# ENUMS Y DATACLASSES
# ══════════════════════════════════════════════════════════════════════

class Estado(Enum):
    ESPERANDO  = auto()
    ORDENANDO  = auto()
    FINALIZADO = auto()


@dataclass
class InfoPaso:
    """
    Instantánea del estado visual en un paso del algoritmo.
    Se genera en cada 'yield' del generador correspondiente.
    """
    mensaje:      str  = ""
    idx_actual:   int  = -1   # índice del elemento activo / clave
    idx_comp:     int  = -1   # índice del elemento comparado
    sorted_hasta: int  = -1   # límite de la zona ya ordenada
    elevado:      bool = False # ¿debe dibujarse la barra elevada?


@dataclass
class Estadisticas:
    """Contadores de rendimiento del algoritmo."""
    nombre:        str = ""
    comparaciones: int = 0
    movimientos:   int = 0

    def reset(self):
        self.comparaciones = 0
        self.movimientos   = 0


# ══════════════════════════════════════════════════════════════════════
# GENERADORES DE ALGORITMOS  (paso a paso con yield)
# ══════════════════════════════════════════════════════════════════════

def gen_insertion_sort(arr: List[int], stats: Estadisticas) -> Generator:
    """
    Insertion Sort como generador Python.
    Cada 'yield' entrega un InfoPaso listo para renderizar.

    Complejidad: O(n²) peor caso | O(n) mejor caso (lista ordenada).
    Estrategia: selecciona un elemento (clave), lo "levanta" y
    desplaza los mayores hacia la derecha hasta encontrar su hueco.
    """
    n = len(arr)
    stats.reset()

    for i in range(1, n):
        clave = arr[i]

        # ── Paso 1: Tomar la clave ──
        yield InfoPaso(
            mensaje      = f"Tomando clave [{clave}] en posición {i}",
            idx_actual   = i,
            idx_comp     = -1,
            sorted_hasta = i - 1,
            elevado      = True
        )

        j = i - 1  # puntero de comparación hacia la izquierda

        while j >= 0:
            stats.comparaciones += 1

            # ── Paso 2: Comparar ──
            yield InfoPaso(
                mensaje      = f"¿[{clave}] < [{arr[j]}]? → {'Sí, desplazar' if arr[j] > clave else 'No, insertar aquí'}",
                idx_actual   = j + 1,   # posición del "hueco" actual
                idx_comp     = j,
                sorted_hasta = i - 1,
                elevado      = True
            )

            if arr[j] > clave:
                # ── Paso 3: Desplazar elemento mayor → derecha ──
                arr[j + 1] = arr[j]
                stats.movimientos += 1

                yield InfoPaso(
                    mensaje      = f"Desplazando [{arr[j + 1]}] → posición {j + 1}",
                    idx_actual   = j,       # el hueco avanza a la izquierda
                    idx_comp     = j + 1,
                    sorted_hasta = i - 1,
                    elevado      = True
                )
                j -= 1
            else:
                break   # posición correcta encontrada

        # ── Paso 4: Insertar la clave en su posición ──
        arr[j + 1] = clave
        stats.movimientos += 1

        yield InfoPaso(
            mensaje      = f"✔ Insertando [{clave}] en posición {j + 1}",
            idx_actual   = j + 1,
            idx_comp     = -1,
            sorted_hasta = i,
            elevado      = False
        )

    # ── Finalizado ──
    yield InfoPaso(
        mensaje      = "✓ ¡Insertion Sort completado!",
        idx_actual   = -1,
        idx_comp     = -1,
        sorted_hasta = n - 1,
        elevado      = False
    )


def gen_bubble_sort(arr: List[int], stats: Estadisticas) -> Generator:
    """
    Bubble Sort como generador Python.
    Cada 'yield' entrega un InfoPaso listo para renderizar.

    Complejidad: O(n²) en casi todos los casos.
    Estrategia: burbujea el máximo hacia la derecha en cada pasada.
    """
    n = len(arr)
    stats.reset()

    for i in range(n - 1):
        intercambiado = False

        for j in range(0, n - i - 1):
            stats.comparaciones += 1

            # ── Comparar vecinos ──
            yield InfoPaso(
                mensaje      = f"Comparando [{arr[j]}] y [{arr[j + 1]}]",
                idx_actual   = j,
                idx_comp     = j + 1,
                sorted_hasta = n - i,   # zona ordenada crece desde el final
                elevado      = False
            )

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                stats.movimientos += 2  # 2 escrituras por intercambio

                yield InfoPaso(
                    mensaje      = f"Intercambiando [{arr[j + 1]}] ↔ [{arr[j]}]",
                    idx_actual   = j + 1,
                    idx_comp     = j,
                    sorted_hasta = n - i,
                    elevado      = False
                )
                intercambiado = True

        if not intercambiado:
            break  # optimización: lista ya ordenada

    yield InfoPaso(
        mensaje      = "✓ ¡Bubble Sort completado!",
        idx_actual   = -1,
        idx_comp     = -1,
        sorted_hasta = n - 1,
        elevado      = False
    )


def gen_selection_sort(arr: List[int], stats: Estadisticas) -> Generator:
    """
    Selection Sort como generador Python.
    Cada 'yield' entrega un InfoPaso listo para renderizar.

    Complejidad: O(n²) en todos los casos.
    Estrategia: busca el mínimo en la parte no ordenada e intercambia
    con la primera posición libre; la zona ordenada crece desde el inicio.
    """
    n = len(arr)
    stats.reset()

    for i in range(n - 1):
        idx_min = i

        yield InfoPaso(
            mensaje      = f"Buscando mínimo desde posición {i}",
            idx_actual   = idx_min,
            idx_comp     = -1,
            sorted_hasta = i - 1,
            elevado      = False
        )

        for j in range(i + 1, n):
            stats.comparaciones += 1

            yield InfoPaso(
                mensaje      = f"¿[{arr[j]}] < mínimo [{arr[idx_min]}]? → {'Sí, nuevo mínimo' if arr[j] < arr[idx_min] else 'No'}",
                idx_actual   = idx_min,
                idx_comp     = j,
                sorted_hasta = i - 1,
                elevado      = False
            )

            if arr[j] < arr[idx_min]:
                idx_min = j
                yield InfoPaso(
                    mensaje      = f"Nuevo mínimo: [{arr[idx_min]}] en posición {idx_min}",
                    idx_actual   = idx_min,
                    idx_comp     = j,
                    sorted_hasta = i - 1,
                    elevado      = False
                )

        if idx_min != i:
            arr[i], arr[idx_min] = arr[idx_min], arr[i]
            stats.movimientos += 2

            yield InfoPaso(
                mensaje      = f"Intercambiando [{arr[i]}] pos {i} ↔ [{arr[idx_min]}] pos {idx_min}",
                idx_actual   = i,
                idx_comp     = idx_min,
                sorted_hasta = i - 1,
                elevado      = False
            )

        yield InfoPaso(
            mensaje      = f"✔ [{arr[i]}] colocado en posición {i}",
            idx_actual   = i,
            idx_comp     = -1,
            sorted_hasta = i,
            elevado      = False
        )

    yield InfoPaso(
        mensaje      = "✓ ¡Selection Sort completado!",
        idx_actual   = -1,
        idx_comp     = -1,
        sorted_hasta = n - 1,
        elevado      = False
    )


# ══════════════════════════════════════════════════════════════════════
# COMPONENTES DE INTERFAZ
# ══════════════════════════════════════════════════════════════════════

class Boton:
    """Botón rectangular con efecto hover y borde redondeado."""

    def __init__(self, x: int, y: int, ancho: int, alto: int, texto: str):
        self.rect   = pygame.Rect(x, y, ancho, alto)
        self.texto  = texto
        self.hover  = False

    def dibujar(self, sup: pygame.Surface, fuente: pygame.font.Font):
        color = C_BTN_HOVER if self.hover else C_BTN
        pygame.draw.rect(sup, color, self.rect, border_radius=8)
        pygame.draw.rect(sup, C_PANEL_BORDE, self.rect, 1, border_radius=8)
        lbl = fuente.render(self.texto, True, C_BTN_TXT)
        sup.blit(lbl, lbl.get_rect(center=self.rect.center))

    def actualizar_hover(self, pos: tuple):
        self.hover = self.rect.collidepoint(pos)

    def clickeado(self, ev: pygame.event.Event) -> bool:
        return (ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and self.rect.collidepoint(ev.pos))


class Slider:
    """
    Deslizador horizontal para controlar la velocidad de animación.
    Valor alto → más frames por paso → animación más lenta.
    """

    def __init__(self, x: int, y: int, ancho: int,
                 val_min: int, val_max: int, valor: int):
        self.x          = x
        self.y          = y
        self.ancho      = ancho
        self.val_min    = val_min
        self.val_max    = val_max
        self.valor      = valor
        self._arrastrando = False

    # ── Propiedades calculadas ──
    @property
    def _pct(self) -> float:
        return (self.valor - self.val_min) / (self.val_max - self.val_min)

    @property
    def _x_perilla(self) -> int:
        return int(self.x + self._pct * self.ancho)

    @property
    def frames_por_paso(self) -> int:
        """Cuántos frames de pygame transcurren entre pasos del algoritmo."""
        return self.valor

    def dibujar(self, sup: pygame.Surface, fuente: pygame.font.Font):
        # Riel completo
        riel = pygame.Rect(self.x, self.y - 3, self.ancho, 6)
        pygame.draw.rect(sup, C_SLIDER_FONDO, riel, border_radius=3)
        # Riel activo (izquierda hasta perilla)
        activo = pygame.Rect(self.x, self.y - 3,
                             self._x_perilla - self.x, 6)
        pygame.draw.rect(sup, C_SLIDER_ACTIVO, activo, border_radius=3)
        # Perilla
        pygame.draw.circle(sup, C_SLIDER_ACTIVO, (self._x_perilla, self.y), 10)
        pygame.draw.circle(sup, C_TEXTO,         (self._x_perilla, self.y), 10, 2)
        # Etiqueta (mostramos velocidad inversa: slider derecha = rápido)
        vel_vis = self.val_max + self.val_min - self.valor
        lbl = fuente.render(f"Velocidad: {vel_vis:2d}x   (↑/↓ o arrastra)",
                            True, C_TEXTO)
        sup.blit(lbl, (self.x, self.y + 14))

    def manejar_evento(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if abs(ev.pos[0] - self._x_perilla) <= 14 and abs(ev.pos[1] - self.y) <= 14:
                self._arrastrando = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            self._arrastrando = False
        elif ev.type == pygame.MOUSEMOTION and self._arrastrando:
            px = max(self.x, min(ev.pos[0], self.x + self.ancho))
            self.valor = int(self.val_min
                             + (px - self.x) / self.ancho
                             * (self.val_max - self.val_min))


class EntradaTexto:
    """Campo de texto para ingresar valores separados por comas."""

    def __init__(self, x: int, y: int, ancho: int, alto: int):
        self.rect   = pygame.Rect(x, y, ancho, alto)
        self.texto  = ""
        self.activa = False

    def manejar_evento(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            self.activa = self.rect.collidepoint(ev.pos)
        if ev.type == pygame.KEYDOWN and self.activa:
            if ev.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif ev.key not in (pygame.K_RETURN, pygame.K_ESCAPE,
                                pygame.K_TAB, pygame.K_UP, pygame.K_DOWN):
                self.texto += ev.unicode

    def dibujar(self, sup: pygame.Surface, fuente: pygame.font.Font):
        color_borde = C_SLIDER_ACTIVO if self.activa else C_PANEL_BORDE
        pygame.draw.rect(sup, (30, 32, 55), self.rect, border_radius=4)
        pygame.draw.rect(sup, color_borde, self.rect, 2, border_radius=4)
        cursor  = "|" if self.activa else ""
        display = self.texto
        while fuente.size(display + cursor)[0] > self.rect.width - 8 and display:
            display = display[1:]
        lbl = fuente.render(display + cursor, True, C_TEXTO)
        sup.blit(lbl, (self.rect.x + 4,
                       self.rect.y + (self.rect.height - lbl.get_height()) // 2))


# ══════════════════════════════════════════════════════════════════════
# FUNCIONES DE DIBUJO
# ══════════════════════════════════════════════════════════════════════

def dibujar_barras(
    sup: pygame.Surface,
    datos: List[int],
    info: InfoPaso,
    x0: int, y0: int,
    ancho: int, alto: int,
    es_burbuja: bool,
    mostrar_valores: bool = False,
    f_valor: Optional[pygame.font.Font] = None
):
    """
    Dibuja las barras verticales que representan el array.

    Parámetros:
        sup             — superficie pygame donde dibujar
        datos           — array de enteros (estado actual)
        info            — estado del paso (índices resaltados, elevación…)
        x0, y0          — origen del área de barras
        ancho, alto     — dimensiones del área
        es_burbuja      — true si es Bubble Sort (lógica de "sorted" invertida)
        mostrar_valores — si True dibuja el valor numérico sobre cada barra
        f_valor         — fuente para los números (requerida si mostrar_valores)
    """
    n = len(datos)
    if not n:
        return

    ancho_barra    = max(2, (ancho - MARGEN_BARRA * (n - 1)) // n)
    val_max        = max(datos)
    base_y         = y0 + alto   # línea base (parte inferior de las barras)
    alto_max_barra = alto - 30   # escala las barras al área real del panel

    for idx, valor in enumerate(datos):
        alto_barra = max(4, int((valor / val_max) * alto_max_barra))
        x_barra    = x0 + idx * (ancho_barra + MARGEN_BARRA)

        # ── Determinar si idx está en zona "ya ordenada" ──
        if es_burbuja:
            # Bubble: la zona ordenada crece desde el final
            ya_ordenado = (info.sorted_hasta != -1
                           and idx >= info.sorted_hasta)
        else:
            # Insertion: la zona ordenada crece desde el inicio
            ya_ordenado = (info.sorted_hasta != -1
                           and idx <= info.sorted_hasta
                           and idx != info.idx_actual)

        # ── Elegir color según rol ──
        if idx == info.idx_actual:
            color = C_BARRA_ACTUAL
        elif idx == info.idx_comp:
            color = C_BARRA_COMP
        elif ya_ordenado:
            color = C_BARRA_SORTED
        else:
            color = C_BARRA_NORMAL

        # ── Elevación del elemento activo (solo Insertion Sort) ──
        offset_y = 0
        if idx == info.idx_actual and info.elevado and not es_burbuja:
            offset_y = -ELEVACION
            # Sombra difusa bajo la barra levantada
            rect_sombra = pygame.Rect(
                x_barra + 4, base_y - alto_barra + 4,
                ancho_barra, alto_barra
            )
            pygame.draw.rect(sup, C_BARRA_SOMBRA, rect_sombra, border_radius=3)

        rect = pygame.Rect(
            x_barra,
            base_y - alto_barra + offset_y,
            ancho_barra,
            alto_barra
        )
        pygame.draw.rect(sup, color, rect, border_radius=3)

        # ── Valor numérico sobre la barra ──
        if mostrar_valores and f_valor:
            txt = f_valor.render(str(valor), True, C_TEXTO)
            tw, th = txt.get_size()
            tx = x_barra + (ancho_barra - tw) // 2
            ty = base_y - alto_barra + offset_y - th - 2
            if ty >= y0 - th:
                sup.blit(txt, (tx, ty))


def truncar_texto(texto: str, fuente: pygame.font.Font, max_ancho: int) -> str:
    """Trunca un string para que no supere max_ancho píxeles."""
    if fuente.size(texto)[0] <= max_ancho:
        return texto
    while texto and fuente.size(texto + "…")[0] > max_ancho:
        texto = texto[:-1]
    return texto + "…"


def dibujar_panel_algoritmo(
    sup: pygame.Surface,
    titulo: str,
    datos: List[int],
    info: InfoPaso,
    stats: Estadisticas,
    estado: Estado,
    x: int, y: int,
    ancho: int, alto: int,
    acento: tuple,
    es_burbuja: bool,
    f_titulo: pygame.font.Font,
    f_info: pygame.font.Font,
    mostrar_valores: bool = False,
    f_valor: Optional[pygame.font.Font] = None
):
    """
    Dibuja el panel completo de un algoritmo:
    borde, título, zona de barras, contadores y mensaje.
    """
    # Fondo del panel
    rect_panel = pygame.Rect(x - 12, y - 28, ancho + 24, alto + 130)
    pygame.draw.rect(sup, C_PANEL, rect_panel, border_radius=10)
    pygame.draw.rect(sup, acento,  rect_panel, 2,  border_radius=10)

    # Título del panel
    lbl = f_titulo.render(titulo, True, acento)
    sup.blit(lbl, (x, y - 24))

    # Zona de barras
    dibujar_barras(sup, datos, info, x, y, ancho, alto, es_burbuja,
                   mostrar_valores, f_valor)

    # Línea base decorativa
    pygame.draw.line(sup, C_PANEL_BORDE,
                     (x, y + alto), (x + ancho, y + alto), 1)

    # ── Contadores ──
    y_stats = y + alto + 8
    comp_txt = f_info.render(
        f"Comparaciones : {stats.comparaciones:>5}", True, C_TEXTO)
    mov_txt  = f_info.render(
        f"Movimientos   : {stats.movimientos:>5}",   True, C_TEXTO)
    sup.blit(comp_txt, (x, y_stats))
    sup.blit(mov_txt,  (x, y_stats + 20))

    # ── Mensaje de estado ──
    y_msg = y_stats + 46
    if estado == Estado.FINALIZADO:
        color_msg = C_BARRA_SORTED
        msg       = info.mensaje
    elif estado == Estado.ORDENANDO:
        color_msg = C_TEXTO_DEST
        msg       = info.mensaje
    else:
        color_msg = (150, 155, 175)
        msg       = "Listo. Presiona '▶ Iniciar' o SPACE."

    msg_corto = truncar_texto(msg, f_info, ancho)
    sup.blit(f_info.render(msg_corto, True, color_msg), (x, y_msg))


# ══════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL DE LA APLICACIÓN
# ══════════════════════════════════════════════════════════════════════

class Aplicacion:
    """
    Gestiona el estado global, el bucle de eventos (MVC-lite)
    y delega el renderizado a las funciones de dibujo.
    """

    def __init__(self):
        pygame.init()
        self.sup    = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj  = pygame.time.Clock()
        pygame.display.set_caption(TITULO)

        # ── Fuentes ──
        self.f_app    = pygame.font.SysFont("Consolas", 19, bold=True)
        self.f_titulo = pygame.font.SysFont("Consolas", 16, bold=True)
        self.f_medio  = pygame.font.SysFont("Consolas", 15, bold=True)
        self.f_pequeño = pygame.font.SysFont("Consolas", 13)
        self.f_mini   = pygame.font.SysFont("Consolas", 11)

        # ── Datos ──
        self.datos_ins: List[int] = []
        self.datos_bub: List[int] = []
        self.datos_sel: List[int] = []
        self._generar_lista()

        # ── Estado ──
        self.estado_ins = Estado.ESPERANDO
        self.estado_bub = Estado.ESPERANDO
        self.estado_sel = Estado.ESPERANDO
        self.info_ins   = InfoPaso()
        self.info_bub   = InfoPaso()
        self.info_sel   = InfoPaso()

        # ── Estadísticas ──
        self.stats_ins = Estadisticas(nombre="Insertion Sort")
        self.stats_bub = Estadisticas(nombre="Bubble Sort")
        self.stats_sel = Estadisticas(nombre="Selection Sort")

        # ── Generadores ──
        self.gen_ins: Optional[Generator] = None
        self.gen_bub: Optional[Generator] = None
        self.gen_sel: Optional[Generator] = None

        # ── Control de velocidad ──
        self.slider    = Slider(
            x=MARGEN + 8, y=198,
            ancho=ANCHO_CTRL - 20,
            val_min=VEL_MIN, val_max=VEL_MAX, valor=VEL_INICIAL
        )
        self.frame_ins = 0
        self.frame_bub = 0
        self.frame_sel = 0

        # ── Botones ──
        bx, bw = MARGEN + 4, ANCHO_CTRL - 8
        self.btn_nueva     = Boton(bx, 255, bw, 36, "🔀  Nueva Lista  (N)")
        self.btn_iniciar   = Boton(bx, 298, bw, 36, "▶  Iniciar  (SPACE)")
        self.btn_reiniciar = Boton(bx, 341, bw, 36, "↺  Reiniciar  (R)")
        self._botones      = [self.btn_nueva, self.btn_iniciar, self.btn_reiniciar]

        # ── Pestañas ──
        self.pestaña    = 0
        ancho_zona_tabs = ANCHO_VIZ * 3 + MARGEN * 2 + 24
        tw = ancho_zona_tabs // 2 - 2
        tx0 = X_INS - 12
        self._rect_tab0 = pygame.Rect(tx0,          53, tw, 28)
        self._rect_tab1 = pygame.Rect(tx0 + tw + 4, 53, tw, 28)

        # ── Controles pestaña 2 ──
        ix = MARGEN + 4
        iw = ANCHO_CTRL - 8
        self.entrada_vals  = EntradaTexto(ix, 432, iw, 26)
        self.btn_aplicar   = Boton(ix, 466, iw, 30, "Aplicar  (Enter)")
        self.btn_paso      = Boton(ix, 558, iw, 36, "▶|  Siguiente Paso  (→)")
        self._n_custom     = N_ELEMENTOS
        self._error_input  = ""

    # ── Helpers de estado ──────────────────────────────────────────────

    def _generar_lista(self):
        """Crea una lista aleatoria nueva (la misma base para los tres algoritmos)."""
        base = random.sample(range(5, 101), N_ELEMENTOS)
        self.datos_ins = base[:]
        self.datos_bub = base[:]
        self.datos_sel = base[:]
        self._n_custom = N_ELEMENTOS
        self._error_input = ""

    def _reiniciar_estado(self):
        """Resetea el estado de los algoritmos sin tocar los datos."""
        self.gen_ins = self.gen_bub = self.gen_sel = None
        self.estado_ins = self.estado_bub = self.estado_sel = Estado.ESPERANDO
        self.info_ins = InfoPaso()
        self.info_bub = InfoPaso()
        self.info_sel = InfoPaso()
        self.stats_ins.reset()
        self.stats_bub.reset()
        self.stats_sel.reset()

    def _iniciar(self):
        """Arranca los tres generadores desde cero."""
        self.gen_ins    = gen_insertion_sort(self.datos_ins, self.stats_ins)
        self.gen_bub    = gen_bubble_sort   (self.datos_bub, self.stats_bub)
        self.gen_sel    = gen_selection_sort(self.datos_sel, self.stats_sel)
        self.estado_ins = Estado.ORDENANDO
        self.estado_bub = Estado.ORDENANDO
        self.estado_sel = Estado.ORDENANDO
        self.frame_ins  = self.frame_bub = self.frame_sel = 0

    def _reiniciar(self):
        """Detiene algoritmos, genera lista nueva y vuelve al estado inicial."""
        self._reiniciar_estado()
        self._generar_lista()

    def _avanzar(self, gen: Optional[Generator],
                 info: InfoPaso, estado: Estado):
        """Avanza un generador un paso; retorna (nuevo_info, nuevo_estado)."""
        if gen is None or estado != Estado.ORDENANDO:
            return info, estado
        try:
            return next(gen), Estado.ORDENANDO
        except StopIteration:
            return info, Estado.FINALIZADO

    # ── Bucle principal ───────────────────────────────────────────────

    def manejar_eventos(self):
        pos = pygame.mouse.get_pos()
        for btn in self._botones:
            btn.actualizar_hover(pos)
        self.btn_aplicar.actualizar_hover(pos)
        self.btn_paso.actualizar_hover(pos)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Teclado
            if ev.type == pygame.KEYDOWN:
                # Cambio de pestaña: siempre activo
                if ev.key == pygame.K_1:
                    self.pestaña = 0
                elif ev.key == pygame.K_2:
                    self.pestaña = 1
                elif self.pestaña == 1 and self.entrada_vals.activa:
                    # Cuando el campo está activo, Enter aplica los valores
                    if ev.key == pygame.K_RETURN:
                        self._aplicar_valores_custom()
                    # el resto de teclas las captura EntradaTexto
                else:
                    if ev.key == pygame.K_UP:
                        self.slider.valor = max(VEL_MIN, self.slider.valor - 4)
                    elif ev.key == pygame.K_DOWN:
                        self.slider.valor = min(VEL_MAX, self.slider.valor + 4)
                    elif ev.key == pygame.K_SPACE:
                        if self.estado_ins != Estado.ORDENANDO:
                            self._reiniciar(); self._iniciar()
                    elif ev.key == pygame.K_r:
                        self._reiniciar()
                    elif ev.key == pygame.K_n:
                        self._reiniciar()
                    elif ev.key == pygame.K_RIGHT and self.pestaña == 1:
                        self._paso_manual_ins()

            # Pestañas
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self._rect_tab0.collidepoint(ev.pos):
                    self.pestaña = 0
                elif self._rect_tab1.collidepoint(ev.pos):
                    self.pestaña = 1

            # Campo de texto (siempre recibe el evento; solo actúa si está activo)
            self.entrada_vals.manejar_evento(ev)

            # Slider
            self.slider.manejar_evento(ev)

            # Botones comunes
            if self.btn_nueva.clickeado(ev):
                self._reiniciar()
            if self.btn_iniciar.clickeado(ev):
                self._reiniciar(); self._iniciar()
            if self.btn_reiniciar.clickeado(ev):
                self._reiniciar()

            # Botones exclusivos de la pestaña 2
            if self.pestaña == 1:
                if self.btn_aplicar.clickeado(ev):
                    self._aplicar_valores_custom()
                if self.btn_paso.clickeado(ev):
                    self._paso_manual_ins()

    def actualizar(self):
        """Avanza cada algoritmo según los frames configurados."""
        fps = self.slider.frames_por_paso

        # Insertion Sort — en pestaña 2 solo avanza con el botón manual
        if self.estado_ins == Estado.ORDENANDO and self.pestaña == 0:
            self.frame_ins += 1
            if self.frame_ins >= fps:
                self.frame_ins = 0
                self.info_ins, self.estado_ins = self._avanzar(
                    self.gen_ins, self.info_ins, self.estado_ins)

        # Bubble Sort
        if self.estado_bub == Estado.ORDENANDO:
            self.frame_bub += 1
            if self.frame_bub >= fps:
                self.frame_bub = 0
                self.info_bub, self.estado_bub = self._avanzar(
                    self.gen_bub, self.info_bub, self.estado_bub)

        # Selection Sort
        if self.estado_sel == Estado.ORDENANDO:
            self.frame_sel += 1
            if self.frame_sel >= fps:
                self.frame_sel = 0
                self.info_sel, self.estado_sel = self._avanzar(
                    self.gen_sel, self.info_sel, self.estado_sel)

    def dibujar(self):
        """Renderiza la interfaz completa."""
        self.sup.fill(C_FONDO)

        # ── Encabezado ──
        titulo_app = self.f_app.render(
            "Insertion Sort  vs  Bubble Sort  vs  Selection Sort  —  Visualizador Educativo",
            True, C_TEXTO)
        self.sup.blit(titulo_app, titulo_app.get_rect(centerx=ANCHO // 2, y=10))

        subtitulo = self.f_pequeño.render(
            "Misma lista aleatoria · Contadores en tiempo real · "
            "Comparativa de eficiencia al finalizar",
            True, (130, 135, 160))
        self.sup.blit(subtitulo, subtitulo.get_rect(centerx=ANCHO // 2, y=34))

        self._dibujar_tabs()
        self._dibujar_panel_ctrl()
        if self.pestaña == 0:
            self._dibujar_algoritmos()
            self._dibujar_panel_teoria()
        else:
            self._dibujar_pestaña_insercion()

        pygame.display.flip()

    # ── Subfunciones de dibujo ────────────────────────────────────────

    def _dibujar_panel_ctrl(self):
        """Panel lateral izquierdo: controles, slider, botones, leyenda."""
        rect = pygame.Rect(MARGEN, 52, ANCHO_CTRL, ALTO - 62)
        pygame.draw.rect(self.sup, C_PANEL, rect, border_radius=10)
        pygame.draw.rect(self.sup, C_PANEL_BORDE, rect, 1, border_radius=10)

        # — Título sección —
        lbl = self.f_medio.render("⚙  CONTROLES", True, C_TEXTO_DEST)
        self.sup.blit(lbl, (MARGEN + 10, 62))

        # — Atajos —
        atajos = [
            "SPACE   Iniciar / Reiniciar",
            "R / N   Reiniciar / Nueva lista",
            "↑ / ↓   Velocidad más rápida/lenta",
        ]
        for i, a in enumerate(atajos):
            self.sup.blit(self.f_pequeño.render(a, True, (165, 170, 190)),
                          (MARGEN + 10, 84 + i * 18))

        # — Separador —
        pygame.draw.line(self.sup, C_PANEL_BORDE,
                         (MARGEN + 6, 148), (MARGEN + ANCHO_CTRL - 6, 148))

        lbl2 = self.f_pequeño.render("VELOCIDAD DE ANIMACIÓN", True, (140, 145, 170))
        self.sup.blit(lbl2, (MARGEN + 10, 155))

        # — Slider —
        self.slider.dibujar(self.sup, self.f_pequeño)

        # — Botones —
        for btn in self._botones:
            btn.dibujar(self.sup, self.f_pequeño)

        # — Separador —
        y_sep = 390
        pygame.draw.line(self.sup, C_PANEL_BORDE,
                         (MARGEN + 6, y_sep), (MARGEN + ANCHO_CTRL - 6, y_sep))

        if self.pestaña == 0:
            # — Leyenda de colores —
            lbl3 = self.f_pequeño.render("LEYENDA DE COLORES", True, (140, 145, 170))
            self.sup.blit(lbl3, (MARGEN + 10, y_sep + 8))

            leyenda = [
                (C_BARRA_ACTUAL,  "Elemento activo / clave"),
                (C_BARRA_COMP,    "Elemento comparado"),
                (C_BARRA_NORMAL,  "Sin procesar"),
                (C_BARRA_SORTED,  "Zona ya ordenada"),
            ]
            for i, (color, texto) in enumerate(leyenda):
                y_l = y_sep + 30 + i * 22
                pygame.draw.rect(self.sup, color,
                                 (MARGEN + 10, y_l, 12, 12), border_radius=3)
                self.sup.blit(self.f_pequeño.render(texto, True, C_TEXTO),
                              (MARGEN + 28, y_l - 1))

            nota = self.f_pequeño.render("↑ En Inserción, la clave sube",
                                         True, (120, 125, 150))
            nota2 = self.f_pequeño.render("  sobre las demás barras.",
                                          True, (120, 125, 150))
            self.sup.blit(nota,  (MARGEN + 10, y_sep + 122))
            self.sup.blit(nota2, (MARGEN + 10, y_sep + 138))

            if (self.estado_ins == Estado.FINALIZADO
                    and self.estado_bub == Estado.FINALIZADO
                    and self.estado_sel == Estado.FINALIZADO):
                self._dibujar_comparativa_final(y_sep + 170)

        else:
            # — Controles exclusivos de la pestaña 2 —
            self.sup.blit(
                self.f_pequeño.render("PERSONALIZAR LISTA", True, (140, 145, 170)),
                (MARGEN + 10, y_sep + 8))
            self.sup.blit(
                self.f_pequeño.render("Números separados por comas:", True, C_TEXTO),
                (MARGEN + 10, y_sep + 26))

            self.entrada_vals.dibujar(self.sup, self.f_pequeño)
            self.btn_aplicar.dibujar(self.sup, self.f_pequeño)

            # Estado / error
            if self._error_input:
                info_txt   = self._error_input
                info_color = C_BARRA_COMP
            else:
                info_txt   = f"Cargado: {self._n_custom} elemento(s)"
                info_color = C_BARRA_SORTED
            self.sup.blit(
                self.f_pequeño.render(info_txt, True, info_color),
                (MARGEN + 10, y_sep + 104))

            pygame.draw.line(self.sup, C_PANEL_BORDE,
                             (MARGEN + 6, y_sep + 122),
                             (MARGEN + ANCHO_CTRL - 6, y_sep + 122))

            self.sup.blit(
                self.f_pequeño.render("PASO A PASO", True, (140, 145, 170)),
                (MARGEN + 10, y_sep + 130))
            self.sup.blit(
                self.f_pequeño.render("Clic o tecla  →  para avanzar:",
                                      True, (165, 170, 190)),
                (MARGEN + 10, y_sep + 148))

            self.btn_paso.dibujar(self.sup, self.f_pequeño)

    def _dibujar_comparativa_final(self, y: int):
        """Muestra tabla de contadores al finalizar los tres algoritmos."""
        lbl = self.f_medio.render("COMPARATIVA FINAL", True, C_TEXTO_DEST)
        self.sup.blit(lbl, (MARGEN + 10, y))

        # Cabecera
        hdr = self.f_pequeño.render("             comp.   mov.", True, (140, 145, 170))
        self.sup.blit(hdr, (MARGEN + 10, y + 20))

        stats = [
            ("Inserción: ", self.stats_ins, C_ACENTO_INS),
            ("Burbuja:   ", self.stats_bub, C_ACENTO_BUB),
            ("Selección: ", self.stats_sel, C_ACENTO_SEL),
        ]

        min_comp = min(s.comparaciones for _, s, _ in stats)
        min_mov  = min(s.movimientos   for _, s, _ in stats)

        for i, (etq, s, color) in enumerate(stats):
            marca_c = "←" if s.comparaciones == min_comp else "  "
            marca_m = "←" if s.movimientos   == min_mov  else "  "
            txt = f"{etq}{s.comparaciones:>5}{marca_c}  {s.movimientos:>5}{marca_m}"
            self.sup.blit(self.f_pequeño.render(txt, True, color),
                          (MARGEN + 10, y + 38 + i * 19))

    def _dibujar_algoritmos(self):
        """Dibuja los tres paneles de visualización de algoritmos."""
        dibujar_panel_algoritmo(
            sup=self.sup, titulo="  INSERTION SORT",
            datos=self.datos_ins, info=self.info_ins,
            stats=self.stats_ins, estado=self.estado_ins,
            x=X_INS, y=Y_VIZ,
            ancho=ANCHO_VIZ, alto=ALTO_VIZ,
            acento=C_ACENTO_INS, es_burbuja=False,
            f_titulo=self.f_medio, f_info=self.f_pequeño
        )
        dibujar_panel_algoritmo(
            sup=self.sup, titulo="  BUBBLE SORT",
            datos=self.datos_bub, info=self.info_bub,
            stats=self.stats_bub, estado=self.estado_bub,
            x=X_BUB, y=Y_VIZ,
            ancho=ANCHO_VIZ, alto=ALTO_VIZ,
            acento=C_ACENTO_BUB, es_burbuja=True,
            f_titulo=self.f_medio, f_info=self.f_pequeño
        )
        dibujar_panel_algoritmo(
            sup=self.sup, titulo="  SELECTION SORT",
            datos=self.datos_sel, info=self.info_sel,
            stats=self.stats_sel, estado=self.estado_sel,
            x=X_SEL, y=Y_VIZ,
            ancho=ANCHO_VIZ, alto=ALTO_VIZ,
            acento=C_ACENTO_SEL, es_burbuja=False,
            f_titulo=self.f_medio, f_info=self.f_pequeño
        )

    def _dibujar_panel_teoria(self):
        """Panel inferior con información teórica de complejidad."""
        y_base = Y_VIZ + ALTO_VIZ + 130
        ancho_panel = ANCHO_VIZ * 3 + MARGEN * 2 + 24
        rect   = pygame.Rect(X_INS - 12, y_base, ancho_panel, ALTO - y_base - 8)
        pygame.draw.rect(self.sup, C_PANEL, rect, border_radius=8)
        pygame.draw.rect(self.sup, C_PANEL_BORDE, rect, 1, border_radius=8)

        lbl = self.f_pequeño.render(
            "COMPLEJIDAD ALGORÍTMICA", True, (130, 135, 160))
        self.sup.blit(lbl, (X_INS, y_base + 7))

        entradas = [
            (C_ACENTO_INS, "Insertion Sort →",
             "O(n²) peor caso  ·  O(n) mejor caso (lista casi ordenada)"
             "  ·  Estable  ·  In-place  ·  Ideal para N pequeño o datos incrementales."),
            (C_ACENTO_BUB, "Bubble Sort    →",
             "O(n²) prácticamente siempre  ·  Más intercambios = más escrituras"
             "  ·  Estable  ·  In-place  ·  Fácil de implementar, rara vez eficiente."),
            (C_ACENTO_SEL, "Selection Sort →",
             "O(n²) siempre  ·  Mínimo de intercambios (n-1)  ·  Inestable"
             "  ·  In-place  ·  Útil cuando el coste de escritura es muy alto."),
        ]
        for i, (color, etq, desc) in enumerate(entradas):
            y_l = y_base + 26 + i * 22
            self.sup.blit(self.f_pequeño.render(etq, True, color), (X_INS, y_l))
            self.sup.blit(self.f_pequeño.render(desc, True, C_TEXTO),
                          (X_INS + 158, y_l))

    def _aplicar_valores_custom(self):
        """Parsea el campo de texto y aplica los valores a los tres algoritmos."""
        self._error_input = ""
        texto = self.entrada_vals.texto.strip()
        if not texto:
            return
        partes = texto.replace(",", " ").split()
        try:
            nums = [int(p) for p in partes if p]
        except ValueError:
            self._error_input = "Error: solo se permiten enteros."
            return
        nums = [max(1, abs(n)) for n in nums][:60]
        if len(nums) < 2:
            self._error_input = "Error: ingresa al menos 2 valores."
            return
        self._reiniciar_estado()
        self.datos_ins = nums[:]
        self.datos_bub = nums[:]
        self.datos_sel = nums[:]
        self._n_custom = len(nums)

    def _paso_manual_ins(self):
        """Avanza el Insertion Sort un único paso (modo manual en pestaña 2)."""
        if self.estado_ins == Estado.ESPERANDO:
            self.gen_ins    = gen_insertion_sort(self.datos_ins, self.stats_ins)
            self.estado_ins = Estado.ORDENANDO
            self.frame_ins  = 0
        if self.estado_ins == Estado.ORDENANDO:
            self.info_ins, self.estado_ins = self._avanzar(
                self.gen_ins, self.info_ins, self.estado_ins)

    def _dibujar_tabs(self):
        """Dibuja los botones de pestañas sobre el área de visualización."""
        definiciones = [
            (self._rect_tab0, "  Comparativa  (1)",   0),
            (self._rect_tab1, "  Insercion Detallada  (2)", 1),
        ]
        for rect, texto, idx in definiciones:
            activa = (idx == self.pestaña)
            color_fondo  = (50, 55, 95)    if activa else C_BTN
            color_borde  = C_ACENTO_INS    if activa else C_PANEL_BORDE
            color_texto  = C_ACENTO_INS    if activa else C_BTN_TXT
            pygame.draw.rect(self.sup, color_fondo, rect, border_radius=7)
            pygame.draw.rect(self.sup, color_borde, rect, 2, border_radius=7)
            lbl = self.f_pequeño.render(texto, True, color_texto)
            self.sup.blit(lbl, lbl.get_rect(center=rect.center))

    def _dibujar_pestaña_insercion(self):
        """Vista detallada de Insertion Sort: panel amplio con valores en cada barra."""
        ancho_full = ANCHO_VIZ * 3 + MARGEN * 2
        alto_det   = ALTO_VIZ + 60   # más alto para mayor claridad visual

        dibujar_panel_algoritmo(
            sup=self.sup,
            titulo="  INSERTION SORT — Vista Detallada",
            datos=self.datos_ins, info=self.info_ins,
            stats=self.stats_ins, estado=self.estado_ins,
            x=X_INS, y=Y_VIZ,
            ancho=ancho_full, alto=alto_det,
            acento=C_ACENTO_INS, es_burbuja=False,
            f_titulo=self.f_medio, f_info=self.f_pequeño,
            mostrar_valores=True, f_valor=self.f_mini
        )

        # Panel de teoría reducido (solo Insertion Sort)
        y_base = Y_VIZ + alto_det + 130
        ancho_panel = ancho_full + 24
        rect = pygame.Rect(X_INS - 12, y_base, ancho_panel, ALTO - y_base - 8)
        pygame.draw.rect(self.sup, C_PANEL, rect, border_radius=8)
        pygame.draw.rect(self.sup, C_PANEL_BORDE, rect, 1, border_radius=8)
        self.sup.blit(
            self.f_pequeño.render("COMPLEJIDAD ALGORÍTMICA", True, (130, 135, 160)),
            (X_INS, y_base + 7))
        desc = ("O(n²) peor caso  ·  O(n) mejor caso (lista casi ordenada)"
                "  ·  Estable  ·  In-place  ·  Ideal para N pequeño o datos incrementales.")
        self.sup.blit(self.f_pequeño.render("Insertion Sort →", True, C_ACENTO_INS),
                      (X_INS, y_base + 26))
        self.sup.blit(self.f_pequeño.render(desc, True, C_TEXTO),
                      (X_INS + 158, y_base + 26))

    # ── Loop ──────────────────────────────────────────────────────────

    def ejecutar(self):
        """Punto de entrada del bucle principal."""
        while True:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)


# ══════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()