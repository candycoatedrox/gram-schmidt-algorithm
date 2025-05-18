# pg 96 of notes
import sys
import time
import copy
from rational import Rational, rat, ratOrInt
from vector import *

# make the whole thing function on fractions???
# currently started to make it function on floats but i can fix that

def slowType(text):
    "Makes the program more user-friendly by appearing to type out the input."
    for l in text:
        print(l, end="")
        sys.stdout.flush()
        time.sleep(.025)

def slowInput(prompt):
    # how do i do this???
    pass

def getDim():
    valid = False
    while not(valid):
        compNum = input("Enter the number of vector components: ")
        try:
            compNum = int(compNum)
            if compNum >= 1:
                valid = True
            else:
                print("Please enter a number greater than or equal to 1.")
        except:
            print("Please enter an integer.")

    valid = False
    while not(valid):
        dimV = input("Enter the number of basis vectors: ")
        try:
            dimV = int(dimV)
            if dimV > compNum:
                print("Dimension must be less than or equal to the number of components.")
            elif dimV >= 1:
                valid = True
            else:
                print("Please enter a number greater than or equal to 1.")
        except:
            print("Please enter an integer.")
    
    return (compNum, dimV)

def getInnerProd(dimV):
    standardAns = False
    while not standardAns:
        standard = input("Standard inner product? (y/n): ")
        if standard == "y" or standard == "Y":
            return identity(dimV)
        elif standard == "n" or standard == "N":
            standardAns = True
        else:
            print('Please input either "y" or "n".')
    
    g = []
    for r in range(dimV):
        valid = False
        while not(valid):
            rawRow = input(f"Enter row {r + 1} of Gij, with components separated by spaces: ")
            rStr = rawRow.split()

            row = []
            if len(rStr) == dimV:
                valid = True
                for x in rStr:
                    try:
                        xNum = ratOrInt(x)
                        row.append(xNum)
                    except:
                        valid = False
                        print("Please enter a list of integers, rational numbers, or floats.")
            else:
                print(f"Please enter a row with {dimV} components.")
        
        g.append(copy.deepcopy(row))
    
    # should hypothetically have another check here that it's symmetrical...
    # or just. change it so you just enter, ex. G11, G12, G22 for dim = 2
    return Matrix(g)

def getBasis(compNum, dimV):
    print("\n")
    basis = []
    for n in range(dimV):
        valid = False
        while not(valid):
            rawVector = input(f"Enter basis vector {n + 1}, with components separated by spaces: ")
            vStr = rawVector.split()

            vector = []
            if len(vStr) == compNum:
                valid = True
                for x in vStr:
                    xNum = ratOrInt(x)
                    vector.append(xNum)
                    '''try:
                        xNum = ratOrInt(x)
                        vector.append(xNum)
                    except:
                        valid = False
                        print("Please enter a list of integers, rational numbers, or floats.")
                        break'''
            else:
                print(f"Please enter a vector with {compNum} components.")
        
        v = Vector(vector)
        basis.append(copy.deepcopy(v))

    return basis

def gramSchmidt(basis, Gij):
    e = []

    for n in range(len(basis)):
        en = basis[n]
        if n != 0:
            for i in range(n):
                p = innerProduct(basis[n], e[i].vec(), Gij)
                if isinstance(e[i], NormalVector):
                    p *= Rational(1, e[i].divSqrt)
                p = ratOrInt(p)
                p *= e[i].vec()

                en -= p

        e.append(en.normalize(Gij))

    return e

def main():
    compNum, dimV = getDim()
    Gij = getInnerProd(compNum)
    basis = getBasis(compNum, dimV)

    orthonormal = gramSchmidt(basis, Gij)
    print(f'Your orthonormal basis is:\n{vertList(orthonormal)}')


if __name__ == '__main__':
    main()