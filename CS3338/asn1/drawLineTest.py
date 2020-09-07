from math import *
from graphicsWindow import graphicsWindow

window = graphicsWindow(512,512)
color = (255,255,255)

x1 = 100
y1 = 100

x2 = 300
y2 = 200

window.drawLine((x1, y1), (x2, y2), color)
window.saveImage("PleaseFkinWork.png")
