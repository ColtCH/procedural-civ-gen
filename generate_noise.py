import os
import random

'''
---------------------------------------------------------------------------
info:   Clamps an int value to be between 0 and 99.
pre:    None
post:   None
return: Value between 0 and 99.
---------------------------------------------------------------------------
'''
def Clamp(Value):
    if Value < 0:
        Value = 0
    elif Value >= 100:
        Value = 100
    return Value
'''
-------------------------------------------------------------------------------
Create a class Noise that handles the generation of a noise plate.
Defines:
    Pass
    Smooth
    Swirl
-------------------------------------------------------------------------------
'''
class Noise:
    '''
    ---------------------------------------------------------------------------
    info:   Initializes Noise object with height and width.
    pre:    Height != 0 && Width != 0
    post:   self.Plate will be initialized to double array of size height and 
            width.
    return: None
    ---------------------------------------------------------------------------
    '''
    def __init__(self, Height, Width):
        self.Height = Height
        self.Width  = Width
        self.Plate  = [[0 for x in range(self.Width)] 
                          for y in range(self.Height)] 
        self.D_Step = 20
        self.D_Pass = 10
        self.D_Nuke = 45
    '''
    ---------------------------------------------------------------------------
    info:   Returns the noise plate.
    pre:    this != NULL
    post:   None
    return: List of Lists representing the noise plate.
    ---------------------------------------------------------------------------
    '''
    def Get_Plate(self):
        return self.Plate
    '''
    ---------------------------------------------------------------------------
    info:   Adds or subtracts some random number from each index within the
            plate. Clamps values below 0 and above 100.
    pre:    this != NULL
    post:   #this != this
    return: None
    ---------------------------------------------------------------------------
    '''
    def Pass(self):
        for x in range(self.Width):
            for y in range(self.Height):
                if (random.randrange(2) == 1):
                    self.Plate[x][y] -= random.randrange(0, self.D_Pass)
                else:
                    self.Plate[x][y] += random.randrange(0, self.D_Pass)
                self.Plate[x][y] = Clamp(self.Plate[x][y])
    '''
    ---------------------------------------------------------------------------
    info:   Smooths each index of the plate by averaging all adjacent neighbors
            and letting this account for 10% of the given indexes value.
    pre:    this != NULL
    post:   #this != this
    return: None
    ---------------------------------------------------------------------------
    '''
    def Smooth(self):
        for x in range(self.Width):
            for y in range(self.Height):

                #Average of all of my adjacent neighbors.
                Averaged_Estimate = \
                      self.Plate[ (x-1)%self.Width ] [y]  \
                    + self.Plate[x]                  [ (y-1)%self.Height ] \
                    + self.Plate[ (x+1)%self.Width ] [y]  \
                    + self.Plate[x]                  [ (y+1)%self.Height ] \
                    + self.Plate[ (x-1)%self.Width ] [ (y-1)%self.Height ] \
                    + self.Plate[ (x-1)%self.Width ] [ (y+1)%self.Height ] \
                    + self.Plate[ (x+1)%self.Width ] [ (y-1)%self.Height ] \
                    + self.Plate[ (x+1)%self.Width ] [ (y+1)%self.Height ] 
                Averaged_Estimate = Averaged_Estimate / 8
                
                #The average of my neighbors accounts for 10% of myself.
                self.Plate[x][y]  = (self.Plate[x][y] *  .9) \
                    + (Averaged_Estimate * .1)
                
                #Convert back to int after float operations.
                self.Plate[x][y]  = int(round(self.Plate[x][y]))
                self.Plate[x][y] = Clamp(self.Plate[x][y])
    '''
    ---------------------------------------------------------------------------
    info:   Randomly selects indexes Num_Steps times, and adds or subtracts a 
            random amount from it.
    pre:    this != NULL
    post:   #this != this
    return: None
    ---------------------------------------------------------------------------
    '''
    def Random_Step(self):
        x = random.randrange(0, self.Width)
        y = random.randrange(0, self.Height)
        if (random.randrange(2) == 1):
            self.Plate[x][y] -= random.randrange(0, self.D_Step)
        else:
            self.Plate[x][y] += random.randrange(0, self.D_Step)
        self.Plate[x][y] = Clamp(self.Plate[x][y])

    '''
    ---------------------------------------------------------------------------
    info:   Randomly selects an index to nuke. Generates a random number based
            on D_Nuke to subtract or add to this value at the index.
            Distributes this effect to surrounding neighbors.
    pre:    this != NULL
    post:   #this != this
    return: None
    ---------------------------------------------------------------------------
    '''
    def Nuke(self):
        x = random.randrange(0, self.Width)
        y = random.randrange(0, self.Height)
        Amount = 0
        if (random.randrange(2) == 1):
            Amount -= random.randrange(0, self.D_Nuke)
        else:
            Amount += random.randrange(0, self.D_Nuke)
        self.Plate[x][y] += Amount
        '''
        .......................................................................
        Cycle back to the upper left tile in the set of 9. For instance:
         + - + - + - +
         |   |   |   |
         + - + - + - + 
         |   | X |   | 
         + - + - + - + 
         |   |   |   |
         + - + - + - +
         Would become:
         + - + - + - +
         | X |   |   |
         + - + - + - + 
         |   |   |   |
         + - + - + - + 
         |   |   |   |
         + - + - + - + 
         After this, distribute the altering amount by half to all surrounding
         neighbors. This has a cratering effect.
        ....................................................................... 
        '''
        x = (x - 1) % self.Width
        y = (y - 1) % self.Height
        for row in range(3):
            for col in range(3):
                self.Plate[(x+row)%self.Width][(y+col)%self.Height] \
                    += (Amount / 2)

    '''
    ---------------------------------------------------------------------------
    info:   Shifts the board up or down by the specified amount.
    pre:    this != NULL
    post:   #this != this
    return: None
    ---------------------------------------------------------------------------
    '''
    def Shift(self, Amount):
        for x in range(self.Width):
            for y in range(self.Height):
                self.Plate[x][y] += Amount
    
    '''
    ---------------------------------------------------------------------------
    info:   Returns the average value of the board. Used in conjunction with
            self.Shift in order to determine if the board is leaning too much
            in one direction.
    pre:    this != NULL
    post:   #this != this
    return: Average value of board.
    ---------------------------------------------------------------------------
    '''
    def Get_Average(self):
        Average = 0
        for x in range(self.Width):
            for y in range(self.Height):
                Average += self.Plate[x][y]
        Average = Average / (self.Height * self.Width)
        return Average

#End of class Noise -----------------------------------------------------------
if __name__ == '__main__':
    Noise_Gen = Noise(10, 10)
    for x in range(1000):
        Noise_Gen.Pass()
    for x in range(100):
        Noise_Gen.Random_Step()
    for x in range(30):
        Noise_Gen.Smooth()
    for x in range(10):
        Noise_Gen.Nuke()
    for x in range(5):
        Noise_Gen.Smooth()
    print(Noise_Gen.Get_Average())
    if   Noise_Gen.Get_Average() > 70:
        Noise_Gen.Shift(-10)
    elif Noise_Gen.Get_Average() < 30:
        Noise_Gen.Shift(10)

    Noise_Plate = Noise_Gen.Get_Plate()
    for Row in Noise_Plate:
        Visual_Row = []
        for Val in Row:
            if Val >= 60:
                Visual_Row.append('M')
            elif Val < 60 and Val >= 30:
                Visual_Row.append('L')
            else:
                Visual_Row.append('O')
        print(Visual_Row)