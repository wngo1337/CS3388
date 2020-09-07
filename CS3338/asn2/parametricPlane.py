from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricPlane(parametricObject):

    def __init__(self,T=matrix(np.identity(4)),height = 1.0,width = 1.0,color=(0,0,0),reflectance=(0.0,0.0,0.0),uRange=(0.0,0.0),vRange=(0.0,0.0),uvDelta=(0.0,0.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__width = width
        self.__height = height

        #   Modifying from the sphere example, get rid of radius and introduce width and height, as per the notes

    def getPoint(self, u, v):
        __P = matrix(np.ones((4, 1)))
        __P.set(0, 0, self.__width * u)
        __P.set(1, 0, self.__height * v)
        __P.set(2, 0, 0)
        return __P

    def setLength(self, length):
        self.__length = length

    def setWidth(self, width):
        self.__width = width

    def getLength(self):
        return self.__length

    def getWidth(self):
        return self.__width


