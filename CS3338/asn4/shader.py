class shader:

    def __shadowed(self,object,I,S,objectList):

        """This is a helper method for the shader that takes a particular object, an intersection point, a light source vector, and a
        list of objects composing the scene, as parameters. It returns true if the object-ray intersection point also intersects
        with another object from the scene. Otherwise, it returns false."""

        EPSILON = 0.001
        M = object.getT()
        newI = M * (I + S.scalarMultiply(EPSILON))  # transforming the intersection point to world coordinates
        newS = M * S                                # transforming the light source vector to world coordinates

        for nextObject in objectList:
            inverseM = nextObject.getT().inverse()
            newerI = inverseM * newI                # ran into a problem here because I was reusing newI for each calculation...
            newerS = (inverseM * newS).normalize()  # same for newS

            possibleIntersection = object.intersection(newerI, newerS)  #   check for intersection between scene object and parameter object

            if possibleIntersection != -1.0:    #   object is shadowed by a scene object
                return True

        return False    #   else object is not shadowed, so shade normally

    def __init__(self,intersection,direction,camera,objectList,light):

        """This method takes an intersection tuple, a ray vector, a cameraMatrix, a list of objects, and a light source as parameters.
        It uses its parameters and the __shadowed helper method to determine how to color the pixel in question. """

        k, t0 = intersection    # k is the index of an object in the object list, t0 is the associated t-value
        object = objectList[k]
        inverseM = object.getT().inverse()
        tS = inverseM * light.getPosition()     # transformed light position in terms of the object in the intersection tuple
        tE = inverseM * camera.getE()           # transformed camera position
        tD = inverseM * direction               # transformed ray

        I = tE + (tD.scalarMultiply(t0))        # intersection point
        S = (tS - I).normalize()                # normalized vector from the intersection point to the transformed light position
        N = object.normalVector(I)              # normal vector to the intersection point

        R = -S + N.scalarMultiply((S.scalarMultiply(2)).dotProduct(N))  # specular reflection vector

        V = (tE - I).normalize()                # vector to the center of projection
        iD = max((N.dotProduct(S)), 0)          # diffuse light intensity
        iS = max((R.dotProduct(V)), 0)          # specular light intensity

        r = object.getReflectance()
        c = object.getColor()
        lI = light.getIntensity()

        isShadowed = self.__shadowed(object, I, S, objectList)  # check to see if object is shadowed by another object

        if not isShadowed:
            f = r[0] + r[1] * iD + r[2] * (iS ** r[3])          # if object is not shadowed, compute the lighting model
                                                                # using reflectance coefficients as per the notes
        else:
            f = r[0]                                            # if object is shadowed, lighting model is just the ambient reflectance coefficient

        originalColor = (c[0] * lI[0], c[1] * lI[1], c[2] * lI[2])

        # now we apply the lighting model to the object's original colors to finish

        self.__color = (int(f * originalColor[0]), int(f * originalColor[1]), int(f * originalColor[2]))

    def getShade(self):
        return self.__color
