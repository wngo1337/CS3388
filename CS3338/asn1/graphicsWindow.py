from PIL import Image

#   Student number:
#   Code for the drawLine method written by William Ngo

class graphicsWindow:

    def __init__(self,width=640,height=480):
        self.__mode = 'RGB'
        self.__width = width
        self.__height = height
        self.__canvas = Image.new(self.__mode,(self.__width,self.__height))
        self.__image = self.__canvas.load()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def drawPixel(self,pixel,color):
        self.__image[pixel[0],pixel[1]] = color

    def saveImage(self,fileName):
        self.__canvas.save(fileName)

    def drawLine(self, p1, p2, colour): #   takes two points and a line colour, and then draws a line between the two points choosing the correct Bresenham line case

        """I guess I probably could have set this up in a way so that there wasn't so much repeated code, but I spent too long on
        figuring out understanding how to do the cases, so I didn't have time :( """

        x1, y1 = p1
        x2, y2 = p2

        deltaX = round(x2 - x1)     #   we shouldn't get any decimals, but round everything off to be safe
        deltaY = round(y2 - y1)

        #   originally had a slope calculation here, but it gave me an error when the change in x was zero :(

        if deltaX >= 0 and deltaY >= 0 and deltaY <= deltaX:

            """Line lies in octant 0.
            This is our standard Bresenham case, so no need for switching things.
            Also, I don't know why these comments appear like regular text instead of grey."""

            print("CASE 0: Line with positive slope between 0 and 1")
            self.drawPixel((x1, y1), colour)    #   draw the initial pixel, and then start Bresenham
            for i in range(x1, x2, 1):

                """Initially I used x2 + 1 for the loop condition because the range function doesn't include the end value,
                but it didn't seem to make a difference so I changed it back"""

                if i == x1:
                    currentPixel = 2 * deltaY - deltaX
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * deltaY
                    else:
                        currentPixel = currentPixel + 2 * deltaY - 2 * deltaX
                        y1 = y1 + 1

                    x1 = x1 + 1     #   we increment the major axis every iteration
                    self.drawPixel((x1, y1), colour)

        elif deltaX >= 0 and deltaY >= 0 and deltaY > deltaX: #   line lies in octant 1 since slope > 1

            """Line lies in octant 1 with a large positive slope.
            We need to travel along the longer y-axis, so swap x, y, deltaX, and deltaY"""

            print("CASE 1: Line with positive slope greater than 1.")
            self.drawPixel((x1, y1), colour)
            for i in range(y1, y2, 1):
                if i == y1:
                    currentPixel = 2 * deltaX - deltaY
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * deltaX
                    else:
                        currentPixel = currentPixel + 2 * deltaX - 2 * deltaY
                        x1 = x1 + 1

                    y1 = y1 + 1
                    self.drawPixel((x1, y1), colour)

        elif deltaX <= 0 and deltaY >= 0 and abs(deltaY) > abs(deltaX): #   line lies in octant 2 since deltaX is neg and magnitude of slope > 1

            """Line lies in octant 2 with a large negative slope. 
            Need to travel along the y-axis, but since x1 > x2, we decrement along the x-axis now.
            This means swapping x, y, deltaX, and deltaY, and lastly change the sign when working with deltaX."""

            print("CASE 2: Line with negative slope greater than 1, x1 > x2")
            self.drawPixel((x1, y1), colour)
            for i in range(y1, y2, 1):
                if i == y1:
                    currentPixel = 2 * (-deltaX) - deltaY
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * (-deltaX)
                    else:
                        currentPixel = currentPixel + 2 * (-deltaX) - 2 * deltaY
                        x1 = x1 - 1

                    y1 = y1 + 1
                    self.drawPixel((x1, y1), colour)

        elif deltaX <= 0 and deltaY >= 0 and abs(deltaY) <= abs(deltaX): #   Line lies in octant 3

            """Line lies in octant 3 with a shallow negative slope.
            Need to travel along the x-axis, but x1 > x2 so we have to decrement it now.
            We also have to change the sign when we are working with deltaX then."""

            print("CASE 3: Line with negative slope between 0 and 1, x1 > x2")
            self.drawPixel((x1, y1), colour)
            for i in range(x1, x2, -1):
                if i == x1:
                    currentPixel = 2 * deltaY - (-deltaX)
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * deltaY
                    else:
                        currentPixel = currentPixel + 2 * deltaY - 2 * (-deltaX)
                        y1 = y1 + 1

                    x1 = x1 - 1
                    self.drawPixel((x1, y1), colour)

        elif deltaX < 0 and deltaY < 0 and abs(deltaY) <= abs(deltaX): #   Line lies in octant 4

            """Line lies in octant 4 with a shallow positive slope, so symmetric to case 0. We travel along the x-axis.
            However, this time y1 > y2 and x1 > x2, so we have to change the signs when working with deltaY and deltaX."""

            print("CASE 4: Line with positive slope between 0 and 1, x1 > x2")
            self.drawPixel((x1, y1), colour)
            for i in range(x1, x2, -1):
                if i == x1:
                    currentPixel = 2 * (-deltaY) + deltaX
                else:
                    if currentPixel < 0:    #   case 1: line lies in quadrant 1
                        currentPixel = currentPixel + 2 * (-deltaY)
                    else:
                        currentPixel = currentPixel + 2 * (-deltaY) - 2 * (-deltaX)
                        y1 = y1 - 1

                    x1 = x1 - 1
                    self.drawPixel((x1, y1), colour)

        elif deltaX < 0 and deltaY < 0 and abs(deltaY) > abs(deltaX):  #   line lies in octant 5

            """Line lies in octant 5 with a steep positive slope, so symmetric to octant 1. We travel along the y-axis.
            We need to swap deltaY with deltaX.
            However, y1 > y2 and x1 > x2 so we have to change the signs when working with deltaY and deltaX."""

            print("CASE 5: Line with positive slope greater than 1, x1 > x2")
            self.drawPixel((x1, y1), colour)
            for i in range(y1, y2, -1):
                if i == y1:
                    currentPixel = 2 * (-deltaX) - (-deltaY)
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * (-deltaX)
                    else:
                        currentPixel = currentPixel + 2 * (-deltaX) - 2 * (-deltaY)
                        x1 = x1 - 1

                    y1 = y1 - 1
                    self.drawPixel((x1, y1), colour)

        elif deltaX >= 0 and deltaY < 0 and abs(deltaY) > abs(deltaX):  #   Line lies in octant 6

            """Line is in octant 6 with a steep negative slope. We travel along the y-axis.
            So we need to swap deltaY and deltaX.
            However, y1 > y2 so we have to change the sign when working with deltaY."""

            print("CASE 6: Line with negative slope greater than 1, y1 > y2")
            self.drawPixel((x1, y1), colour)
            for i in range(y1, y2, -1):
                if i == y1:
                    currentPixel = 2 * deltaX - (-deltaY)
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * deltaX
                    else:
                        currentPixel = currentPixel + 2 * deltaX - 2 * (-deltaY)
                        x1 = x1 + 1

                    y1 = y1 - 1
                    self.drawPixel((x1, y1), colour)

        else:   #   If line doesn't lie in the first 7 quadrants, it has to be here in octant 7
                #   is equivalent to my original line: elif deltaX >= 0 and deltaY < 0 and abs(deltaY) <= abs(deltaX):

            """Lastly, the line lies in octant 7 with a shallow negative slope. We travel along the x-axis.
            However, y1 > y2, so we have to change the sign when working with deltaY."""

            print("CASE 7: Line with negative slope between 0 and 1, y1 > y2")
            self.drawPixel((x1, y1), colour)
            for i in range(x1, x2, 1):
                if i == x1:
                    currentPixel = 2 * (-deltaY) - deltaX
                else:
                    if currentPixel < 0:
                        currentPixel = currentPixel + 2 * (-deltaY)
                    else:
                        currentPixel = currentPixel + 2 * (-deltaY) - 2 * deltaX
                        y1 = y1 - 1

                    x1 = x1 + 1
                    self.drawPixel((x1, y1), colour)

