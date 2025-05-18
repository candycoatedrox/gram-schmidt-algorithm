import copy
import math
import itertools
from rational import Rational, rat, ratOrInt

def isScalar(a):
    if isinstance(a, int):
        return True
    if isinstance(a, float):
        return True
    if isinstance(a, Rational):
        return True
    return False

def isVector(a):
    if isinstance(a, Vector):
        return True
    if isinstance(a, NormalVector):
        return True

def isSquare(a):
    b = math.sqrt(a)
    return b.is_integer()

# yeah i copied some code directly from my linkedlist project just to do an overly complex way of checking
# whether a randomly shuffled ordering is swapped an odd or even amount of times... haha... what about it...
def swap(list, key1: int, key2: int):
    if not(isinstance(key1, int)) or not(isinstance(key2, int)):
        raise TypeError("list indices must be integers or slices")
    if key1 >= len(list) or key1 < -len(list) or key2 >= len(list) or key2 < -len(list):
        raise KeyError("list index out of range")
    
    v1 = list[key1]
    v2 = list[key2]
    list[key1] = v2
    list[key2] = v1

def inOrder(a):
    s = sorted(a)
    return a == s

def orderIsEven(a: tuple) -> bool:
    "Returns a boolean based on whether a given ordering of a range of numbers has even swaps (True) or odd swaps (False)."
    # done via bubble sort, because I don't know how else to do it
    
    # input tuple, convert to list, because i don't know how to work with tuples ayyyy
    l = []
    for n in a:
        l.append(a)

    swaps = 0
    while not inOrder(l):
        for i in range(len(l) - 1):
            if l[i] > l[i+1]:
                swaps += 1
                l.swap(i, i+1)

    if (swaps % 2) == 0:
        return True
    else:
        return False

def identity(dimV: int):
    "Returns an n x n identity matrix."
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

def zero(dimV: int, dimW: int = None):
    "Returns the zero vector or matrix for the given dimension(s)."

    z = []

    # IF VECTOR: dimV = dim
    if dimW == None:
        for n in range(dimV):
            z.append(0)
        return Vector(z)
    
    # IF MATRIX: dimV = k, dimW = n
    else:
        for r in range(dimV):
            row = []
            for c in range(dimW):
                row.append(0)
            z.append(copy.deepcopy(row))
        return Matrix(z)

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
    
    if v.dim != w.dim:
        raise ValueError("vectors must share dimension")
    
    dimV = v.dim
    sum = 0
    for i in range(dimV):
        for j in range(dimV):
            a = (v[i] * w[j] * Gij[i][j])
            sum += a
    
    if isinstance(v, NormalVector):
        sum /= math.sqrt(v.divSqrt)
    if isinstance(w, NormalVector):
        sum /= math.sqrt(w.divSqrt)
    
    return sum

def maxLength(l: list):
    "Returns the length of the longest item in a list."

    maxLen = 0
    for n in l:
        if len(n) > maxLen:
            maxLen = len(n)
    return maxLen

def vertList(vectors: list):
    "Returns a string representation of a list of vectors of the same dimension, in vertical form."

    norm = False
    dimV = vectors[0].dim
    comps = []
    s = ""

    for v in vectors:
        if not isVector(v):
            raise TypeError("all arguments must be vectors")
        elif isinstance(v, NormalVector):
            norm = True
        
        if v.dim != dimV:
            raise ValueError("all vectors must share dimension")
        
        comps.append(v.vert().split("\n"))
    
    for i in range(dimV):
        if i != 0:
            s += "\n"
        
        for n in range(len(comps)):
            if n != 0:
                if norm:
                    s += "   "
                else:
                    s += " "
            s += comps[n][i]
            
            space = maxLength(comps[n]) - len(comps[n][i])
            for x in range(space):
                s += " "
    
    return s

