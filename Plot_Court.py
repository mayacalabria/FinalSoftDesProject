import pygame
import sys
import matplotlib.path
import SVG_Parsing
import csv


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (75, 75, 255)
GREEN = (75, 255, 75)
RED = (255, 50, 50)
GRAY = (127, 127, 127)
LIGHT_GRAY = (191, 191, 191)
zone=['Three-point line']
width, height = 800,800

pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(WHITE)


def point_in_polygon(pt, polygon):
    """Returns True iff `pt` is inside `polygon`.
    `polygon` is a list of tuples `(x, y)`."""

    return matplotlib.path.Path(polygon).contains_point(pt)

for polygon in SVG_Parsing.zones[zone]:
    # `polygon` points are tuples `(float, float)`. PyGame requires `(int, int)`.
    points = [(int(x), int(y)) for x, y in polygon]
    # Draw the interior
    pygame.draw.polygon(screen, BLACK, points, 1)

pygame.display.flip()
