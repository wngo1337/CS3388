import operator
from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):
        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):
        Mv = matrix(np.identity(4))
        Mv.set(0,0,U.get(0,0))
        Mv.set(0,1,U.get(1,0))
        Mv.set(0,2,U.get(2,0))
        Mv.set(0,3,-E.removeRow(3).dotProduct(U))

        Mv.set(1,0,V.get(0,0))
        Mv.set(1,1,V.get(1,0))
        Mv.set(1,2,V.get(2,0))
        Mv.set(1,3,-E.removeRow(3).dotProduct(V))

        Mv.set(2,0,N.get(0,0))
        Mv.set(2,1,N.get(1,0))
        Mv.set(2,2,N.get(2,0))
        Mv.set(2,3,-E.removeRow(3).dotProduct(N))
        return Mv

    def __setMp(self,nearPlane,farPlane):
        Mp = matrix(np.identity(4))
        Mp.set(0,0,nearPlane)
        Mp.set(1,1,nearPlane)
        Mp.set(2,2,-(farPlane+nearPlane)/(farPlane-nearPlane))
        Mp.set(2,3,-2.0*(farPlane*nearPlane)/(farPlane-nearPlane))
        Mp.set(3,2,-1.0)
        Mp.set(3,3,0.0)
        return Mp

    def __setT1(self,nearPlane,theta,aspect):
        top = nearPlane*tan(pi/180.0*theta/2.0)
        right = aspect*top
        bottom = -top
        left = -right
        T1 = matrix(np.identity(4))
        T1.set(0,3,-(right+left)/2.0)
        T1.set(1,3,-(top+bottom)/2.0)
        return T1

    def __setS1(self,nearPlane,theta,aspect):
        top = nearPlane*tan(pi/180.0*theta/2.0)
        right = aspect*top
        bottom = -top
        left = -right
        S1 = matrix(np.identity(4))
        S1.set(0,0,2.0/(right-left))
        S1.set(1,1,2.0/(top-bottom))
        return S1

    def __setT2(self):
        T2 = matrix(np.identity(4))
        T2.set(0,3,1.0)
        T2.set(1,3,1.0)
        return T2

    def __setS2(self,width,height):
        S2 = matrix(np.identity(4))
        S2.set(0,0,width/2.0)
        S2.set(1,1,height/2.0)
        return S2

    def __setW2(self,height):
        W2 = matrix(np.identity(4))
        W2.set(1,1,-1.0)
        W2.set(1,3,height)
        return W2

    def getRay(self,window,i,j):
        a = -self.__np
        b = self.__npWidth*(2.0*i/window.getWidth() - 1.0)
        c = self.__npHeight*(2.0*(window.getHeight() - (j+1))/window.getHeight() - 1.0)
        return (self.__N.scalarMultiply(a) + self.__U.scalarMultiply(b) + self.__V.scalarMultiply(c)).insertRow(3,0.0)

    def minimumIntersection(self,direction,objectList):
        intersectionList = []

        """this function takes a ray vector and a list of objects in the scene respectively as its parameters, direction and objectList.
        It returns a sorted list of tuples, in which each tuple consists of an object's index in the list, and the minimum t-value
        at which the ray intersects it, if at all."""

        counter = 0     # counts the object's position in the object list since we iterate by object

        for object in objectList:
            inverseM = object.getT().inverse()  # this is M inverse

            transformedCamera = inverseM * self.getE()   # this is Te
            transformedRay = inverseM * direction   # this is Td

            minimumIntersection = object.intersection(transformedCamera, transformedRay)    # this is t0

            # above gives a potential intersection, so we just check if it is equal to -1 or not. If not, intersection exists

            if minimumIntersection != -1.0:
                intersectionList.append((counter, minimumIntersection))     # add the intersection tuple to the list

            counter += 1    # move to the next object in the list

        # after everything is added, sort the list

        # selection sort is probably not great for large lists like this, but easy to implement lol...
        for i in range(len(intersectionList)):
            minIndex = i
            for j in range(i + 1, len(intersectionList)):
                if intersectionList[j][1] < intersectionList[minIndex][1]:
                    minIndex = j

            tempElement = intersectionList[i]
            intersectionList[i] = intersectionList[minIndex]
            intersectionList[minIndex] = tempElement

        return intersectionList

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth
