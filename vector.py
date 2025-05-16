import copy
from rational import Rational, rat

def isScalar(a):
    if isinstance(a, int):
        return True
    if isinstance(a, float):
        return True
    if isinstance(a, Rational):
        return True
    return False

def ratOrInt(a):
    if isinstance(a, int):
        return a
    
    if not isinstance(a, Rational):
        aNum = rat(a)
    if aNum.isWhole():
        aNum = int(aNum)
    return aNum

def identity(dimV):
    m = []
    for r in range(dimV):
        row = []
        for c in range(dimV):
            if r == c:
                row.append(1)
            else:
                row.append(0)
        m.append(copy.deepcopy(row))

    return Matrix(m)

def vector(a):
    "Converts a list or string into a vector."

    if isinstance(a, Vector):
        return a
    
    elif isinstance(a, list):
        return Vector(a)
    
    elif isinstance(a, str):
        # fill me in
        pass

    else:
        raise TypeError("can only convert list or str to vector")

def innerProduct(v, w, Gij):
    "Calculate the inner product of two vectors in a given inner product space."
    
    # needs to work w/ Vectors + NormalVectors
    if v.dim() != w.dim():
        raise ValueError("vectors must share dimension")
    
    dimV = v.dim()

class Vector:

    # MATH NEEDS TO BE ABLE TO FUNCTION WITH BOTH OTHER VECTORS AND NORMALVECTORS

    def __init__(self, vector):
        "Initialize a vector."
        self.vector = vector

    def __len__(self):
        "Returns the dimension of a vector."
        return len(self.vector)

    def dim(self):
        "Returns the dimension of a vector."
        return len(self)
    
    def mag2(self, Gij):
        "Returns the magnitude-squared of a vector within a given inner product space."
        return innerProduct(self, self, Gij)

    def mag(self):
        "Returns the magnitude of a normalized vector."
        pass

    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."

        if self.dim() == other.dim():
            if self.vector == other.vector:
                return 0
            # kind of arbitrary but SOMETHING needs to go here right?
            elif self.mag() <= other.mag():
                return -1
            else:
                return 1
        elif self.dim() < other.dim():
            return -1
        else:
            return 1

    def __neg__(self):
        "Define unary negation with the - symbol."
        
        new = copy.deepcopy(self)
        for i in new.vector:
            new.vector[i] *= -1
        return new

    def __add__(self, other):
        "Add two vectors."

        if self.dim() != other.dim():
            raise ValueError("vectors must share dimension")
    
        sum = []
        for i in range(self.dim()):
            sum.append(self.vector[i] + other.vector[i])
        return sum

    def __sub__(self, other):
        "Subtract two vectors."
        return self + (-other)

    def __mul__(self, other):
        "Multiply a vector by a constant or matrix."

        if isScalar(other):
            a = ratOrInt(other)
            p = copy.deepcopy(self)
            for i in range(self.dim()):
                p.vector[i] = ratOrInt(p.vector[i] * a)
            return p

        elif isinstance(other, Matrix):
            return other * self

        else:
            raise TypeError("can only multiply a vector by a scalar or matrix")

    def __radd__(self, other):
        "Add two vectors, reflected version."
        return other + self

    def __rsub__(self, other):
        "Subtract two vectors, reflected version."
        return other - self
    
    def __rmul__(self, other):
        "Multiply a vector by a constant or matrix, reflected version."
        return self * other

    def normalize(self, Gij):
        # input Vector — outputs NormalVector
        "Normalize a vector within a given inner product space."
    
    def __str__(self):
        "Provide a basic string representation of a normalized vector."

        s = "("
        for i in range(len(self.vector)):
            s += self.vector[i]
            if i != 0:
                s += " "
        s += ")"

        return s

class NormalVector:

    # MATH NEEDS TO BE ABLE TO FUNCTION WITH BOTH OTHER NORMALVECTORS AND VECTORS

    def __init__(self, divSqrt, vector):
        "Initialize a normalized vector."
        self.divSqrt = divSqrt
        self.vector = vector
    
    def __len__(self):
        "Returns the dimension of a normalized vector."
        return len(self.vector)

    def dim(self):
        "Returns the dimension of a normalized vector."
        return len(self)

    def mag(self):
        "Returns the magnitude of a normalized vector."
        # lol
        return 1

    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."
        
        if self.dim() == other.dim():
            if self.vector == other.vector:
                return 0
            else:
                # i dunno man
                return -1
        elif self.dim() < other.dim():
            return -1
        else:
            return 1

    def __neg__(self):
        "Define unary negation with the - symbol."
        
        new = copy.deepcopy(self)
        for i in new.vector:
            new.vector[i] *= -1
        return new

    def __add__(self, other):
        "Add two normalized vectors."
        pass

    def __sub__(self, other):
        "Subtract two normalized vectors."
        pass

    def __mul__(self, other):
        "Multiply a normalized vector by a constant or matrix."

        if isScalar(other):
            a = ratOrInt(other)
            p = copy.deepcopy(self)
            for i in range(self.dim()):
                p.vector[i] = ratOrInt(p.vector[i] * a)
            return p

        elif isinstance(other, Matrix):
            return other * self

        else:
            raise TypeError("can only multiply a vector by a scalar or matrix")

    def __radd__(self, other):
        "Add two normalized vectors, reflected version."
        return other + self

    def __rsub__(self, other):
        "Subtract two normalized vectors, reflected version."
        return other - self

    def __rmul__(self, other):
        "Multiply a normalized vector by a constant or matrix, reflected version."
        return self * other
    
    def __str__(self):
        "Provide a basic string representation of a normalized vector."

        s = "("
        if self.divSqrt != 0:
            s = f'1/sqrt({self.divSqrt})('

        for i in range(len(self.vector)):
            s += self.vector[i]
            if i != 0:
                s += " "
        s += ")"

        return s