class Vector:

    # MATH NEEDS TO BE ABLE TO FUNCTION WITH BOTH OTHER VECTORS AND NORMALVECTORS

    def __init__(self, vector):
        "Initialize a vector."
        self.vector = vector
        self.dim = len(self.vector)

    def __len__(self):
        "Returns the dimension of a vector."
        return self.dim
    
    def __getitem__(self, n):
        "Returns the nth component of a vector."
        if not(isinstance(n, int)):
            raise TypeError("component indices must be integers or slices")
        if n >= self.dim or n < -self.dim:
            raise KeyError("component index out of range")
        
        return self.vector[n]

    def __setitem__(self, n, value):
        "Sets the nth component of a vector to the specified value."
        if not(isinstance(n, int)):
            raise TypeError("component indices must be integers or slices")
        if n >= self.dim or n < -self.dim:
            raise KeyError("component index out of range")
        
        self.vector[n] = value
    
    def __iter__(self):
        "Allows iteration through components of a vector."
        for i in range(self.dim):
            yield self[i]
    
    def reduce(self):
        for i in range(self.dim):
            if isinstance(self[i], Rational):
                self[i].reduce()
                if self[i].denom == 1:
                    self[i] = int(self[i])
    
    def mag2(self, Gij):
        "Returns the magnitude-squared of a vector within a given inner product space."
        return innerProduct(self, self, Gij)

    def mag(self, Gij):
        "Returns the magnitude of a normalized vector."
        return math.sqrt(self.mag2(Gij))

    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."

        if self.dim == other.dim:
            if self.vector == other.vector:
                return 0
            # kind of arbitrary but SOMETHING needs to go here right?
            elif self.mag() <= other.mag():
                return -1
            else:
                return 1
        elif self.dim < other.dim:
            return -1
        else:
            return 1

    def __neg__(self):
        "Define unary negation with the - symbol."
        return self * -1

    def __add__(self, other):
        "Add two vectors."

        if self.dim != other.dim:
            raise ValueError("vectors must share dimension")
    
        sum = []
        for i in range(self.dim):
            sum.append(self[i] + other[i])
        return Vector(sum)

    def __sub__(self, other):
        "Subtract two vectors."
        return self + (-other)

    def __mul__(self, other):
        "Multiply a vector by a constant or matrix."

        if isScalar(other):
            a = ratOrInt(other)
            p = copy.deepcopy(self)
            for i in range(self.dim):
                p[i] = ratOrInt(p[i] * a)
            return p

        elif isinstance(other, Matrix):
            return self.matrix() * other

        else:
            raise TypeError("can only multiply a vector by a scalar or matrix")
        
    def __truediv__(self, other):
        "Divide a vector by a scalar."

        if isScalar(other):
            return self * (Rational(1,other))

        else:
            raise TypeError("can only divide a vector by a scalar")

    def __radd__(self, other):
        "Add two vectors, reflected version."
        return self + other

    def __rsub__(self, other):
        "Subtract two vectors, reflected version."
        return -(self - other)
    
    def __rmul__(self, other):
        "Multiply a vector by a constant or matrix, reflected version."
        if isScalar(other):
            return self * other
        
        elif isinstance(other, Matrix):
            return other * self.matrix()

        else:
            raise TypeError("can only multiply a vector by a scalar or matrix")
    
    def __iadd__(self, other):
        "Alter a vector, adding another vector to it."
        self = self + other
        return self

    def __isub__(self, other):
        "Alter a vector, subtracting another vector from it."
        self = self - other
        return self
    
    def __imul__(self, other):
        "Alter a vector, multiplying it by by a constant or matrix."
        self = self * other
        return self
    
    def __itruediv__(self, other):
        "Alter a vector, dividing it by by a constant."
        self = self / other
        return self
    
    def vec(self):
        "Returns itself. Exists to allow vec() when a NormalVector is expected."
        return self

    def normalize(self, Gij):
        "Normalize a vector within a given inner product space."
        # input Vector — outputs NormalVector (unless mag2 is a perfect square)

        # getting any fractional components out of the way
        v = self
        rat = False
        d = []
        for n in self:
            if isinstance(n, Rational):
                rat = True
                d.append(n.denom)
        
        if rat:
            l = math.lcm(*d)
            v *= l
            v.reduce()
            
            g = math.gcd(*v.vector)
            v /= g

        mag2 = v.mag2(Gij)
        if isSquare(mag2):
            v /= math.sqrt(mag2)
            return v
        else:
            return NormalVector(mag2, v.vector)

    def matrix(self):
        "Returns a vector as a matrix."

        m = []
        for n in self:
            nL = [n]
            m.append(copy.deepcopy(nL))
        return Matrix(m)
    
    def __str__(self):
        "Provide a basic string representation of a vector."

        s = "("
        for i in range(self.dim):
            if i != 0:
                s += " "
            s += str(self[i])
        s += ")"

        return s
    
    def __repr__(self):
        return str(self)
    
    def vert(self):
        "Returns a basic string representation of a vector, in vertical form."

        s = ""
        for i in range(self.dim):
            if i != 0:
                s += "\n"
            s += f'|{self[i]}|'
        
        return s

