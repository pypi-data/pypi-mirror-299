import numpy as np
class Set:
    def __init__(self, myArray):
        self.myArray = myArray
        self.arr = np.array(self.myArray)
    def display(self):
        #print(self.arr)
        return self.arr
    def setMyArray(self, myArray2):
        self.arr = myArray2
    def getMyArray(self):
        return self.arr
a = Set([1,2,3,4,5])
#print(a.getMyArray())
#print(type(a.arr))
#print(a.display())
#a.setMyArray([0,88])
#print(a.getMyArray())
#a.display()



class Interval:
    def __init__(self, a, b, isOpen):
        self.a = a
        self.b = b
        self.isOpen = isOpen
    def ReturnSet(self, order) :
        sett = []
        i=self.a
        if(self.isOpen):
            while(i<(self.b-2*order)):
                i+=order
                sett.append(i)
        else:
            while(i<(self.b+order)):
                sett.append(i)
                i+=order
        return Set(sett)
    
class Function:
    def __init__(self, MyFunction,  MyParams):
        self.MyFunction = MyFunction
        self.MyParams = MyParams
    def GetOutput(self):
        for i in Set(self.MyParams).display():
            if(self.MyFunction(i)==None):
                print(self.MyFunction(i))
            else:
                self.MyFunction(i)
i = Interval(0,9,False)
#i.ReturnSet(1).display()