class Matrix:
    
    def __init__(self, values):
        # should be organized as outer lists = rows
        # convert all floats to rational numbers...?
        self.values = values

        n = self.n()
        for r in self.values:
            if len(r) != n:
                raise ValueError("inconsistent amount of columns")

    def k(self):
        "Returns output dimension and number of rows in a matrix."
        return len(self.values)

    def n(self):
        "Returns input dimension and number of columns in a matrix."
        return len(self.values[0])
    
    def kN(self):
        "Returns both k and n. Useful for checking whether two matrices share the same dimensions."
        return (self.k(), self.n())

    def isSquare(self):
        "Returns a boolean value depending on whether a matrix is square."
        return self.k() == self.n()
    
    def col(self, i):
        "Returns the specified column of a matrix as a list of values."

        c = []
        for r in range(self.k()):
            c.append(r[i])
        return c
    
    def rowVectors(self):
        "Returns the rows of a matrix as a list of vectors."

        vectors = []
        for r in self.values:
            vectors.append(vector(r))
        return vectors
    
    def columnVectors(self):
        "Returns the columns of a matrix as a list of vectors."

        vectors = []
        n = self.n()
        for i in range(n):
            vectors.append(Vector(self.col(i)))
        return vectors
    
    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."

        if self.kN() == other.kN():
            if self.values == other.values:
                return 0
            # kind of arbitrary but SOMETHING needs to go here right?
        elif (self.k() * self.n()) < (other.k() * other.n()):
            return -1
        else:
            return 1

    def __neg__(self):
        "Define unary negation with the - symbol."
        
        new = copy.deepcopy(self)
        for j in new.k():
            for i in new.n():
                new.values[j][i] *= -1
        return new

    def __add__(self, other):
        "Add two matrices."

        if self.kN() != other.kN():
            raise ValueError("matrices must share dimensions")
        
        sum = []
        for j in range(self.k()):
            r = []
            for i in range(self.n()):
                r.append(self.values[j][i] + other.values[j][i])
            sum.append(copy.deepcopy(r))
        return sum

    def __sub__(self, other):
        "Subtract two matrices."
        return self + (-other)

    def __mul__(self, other):
        "Multiply two matrices, a matrix and a vector, or a matrix and a constant."
        
        if isScalar(other):
            a = ratOrInt(other)
            p = copy.deepcopy(self)
            for j in range(self.k()):
                for i in range(self.n()):
                    p.values[j][i] = ratOrInt(p.values[j][i] * a)

        elif isinstance(other, Vector):
            pass

        elif isinstance(other, Matrix):
            if self.k() != other.n():
                raise ValueError("matrices are not compatible")
            
            # gives other.k x self.n matrix
            p = []
            for j in range(other.k):
                r = []
                for i in range(self.n):
                    c = other.col(i)
                    x = 0
                    for ind in range(self.n):
                        x += (self.values[j][ind] * c[ind])

                    r.append(copy.deepcopy(x))
                
                p.append(copy.deepcopy(r))

        else:
            raise TypeError("can only multiply a matrix by a scalar, vector, or matrix")
        
        return p

    def __radd__(self, other):
        "Add two matrices, reflected version."
        return other + self

    def __rsub__(self, other):
        "Subtract two matrices, reflected version."
        return other - self

    def __rmul__(self, other):
        "Multiply a matrix and a vector or a matrix and a constant, reflected version."

        if isScalar(other):
            return self * other
        
        elif isinstance(other, vector):
            pass

    def inverse(self):
        "Calculate the inverse of a matrix."
        pass

    def det(self):
        "Calculate the determinant of a matrix."
        
        if not self.isSquare():
            raise ValueError("matrix must be a square matrix")
        
        pass
    
    def __str__(self):
        "Provide a basic string representation of a matrix."

        s = ""
        for j in range(self.k()):
            if j != 0:
                s += "\n"
            s += "|"
            for i in range(self.n()):
                if i != 0:
                    s += " "
                s += self.values[j][i]
            s += "|"
        
        return s