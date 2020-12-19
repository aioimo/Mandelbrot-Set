from PIL import Image
import colorsys
import math
import os

width = 100

center_x = -0.65
center_y = 0
x_range = 3.4
aspect_ratio = 4/3

height = round(width / aspect_ratio)
y_range = x_range / aspect_ratio
min_x = center_x - x_range / 2
max_y = center_y + y_range / 2

precision = 500

img = Image.new('RGB', (width, height), color = 'black')
pixels = img.load()

## Coloring options
EXP = 0.3
CONST = 0.50
SCALE = 2.2

def fileName(precision, exp, const, scale):
    return f"output_{precision}_{exp}_{const}_{scale}.png"

def logColor(distance):
    color = -1 * math.log(distance, 50)
    rgb = colorsys.hsv_to_rgb(0.4 + 0.9 * color,0.8,0.9)
    return tuple(round(i * 255) for i in rgb)

def powerColor(distance, exp, const, scale):
    color = distance**exp
    rgb = colorsys.hsv_to_rgb(const + scale * color,1 - 0.6 * color,0.9)
    return tuple(round(i * 255) for i in rgb)

def z_squared(x,y):
    return x*x - y*y, 2 * x * y

def plus(a,b, x,y):
    return a + x, b + y

for row in range(height):
    for col in range(width):
        x = min_x + col * x_range / width
        y = max_y - row * y_range / height
        x_0 = x
        y_0 = y
        for i in range(precision + 1):
            a, b = z_squared(x,y)
            x, y = plus(a,b, x_0, y_0)

            if x*x + y*y > 4:
                break
        if i < precision:
            distance = (i + 1) / (precision + 1)
            rgb = powerColor(distance, EXP, CONST, SCALE)
            pixels[col,row] = rgb
        index = row * width + col + 1
        print("{} / {}, {}%".format(index, width * height, round(index / width / height * 100 * 10) / 10))

filename = fileName(precision, EXP, CONST, SCALE)

img.save(filename)
os.system(f"open {filename}")
