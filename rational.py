from decimal import *

def rat(a):
        "Converts a number or string into a rational."
        from math import floor

        if isinstance(a, Rational):
            return a
        
        elif isinstance(a, str):
            splitA = a.split("/")

            # check validity of rational
            if len(splitA) != 2:
                raise ValueError("improperly formatted rational number")
            
            return Rational(splitA[0], splitA[1])
        
        elif isinstance(a, int):
            return Rational(a, 1)
        
        elif isinstance(a, float) or isinstance(a, Decimal):
            if isinstance(a, float):
                # ensures precise representation of decimals
                aDec = Decimal(str(a))
            
            i = 7 # number of times to run the continued fractions formula — can be increased
            b0 = floor(aDec)
            err = aDec - b0
            #print(f'error initial value: {err}')
            # prevN1 is the numerator for n-1, prevD2 is the denominator for n-2, etc
            prevN1 = b0
            prevD1 = 1
            prevN2 = 1
            prevD2 = 0

            for n in range(0, i):
                if err == 0:
                    break

                numer, denom, err = contFract(err, prevN1, prevD1, prevN2, prevD2)

                prevN2 = prevN1
                prevD2 = prevD1
                prevN1 = numer
                prevD1 = denom
            return Rational(numer, denom)
        
        else:
            raise TypeError("can only convert str, int, float, or decimal to rational number")

def contFract(a, prevN1, prevD1, prevN2, prevD2):
    '''Calculates a single recurrent iteration of a continued fraction.'''

    # prevN1 is the numerator for n-1, prevD2 is the denominator for n-2, etc
    from math import floor
    b = 1/a
    #print(f'1/a = {b}')
    bN = floor(b)
    err = b - bN

    #print(f'prevN1 = {prevN1}; prevD1 = {prevD1}; prevN2 = {prevN2}; prevD2 = {prevD2}')

    numer = (bN * prevN1) + prevN2
    denom = (bN * prevD1) + prevD2
    #print(f'{numer}, {denom}')
    return numer, denom, err

def gcf(a, b):
        if a > b:
            small = b
            large = a
        else:
            small = a
            large = b
        
        factor = 1
        while 1 == 1:
            remainder = large % small
            if (remainder) == 0:
                factor = small
                break
            else:
                large = small
                small = remainder
        
        return factor

class Rational:

    def __init__(self, numer, denom):
        "Initialize a rational number."

        self.numer = numer
        self.denom = denom
        self.reduce()

    def reduce(self):
        "Reduce the fraction to lowest terms."

        numer = self.numer
        denom = self.denom

        # Ensures numerator and denominator are both whole numbers (only considers the first two digits past the decimal point)
        # (It doesn't matter if they end up as massive numbers, since they'll be reduced anyway)
        if isinstance(numer, float) and (not numer.is_integer):
            numer = int(numer * 100)
            denom = int(numer * 100)
        elif isinstance(denom, float) and (not denom.is_integer):
            numer = int(numer * 100)
            denom = int(numer * 100)

        if numer == denom:
            self.numer = 1
            self.denom = 1
            return
        
        common = gcf(numer, denom)
        numer = numer // common
        denom = denom // common
        if denom < 0:
            numer *= -1
            denom *= -1
        
        self.numer = int(numer)
        self.denom = int(denom)

    # I added this one because it's simple, it might be useful for the user, and it's convenient for division
    def invert(self):
        "Invert a rational number, swapping the numerator and denominator."

        return Rational(self.denom, self.numer)

    def __cmp__(self, other):
        "Comparson, used to implement ==, <, etc."

        if self.numer == other.numer and self.denom == other.denom:
            return 0
        else:
            dec1 = self.numer / self.denom
            dec2 = other.numer / other.denom

            if dec1 > dec2:
                return 1
            else:
                return -1

    def __neg__(self):
        "Define unary negation with the - symbol."

        numer = self.numer * -1
        denom = self.denom
        return Rational(numer, denom)

    def __abs__(self):
        "Define absolute value of a rational number."

        numer = self.numer
        denom = self.denom
        if self.numer < 0:
            numer *= -1
        return Rational(numer, denom)


    def __add__(self, other):
        "Add two rational numbers."

        otherCopy = other
        if isinstance(other, int) or isinstance(other, float):
            otherCopy = rat(other)
        elif self.denom == otherCopy.denom:
            return Rational(self.numer + otherCopy.numer, self.denom)
        
        # Converting both fractions to the same denominator
        n1 = self.numer * otherCopy.denom
        n2 = otherCopy.numer * self.denom
        denom = self.denom * otherCopy.denom

        return Rational(n1 + n2, denom)

    def __sub__(self, other):
        "Subtract two rational numbers."
        
        otherCopy = other
        if isinstance(other, int) or isinstance(other, float):
            otherCopy = rat(other)
        elif self.denom == otherCopy.denom:
            return Rational(self.numer - otherCopy.numer, self.denom)
        
        # Converting both fractions to the same denominator
        n1 = self.numer * otherCopy.denom
        n2 = otherCopy.numer * self.denom
        denom = self.denom * otherCopy.denom

        return Rational(n1 - n2, denom)

    def __mul__(self, other):
        "Multiply two rational numbers."

        otherCopy = other
        if isinstance(other, int) or isinstance(other, float):
            otherCopy = rat(other)
        
        numer = self.numer * otherCopy.numer
        denom = self.denom * otherCopy.denom
        return Rational(numer, denom)

    def __truediv__(self, other):
        "Divide two rational numbers."

        otherCopy = other
        if isinstance(other, int) or isinstance(other, float):
            otherCopy = rat(other)
        
        return self * otherCopy.invert()

    # I don't understand why the reflected operations are useful?
    # What's the point of defining the second one as "self" instead? When will it ever get called?
    # The docs say it's called when the object on the left doesn't have the original operation defined,
    # but I don't think defining operations within a class lets you mix classes anyway, so won't x + y always call __add__?
    def __radd__(self, other):
        "Add two rational numbers, reflected version."
        
        return other + self

    def __rsub__(self, other):
        "Subtract two rational numbers, reflected version."
        
        return -(self - other)

    def __rmul__(self, other):
        "Multiply two rational numbers, reflected version."

        return other * self

    def __rtruediv__(self, other):
        "Divide two rational numbers, reflected version."

        return other / self

    def __float__(self):
        "Convert a rational number to a float."

        return(self.numer / self.denom)
    
    def __int__(self):
        "Convert a rational number to an integer, rounded down."

        if self.isWhole():
            return self.numer
        else:
            flt = float(self)
            return int(flt)

    def __str__(self):
        "Provide a basic string representation of a rational number."
        return(f'{self.numer}/{self.denom}')
    
    def isWhole(self):
        "Return a boolean value based on whether a rational number is an integer."

        if self.denom == 1:
            return True
        else:
            return False
