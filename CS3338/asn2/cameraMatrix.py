from math import *
import numpy as np
from matrix import matrix

#   Student Name: William Ngo
#   Student Number: 250917380

class cameraMatrix:

    def __init__(self,UP,E,G,nearPlane=10.0,farPlane=50.0,width=640,height=480,theta=90.0):
        __Mp = self.__setMp(nearPlane,farPlane)
        __T1 = self.__setT1(nearPlane,theta,width/height)
        __S1 = self.__setS1(nearPlane,theta,width/height)
        __T2 = self.__setT2()
        __S2 = self.__setS2(width,height)
        __W2 = self.__setW2(height)

        self.__UP = UP.normalize()
        self.__N = (E - G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).transpose().crossProduct(self.__N.transpose()).normalize().transpose()
        self.__V = self.__N.transpose().crossProduct(self.__U.transpose()).transpose()
        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,E)
        self.__C = __W2*__S2*__T2*__S1*__T1*__Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):

        #   so the U, V, N we have here are already normalized and everything

        #   getting rid of the the extra row in e and transposing for easy calculation

        modifiedE = E.removeRow(3).transpose()

        #   apparently Python still sees the below dot products as matrices, so I need to get their actual values

        eU = -modifiedE * U
        eV = -modifiedE * V
        eN = -modifiedE * N

        eUValue = eU.get(0, 0)
        eVValue = eV.get(0, 0)
        eNValue = eN.get(0, 0)

        #   really annoying because I couldn't figure out that the np.zeros method needs to be passed a position,
        #   thus requiring an extra pair of brackets...

        newMv = matrix(np.zeros((4,4)))

        #   CAN'T PUT U, V, N IN DIRECTLY, so one by one...

        newMv.set(0, 0, U.get(0, 0))
        newMv.set(0, 1, U.get(1, 0))
        newMv.set(0, 2, U.get(2, 0))
        newMv.set(0, 3, eUValue)

        newMv.set(1, 0, V.get(0, 0))
        newMv.set(1, 1, V.get(1, 0))
        newMv.set(1, 2, V.get(2, 0))
        newMv.set(1, 3, eUValue)

        newMv.set(2, 0, N.get(0, 0))
        newMv.set(2, 1, N.get(1, 0))
        newMv.set(2, 2, N.get(2, 0))
        newMv.set(2, 3, eNValue)

        newMv.set(3, 3, 1)

        self.__Mv = newMv

        return self.__Mv

    def __setMp(self,nearPlane,farPlane):

        # Oookay so it seems like we only need the matrix part of what's in the notes and not the multiplication with a point

        b = -2 * (farPlane * nearPlane) / (farPlane - nearPlane)
        a = -(farPlane + nearPlane)/(farPlane - nearPlane)

        newMp = matrix(np.zeros((4,4)))
        newMp.set(0, 0, nearPlane)
        newMp.set(1, 1, nearPlane)
        newMp.set(2, 2, a)
        newMp.set(2, 3, b)
        newMp.set(3, 2, -1)

        self.__Mp = newMp
   
        return self.__Mp

    def __setT1(self,nearPlane,theta,aspect):

        # order here is important so we don't get reference errors...
        # call them temp variables so I don't confuse them with the matrix names

        tempT = nearPlane * tan(pi/180 * theta/2)
        tempB = -tempT
        tempR = aspect * tempT
        tempL = -tempR

        newT1 = matrix(np.identity((4)))
        newT1.set(0, 3, -(tempR + tempL)/2)
        newT1.set(1, 3, -(tempT + tempB)/2)

        self.__T1 = newT1

        return self.__T1

    def __setS1(self,nearPlane,theta,aspect):

        #   copy-paste of above calculations...

        tempT = nearPlane * tan(pi/180 * theta/2)
        tempB = -tempT
        tempR = aspect * tempT
        tempL = -tempR

        newS1 = matrix(np.identity((4)))
        newS1.set(0, 0, 2/(tempR - tempL))
        newS1.set(1, 1, 2/(tempT - tempB))

        self.__S1 = newS1

        return self.__S1

    def __setT2(self):

        #   computed directly from note definition

        newT2 = matrix(np.identity((4)))

        newT2.set(0, 3, 1)
        newT2.set(1, 3, 1)

        self.__T2 = newT2

        return self.__T2

    def __setS2(self,width,height):

        #   computed directly from note definition

        newS2 = matrix(np.identity((4)))
        newS2.set(0, 0, width/2)
        newS2.set(1, 1, height/2)

        self.__S2 = newS2

        return self.__S2

    def __setW2(self,height):

        newW2 = matrix(np.identity((4)))
        newW2.set(1, 1, -1)
        newW2.set(1, 3, height)

        self.__W2 = newW2
 
        return self.__W2

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M
