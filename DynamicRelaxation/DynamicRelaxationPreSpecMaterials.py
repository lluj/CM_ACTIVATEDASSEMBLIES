class Materials():
    
    # Materials properties are in N and mm
    # E in N/mm2
    # I in mm^4
    # A in mm^2
    # D in mm
    
    def __init__(self):    
        self.name = 'materials'

    def steel(self, NAME = 'STEEL', E = 210000, I = 0.78539, A = 3.1415, C = 1, D = 1): 
        return [NAME, E, A, I, C, D]

    def gfrp(self, NAME = 'GFRP', E = 20000, I = 0.78539, A = 3.1415, C = 1, D = 1): 
        return [NAME, E, A, I, C, D]

    def rattan(self, NAME = 'RATTAN', E = 3500, I = 0.78539, A = 3.1415, C = 1, D = 1): 
        return [NAME, E, A, I, C, D]
    
    def pvc(self, NAME = 'PVC', E = 3000, I = 0.78539, A = 3.1415, C = 1, D = 1):
        return [NAME, E, A, I, C, D]
        
    def membrane(self, NAME = 'MEMBRANE', E = 10, I = 0.78539, A = 3.1415, C = 0.5, D = 1): 
        return [NAME, E, A, I, C, D]
    
    def wood(self, NAME = 'WOOD', E = 11000, I = 0.78539, A = 3.1415, C = 1, D = 1): 
        return [NAME, E, A, I, C, D]

    #def wood(self, NAME = 'WOOD', E = 2100, I = 1000, A = 1000, C = 1.9, D = 1): 
    #    return [NAME, E, A, I, C, D]