# You should not ever be defining a NormalVector directly.
# Always define a Vector first, then normalize() it.
class NormalVector:

    # MATH NEEDS TO BE ABLE TO FUNCTION WITH BOTH OTHER NORMALVECTORS AND VECTORS

    def __init__(self, divSqrt, vector):
        "Initialize a normalized vector."
        self.divSqrt = divSqrt
        self.vector = vector
        self.dim = len(self.vector)
    
    def __len__(self):
        "Returns the dimension of a normalized vector."
        return self.dim
    
    def __getitem__(self, n):
        "Returns the nth component of a vector."
        if not(isinstance(n, int)):
            raise TypeError("component indices must be integers or slices")
        if n >= self.dim or n < -self.dim:
            raise KeyError("component index out of range")
        
        return self.vector[n]

    def __setitem__(self, n, value):
        "Sets the nth component of a vector to the specified value."
        if not(isinstance(n, int)):
            raise TypeError("component indices must be integers or slices")
        if n >= self.dim or n < -self.dim:
            raise KeyError("component index out of range")
        
        self.vector[n] = value
    
    def __iter__(self):
        "Allows iteration through components of a normalized vector."
        for i in range(self.dim):
            yield self[i]
    
    def reduce(self):
        for i in range(self.dim):
            if isinstance(self[i], Rational):
                self[i].reduce()
                if self[i].denom == 1:
                    self[i] = int(self[i])

    def mag(self):
        "Returns the magnitude of a normalized vector."
        # lol
        return 1
    
    def vec(self):
        "Returns the vector component of a normalized vector."
        return Vector(self.vector)

    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."
        
        if self.dim == other.dim:
            if self.vector == other.vector:
                return 0
            else:
                # i dunno man
                return -1
        elif self.dim < other.dim:
            return -1
        else:
            return 1

    def __neg__(self):
        "Define unary negation with the - symbol."
        return self * -1
    
    def __abs__(self):
        "Define absolute value of a normalized vector."
        return 1

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
            for i in range(self.dim):
                p[i] = ratOrInt(p[i] * a)
            return p

        elif isinstance(other, Matrix):
            return other * self

        else:
            raise TypeError("can only multiply a vector by a scalar or matrix")
        
    def __truediv__(self, other):
        "Divide a normalized vector by a scalar."

        if isScalar(other):
            return self * (1/other)

        else:
            raise TypeError("can only divide a vector by a scalar")

    def __radd__(self, other):
        "Add two normalized vectors, reflected version."
        return self + other

    def __rsub__(self, other):
        "Subtract two normalized vectors, reflected version."
        return -(self - other)

    def __rmul__(self, other):
        "Multiply a normalized vector by a constant or matrix, reflected version."
        return self * other
    
    def __iadd__(self, other):
        "Alter a normalized vector, adding another vector to it."
        self = self + other
        return self

    def __isub__(self, other):
        "Alter a normalized vector, subtracting another vector from it."
        self = self - other
        return self
    
    def __imul__(self, other):
        "Alter a normalized vector, multiplying it by by a constant or matrix."
        self = self * other
        return self
    
    def __itruediv__(self, other):
        "Alter a normalized vector, dividing it by by a constant."
        self = self / other
        return self
    
    def __str__(self):
        "Provide a basic string representation of a normalized vector."

        s = "("
        if self.divSqrt != 0:
            s = f'(1/√{self.divSqrt})('

        for i in range(self.dim):
            if i != 0:
                s += " "
            s += str(self[i])
        s += ")"

        return s
    
    def __repr__(self):
        return str(self)
    
    def vert(self):
        "Returns a basic string representation of a vector, in vertical form."

        s = ""
        for i in range(self.dim):
            if i != 0:
                s += "\n"
            s += f'|{self[i]}|'
            if i == 0:
                s += " * 1"
            elif i == 1:
                s += f'  √{self.divSqrt}'
        
        return s

