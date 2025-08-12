import pygame as pg
import numba
import numpy as np
import math
from decimal import Decimal, getcontext

# ----- Einstellungen -----
größe = breite, höhe = 900, 600
max_farb_iter = 20000
farben = np.zeros((max_farb_iter, 3), dtype=np.uint8)
for i in range(max_farb_iter):
    farben[i] = (
        int((0.5 * math.sin(0.1 * i + 2.094) + 0.5) * 255),
        int((0.5 * math.sin(0.1 * i + 4.188) + 0.5) * 255),
        int((0.5 * math.sin(0.1 * i) + 0.5) * 255)
    )
base_iter = 50
FPS_LIMIT = 60
float_threshold = 1e14

def compute_max_iter(zoom):
    """
    Berechnet die maximale Iterationszahl basierend auf dem Zoom-Level.
    Erhöht Iterationen aggressiver bei extremem Zoom, um Detailverlust zu vermeiden.
    """
    z = max(zoom, 1.0)
    linear = 100 * math.log10(z)
    quadratic = 20 * (math.log10(z) ** 2)
    return int(base_iter + linear + quadratic)

@numba.njit(fastmath=True, parallel=True)
def render_mandel(bild, x1, x2, y1, y2, max_iter):
    w, h = bild.shape[0], bild.shape[1]
    dx = (x2 - x1) / w
    dy = (y2 - y1) / h
    for j in numba.prange(h):
        y0 = y1 + j * dy
        for i in range(w):
            x0 = x1 + i * dx
            x = 0.0; y = 0.0; iteration = 0
            while x*x + y*y <= 4.0 and iteration < max_iter:
                xt = x*x - y*y + x0
                y = 2*x*y + y0; x = xt
                iteration += 1
            if iteration < max_iter:
                log_zn = math.log(x*x + y*y) * 0.5
                nu = math.log(log_zn / math.log(2)) / math.log(2)
                idx = int(iteration + 1 - nu) % farben.shape[0]
            else:
                idx = 0
            bild[i, j] = farben[idx]
    return bild

def render_mandel_decimal(width, height, x1, x2, y1, y2, max_iter, prec):
    getcontext().prec = prec
    dx = (Decimal(x2) - Decimal(x1)) / width
    dy = (Decimal(y2) - Decimal(y1)) / height
    img = np.zeros((width, height, 3), dtype=np.uint8)
    step = 2  # jedes zweite Pixel berechnen
    for j in range(0, height, step):
        y0 = Decimal(y1) + j*dy
        for i in range(0, width, step):
            x0 = Decimal(x1) + i*dx
            x = Decimal(0); y = Decimal(0)
            it = 0
            while x*x + y*y <= 4 and it < max_iter:
                x, y = x*x - y*y + x0, 2*x*y + y0
                it += 1
            color = farben[it % len(farben)] if it < max_iter else (0,0,0)
            img[i:i+step, j:j+step] = color
    return img

pg.init()
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
fraktal = np.zeros((breite, höhe, 3), dtype=np.uint8)

# View-Parameter
x1, x2, y1, y2 = -2.0, 1.0, -1.0, 1.0
zoom = 1.0
needs_redraw = True
verschiebe = False
lx = ly = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit(); raise SystemExit
        if event.type == pg.MOUSEWHEEL:
            scale = 0.8 if event.y > 0 else 1.25
            mx, my = pg.mouse.get_pos()
            cx = x1 + mx/breite*(x2-x1)
            cy = y1 + my/höhe*(y2-y1)
            x1, x2 = cx-(cx-x1)*scale, cx+(x2-cx)*scale
            y1, y2 = cy-(cy-y1)*scale, cy+(y2-cy)*scale
            zoom *= 1/scale; needs_redraw = True
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            verschiebe = True; lx, ly = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            verschiebe = False
        if verschiebe and event.type == pg.MOUSEMOTION:
            mx, my = pg.mouse.get_pos()
            dx = (lx - mx)/breite*(x2-x1)
            dy = (ly - my)/höhe*(y2-y1)
            x1, x2, y1, y2 = x1+dx, x2+dx, y1+dy, y2+dy
            lx, ly = mx, my; needs_redraw = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                base_iter <<= 1; needs_redraw = True
            elif event.key == pg.K_DOWN and base_iter > 10:
                base_iter >>= 1; needs_redraw = True

    if needs_redraw:
        max_iter = compute_max_iter(zoom)
        if zoom < float_threshold:
            fraktal = render_mandel(fraktal, x1, x2, y1, y2, max_iter)
        else:
            prec = min(80, int(30 + math.log10(zoom)*10))
            fraktal = render_mandel_decimal(breite, höhe, x1, x2, y1, y2, max_iter, prec)
        needs_redraw = False

    pg.surfarray.blit_array(fenster, fraktal)
    pg.display.flip()
    clock.tick(FPS_LIMIT)
    pg.display.set_caption(f"FPS={clock.get_fps():.1f} Zoom={zoom:.2f} Iter={max_iter}")
