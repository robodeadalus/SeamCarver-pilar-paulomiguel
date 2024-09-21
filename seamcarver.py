#!/usr/bin/env python3

from picture import Picture
import math

class SeamCarver(Picture):
    
    # --- part 1: energy calculation ---
    
    def energy(self, i: int, j: int) -> float:
        """
        Return the energy of pixel at column i and row j
        """
        
        width = self.width();
        height = self.height();
        
        if not ((0 <= i < width) and (0 <= j < height)):
            raise IndexError("Pixel coordinates out of bounds")

        XGradient = self.calculateXGradient(i, j)
        YGradient = self.calculateYGradient(i, j)
        
        return math.sqrt(XGradient + YGradient)

    def calculateXGradient(self, i, j):
        """
        Return the square of the x-gradient
        """
        
        width = self.width()
        height = self.height()
        
        if not ((0 <= i < width) and (0 <= j < height)):
            raise IndexError("Pixel coordinates out of bounds")

        if (i - 1) < 0:
            previousPixel = self[width - 1, j]
        else:
            previousPixel = self[i - 1, j]
        if (i + 1) >= width:
            nextPixel = self[0, j]
        else:
            nextPixel = self[i + 1, j]
            
        redX = abs(nextPixel[0] - previousPixel[0])
        greenX = abs(nextPixel[1] - previousPixel[1])
        blueX = abs(nextPixel[2] - previousPixel[2])
        
        return redX**2 + greenX**2 + blueX**2

    def calculateYGradient(self, i, j):
        """
        Return the square of the y-gradient
        """
        
        width = self.width()
        height = self.height()
        
        if not ((0 <= i < width) and (0 <= j < height)):
            raise IndexError("Pixel coordinates out of bounds")

        if (j - 1) < 0:
            previousPixel = self[i, height - 1]
        else:
            previousPixel = self[i, j - 1]
        if (j + 1) >= height:
            nextPixel = self[i, 0]
        else:
            nextPixel = self[i, j + 1]
            
        redY = abs(nextPixel[0] - previousPixel[0])
        greenY = abs(nextPixel[1] - previousPixel[1])
        blueY = abs(nextPixel[2] - previousPixel[2])
        
        return redY**2 + greenY**2 + blueY**2
    
    # --- part 2: seam identification ---
    
    def find_vertical_seam(self) -> list[int]:
        """
        Return a sequence of indices representing the lowest-energy
        vertical seam
        """

        column = 0
        row = 0
        width = self.width()
        height = self.height()

        # used https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array

        total_energy = [([0] * width) for i in range(height)]
        prev = [([None] * width) for i in range(height)]

        # go through each row
        # store the total energy and previous pixel per pixel

        while row < height:
            while column < width:
                # in first row
                if row == 0:
                    total_energy[row][column] = self.energy(column, row)
                # in first column
                elif column == 0:
                    total_energy[row][column] = self.energy(column, row) + min(total_energy[row - 1][column], total_energy[row - 1][column + 1])
                    if min(total_energy[row - 1][column], total_energy[row - 1][column + 1]) == total_energy[row - 1][column]:
                        prev[row][column] = column
                    else:
                        prev[row][column] = column + 1
                # in last column
                elif column == (width - 1):
                    total_energy[row][column] = self.energy(column, row) + min(total_energy[row - 1][column - 1], total_energy[row - 1][column])
                    if (min(total_energy[row - 1][column - 1], total_energy[row - 1][column]) == total_energy[row - 1][column]):
                        prev[row][column] = column
                    else:
                        prev[row][column] = column - 1
                # the rest
                else:
                    total_energy[row][column] = self.energy(column, row) + min(total_energy[row - 1][column - 1], total_energy[row - 1][column], total_energy[row - 1][column + 1])
                    if (min(total_energy[row - 1][column - 1], total_energy[row - 1][column], total_energy[row - 1][column + 1]) == total_energy[row - 1][column]):
                        prev[row][column] = column
                    elif (min(total_energy[row - 1][column - 1], total_energy[row - 1][column], total_energy[row - 1][column + 1]) == total_energy[row - 1][column - 1]):
                        prev[row][column] = column - 1
                    else:
                        prev[row][column] = column + 1
                column += 1
            column = 0
            row += 1

        # find the minimum energy in the last row
        # backtrack through minimals using prev
        # create the vertical seam as you backtrack

        vertical_seam = []
        row = height - 1

        vertical_seam.insert(0, total_energy[height - 1].index(min(total_energy[height - 1])))
        column = vertical_seam[0]

        while row > 0:
            vertical_seam.insert(0, prev[row][column])
            column = vertical_seam[0]
            row -= 1
        
        return vertical_seam

    def find_horizontal_seam(self) -> list[int]:
        """
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        """

        og_width = self.width()
        og_height = self.height()
        new_width = self.height()
        new_height = self.width()

        original_image = {}
        transposed_image = {}

        # save old image

        column = 0
        row = 0

        while row < og_height:
            while column < og_width:
                original_image[column, row] = self[column, row]
                column += 1
            column = 0
            row += 1

        # create transposed image

        column = 0
        row = 0

        while row < new_height:
            while column < new_width:
                transposed_image[column, row] = self[row, column]
                column += 1
            column = 0
            row += 1
            
        # set image to transposed image

        self.clear()

        column = 0
        row = 0

        self._width = new_width
        self._height = new_height

        while row < new_height:
            while column < new_width:
                self[column, row] = transposed_image[column, row]
                column += 1
            column = 0
            row += 1

        # run find vertical seam on image that is now transposed

        horizontal_seam = []
        horizontal_seam = self.find_vertical_seam()

        # revert image to original

        self.clear()

        column = 0
        row = 0

        self._width = og_width
        self._height = og_height

        while row < og_height:
            while column < og_width:
                self[column, row] = original_image[column, row]
                column += 1
            column = 0
            row += 1

        return horizontal_seam
    
    # --- part 3: seam removal ---

    def remove_vertical_seam(self, seam: list[int]):
        """
        Remove a vertical seam from the picture
        """
        
        width = self.width()
        height = self.height()
        
        if width <= 1:
            raise SeamError
        if len(seam) != height:
            raise SeamError
        for i in range(len(seam) - 1):
            if abs(seam[i] - seam[i + 1]) > 1:
                raise SeamError

        for row in range(len(seam)):
            for column in range(seam[row], width - 1):
                self[column, row] = self[column + 1, row]
            del self[width - 1, row]

        self._width -= 1

    def remove_horizontal_seam(self, seam: list[int]):
        """
        Remove a horizontal seam from the picture
        """

        og_width = self.width()
        og_height = self.height()
        new_width = self.height()
        new_height = self.width()

        original_image = {}
        transposed_image = {}

        # create transposed image

        column = 0
        row = 0

        while row < new_height:
            while column < new_width:
                transposed_image[column, row] = self[row, column]
                column += 1
            column = 0
            row += 1
            
        # set image to transposed image

        self.clear()

        column = 0
        row = 0

        self._width = new_width
        self._height = new_height

        while row < new_height:
            while column < new_width:
                self[column, row] = transposed_image[column, row]
                column += 1
            column = 0
            row += 1
            
        # run remove vertical seam on image that is now transposed
        
        self.remove_vertical_seam(seam)
        
        # undo transpose

        column = 0
        row = 0
        
        og_height -= 1 # new height

        while row < og_height:
            while column < og_width:
                original_image[column, row] = self[row, column]
                column += 1
            column = 0
            row += 1

        # revert image to original

        self.clear()

        column = 0
        row = 0

        self._height = og_height
        self._width = og_width

        while row < og_height:
            while column < og_width:
                self[column, row] = original_image[column, row]
                column += 1
            column = 0
            row += 1

class SeamError(Exception):
    pass