class Matrix:
    
    def __init__(self, values):
        # should be organized as outer lists = rows
        # convert all floats to rational numbers...?

        if isinstance(values, list):
            # assume all elements of values are the same type
            if isinstance(values[0], list):
                self.values = values

            # automatically convert a list of vectors into a properly formatted list of lists?
            elif isinstance(values[0], Vector):
                dim = values[0].dim
                for c in values:
                    if c.dim != dim:
                        raise ValueError("inconsistent amount of rows")
                
                matrix = []
                for r in range(dim):
                    row = []
                    for c in range(len(values)):
                        row.append(values[c][r])
                    matrix.append(copy.deepcopy(row))
                
                self.values = matrix

            else:
                raise TypeError("matrix must be made of a list of either lists (rows) or vectors (columns)")
            
            # k = number of rows; n = number of columns
            self.k = len(self.values)
            self.n = len(self.values[0])
            self.kN = (self.k, self.n)

            self.second_access = False

            for r in self.values:
                if len(r) != self.n:
                    raise ValueError("inconsistent amount of columns")
        
        else:
            raise TypeError("matrix must be made of a list of either lists (rows) or vectors (columns)")

    def __getitem__(self, key):
        "Returns the ith/jth component of a matrix."
        # proper syntax: self[i][j]
        # first access will use i, second will use j

        if not(isinstance(key, int)):
            raise TypeError("component indices must be integers or slices")
        
        if not self.second_access:
            if key >= self.n or key < -self.n:
                raise KeyError("component index i out of range")
            
            self.key1 = key
            self.second_access = True
            return self
        
        else:
            if key >= self.k or key < -self.k:
                raise KeyError("component index j out of range")
            
            self.second_access = False
            return self.values[key][self.key1]

    def __setitem__(self, key, value):
        "Sets the ith/jth component of a matrix to the specified value."
        # proper syntax: self[i][j]
        # first access will use i, second will use j

        if not(isinstance(key, int)):
            raise TypeError("component indices must be integers or slices")
        
        if not self.second_access:
            if key >= self.n or key < -self.n:
                raise KeyError("component index i out of range")
            
            self.key1 = key
            self.second_access = True
            return self
        
        else:
            if key >= self.k or key < -self.k:
                raise KeyError("component index j out of range")
            
            self.second_access = False
            self.values[key][self.key1] = value
    
    def reduce(self):
        for i in range(self.n):
            for j in range(self.k):
                if isinstance(self[i][j], Rational):
                    self[i][j].reduce()
                    if self[i][j].denom == 1:
                        self[i][j] = int(self[i][j])
    
    def isSquare(self):
        "Returns a boolean value depending on whether a matrix is square."
        return self.k == self.n
    
    def col(self, i):
        "Returns the specified column of a matrix as a list of values."

        c = []
        for r in range(self.k):
            c.append(self.values[r][i])
        return c
    
    def rowVectors(self):
        "Returns the rows of a matrix as a list of vectors."

        vectors = []
        for r in self.values:
            vectors.append(Vector(r))
        return vectors
    
    def columnVectors(self):
        "Returns the columns of a matrix as a list of vectors."

        vectors = []
        n = self.n
        for i in range(n):
            vectors.append(Vector(self.col(i)))
        return vectors
    
    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."

        if self.kN == other.kN:
            if self.values == other.values:
                return 0
        # kind of arbitrary but SOMETHING needs to go here right?
        elif (self.k * self.n) < (other.k * other.n):
            return -1
        else:
            return 1

    def __neg__(self):
        "Define unary negation with the - symbol."
        return self * -1

    def __add__(self, other):
        "Add two matrices."

        if self.kN != other.kN:
            raise ValueError("matrices must share dimensions")
        
        sum = []
        for j in range(self.k):
            r = []
            for i in range(self.n):
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
            for j in range(self.k):
                for i in range(self.n):
                    p.values[j][i] = ratOrInt(p.values[j][i] * a)
            return p

        elif isinstance(other, Vector):
            return self * Matrix(other)

        elif isinstance(other, Matrix):
            if self.k != other.n:
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
            
            return p

        else:
            raise TypeError("can only multiply a matrix by a scalar, vector, or matrix")
    
    def __truediv__(self, other):
        "Divide a matrix by a scalar."

        if isScalar(other):
            return self * (1/other)

        else:
            raise TypeError("can only divide a matrix by a scalar")

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
            return Matrix(other) * self
    
    def __iadd__(self, other):
        "Alter a matrix, adding another matrix to it."
        self = self + other
        return self

    def __isub__(self, other):
        "Alter a matrix, subtracting another matrix from it."
        self = self - other
        return self
    
    def __imul__(self, other):
        "Alter a matrix, multiplying it by by a constant, vector, or matrix."
        self = self * other
        return self
    
    def __itruediv__(self, other):
        "Alter a matrix, dividing it by by a constant."
        self = self / other
        return self

    def inverse(self):
        "Calculate the inverse of a matrix."
        
        if not self.isSquare():
            raise ValueError("matrix must be a square matrix")
        
        pass

    def det(self):
        "Calculate the determinant of a matrix."
        
        if not self.isSquare():
            raise ValueError("matrix must be a square matrix")
        
        d = 0
        orders = itertools.permutations(range(self.k))
        for o in orders:
            a = 1
            for j in range(self.k):
                i = o[j]
                a *= self[i][j]

            if not orderIsEven(o):
                a *= -1
            d += a
        
        return d
    
    def __str__(self):
        "Provide a basic string representation of a matrix."

        s = ""
        for j in range(self.k):
            if j != 0:
                s += "\n"
            s += "|"
            for i in range(self.n):
                if i != 0:
                    s += " "
                s += str(self.values[j][i])
            s += "|"
        
        return s
    
    def __repr__(self):
        return str(self)