from math import *
from graphicsWindow import graphicsWindow

window = graphicsWindow(512,512)

t = 0.0
dt = 2.0*pi/200.0
color = (20,200,50)
i = 150
j = 150
k = 150

while t < 2.0*pi:
    i = (i + 20) % 255
    j = (j + 40) % 255
    k = (k + 60) % 255
    color = (i, j, k)
    x1 = 256 + int(100.0*(1.5*cos(t) - cos(13.0*t)))
    y1 = 256 + int(100.0*(1.5*sin(t) - sin(13.0*t)))
    t += dt
    x2 = 256 + int(100.0*(1.5*cos(t) - cos(13.0*t)))
    y2 = 256 + int(100.0*(1.5*sin(t) - sin(13.0*t)))
    window.drawLine((x1,y1),(x2,y2),color)

window.saveImage("testImage.png")
