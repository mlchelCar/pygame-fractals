import sys
import tkinter

import pygame
from numba import njit


@njit()
def val(num, zm):
    var = num*0.00390625/zm
    return var


@njit()
def get_iter_mandelbrot(c, max_iter):
    z, n = 0, 0
    while abs(z) <= 2 and n < max_iter:
        z = z**2 + c
        n += 1
    return n, z


@njit()
def get_iter_burning_ship(c, max_iter):
    z, n = 0, 0
    while abs(z) <= 2 and n < max_iter:
        z = (abs(z.real)+1j*abs(z.imag))**2 + c
        n += 1
    return n, z


@njit()
def get_iter_other(c, max_iter):
    z, n = 0, 0
    while abs(z) <= 2 and n < max_iter:
        z = c**z
        n += 1
    return n, z


@njit()
def color_gray(iter, comp, max_iter):
    color = 255 - int(iter * 255 / max_iter)
    return color, color, color


@njit()
def color_pink(iter, comp, max_iter):
    color_list = [
        (54, 17, 52), (176, 34, 140), (234, 55, 136), (229, 107, 112), (243, 145, 160)]
    if iter < max_iter:
        color = color_list[iter % len(color_list)]
    else:
        color = (0, 0, 0)

    return color


@njit()
def color_blue(iter, comp, max_iter):
    color_list = [
        (66, 30, 15), (25, 7, 26), (9, 1, 47), (4, 4, 73),
        (0, 7, 100), (12, 44, 138), (24, 82, 177), (57, 125, 209),
        (134, 181, 229), (211, 236, 248), (241, 233, 191), (248, 201, 95),
        (255, 170, 0), (204, 128, 0), (153, 87, 0), (106, 52, 3)]
    if iter < max_iter:
        color = color_list[iter % len(color_list)]
    else:
        color = (0, 0, 0)

    return color


def pixels():
    pixels_1 = [i for i in range(int(WIDTH/2), WIDTH+1)]
    pixels_2 = [i for i in range(int(WIDTH/2))]
    pixels_2_reverse = pixels_2.copy()
    pixels_2_reverse.sort(reverse=True)
    pixels_largura = {}

    for i, j in zip(pixels_2, pixels_2_reverse):
        pixels_largura[i] = val(-j, zoom_level)

    pixels_2.pop(0)
    pix2 = {}

    for i, j in zip(pixels_1, pixels_2):
        pix2[i] = val(j, zoom_level)

    for i in pix2:
        pixels_largura[i] = pix2[i]

    for i in pixels_largura:
        pixels_largura[i] = pixels_largura[i] - right + left

    ph1 = [i for i in range(int(HEIGHT/2), HEIGHT+1)]
    ph2 = [i for i in range(int(HEIGHT/2))]
    ph2_reverse = ph2.copy()
    ph2_reverse.sort(reverse=True)
    pixels_altura = {}

    for i, j in zip(ph2, ph2_reverse):
        pixels_altura[i] = complex(0, val(-j, zoom_level))

    ph2.pop(0)
    phx2 = {}

    for i, j in zip(ph1, ph2):
        phx2[i] = complex(0, val(j, zoom_level))

    for i in phx2:
        pixels_altura[i] = phx2[i]

    for i in pixels_altura:
        pixels_altura[i] = pixels_altura[i] - up + down

    return pixels_altura, pixels_largura


def mandelbrot():
    pixels_altura, pixels_largura = pixels()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            try:
                pxH = pixels_altura[i]
                pxW = pixels_largura[j]
            except KeyError:
                continue
            sum = pxH + pxW
            max_iter = 80

            if fractal == 'mandelbrot':
                iter, comp = get_iter_mandelbrot(sum, max_iter)
            elif fractal == 'other':
                iter, comp = get_iter_other(sum, max_iter)
            elif fractal == 'burning_ship':
                iter, comp = get_iter_burning_ship(sum, max_iter)
            else:
                raise Exception('Fractal not identified')

            if color_scheme == 'gray':
                col = color_gray(iter, comp, max_iter)
            elif color_scheme == 'pink':
                col = color_pink(iter, comp, max_iter)
            elif color_scheme == 'blue':
                col = color_blue(iter, comp, max_iter)
            else:
                raise Exception('Color not identified')

            pygame.draw.rect(screen, col, (j, i, 1, 1))
        pygame.display.update()


def main():
    global right, left, up, down, zoom_level, screen, WIDTH, HEIGHT, fractal, color_scheme

    if len(sys.argv) != 3:
        raise Exception(
            '\nUsage: python3 pygame-fractals.py [fractal] [color]\nfractal = mandelbrot/burning_ship/other\ncolor = gray/pink/blue')
    else:
        fractal = sys.argv[1]
        color_scheme = sys.argv[2]

    WIDTH = tkinter.Tk().winfo_screenwidth()  # 1366
    HEIGHT = tkinter.Tk().winfo_screenheight()  # 768

    right = 0
    left = 0
    up = 0j
    down = 0j
    zoom_level = 1

    # initiate the pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # title
    pygame.display.set_caption("Pygame-Fractals")

    mandelbrot()

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                    break
                if ev.key == pygame.K_UP:
                    up += 0.5j/zoom_level
                    mandelbrot()
                if ev.key == pygame.K_DOWN:
                    down += 0.5j/zoom_level
                    mandelbrot()
                if ev.key == pygame.K_LEFT:
                    right += 0.5/zoom_level
                    mandelbrot()
                if ev.key == pygame.K_RIGHT:
                    left += 0.5/zoom_level
                    mandelbrot()
                if ev.key == pygame.K_LSHIFT:
                    zoom_level *= 2.0
                    mandelbrot()
                elif ev.key == pygame.K_LCTRL:
                    zoom_level /= 2.0
                    mandelbrot()
                elif ev.key == pygame.K_SPACE:
                    mandelbrot()


if __name__ == '__main__':
    main()
