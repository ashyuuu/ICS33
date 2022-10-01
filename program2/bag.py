from collections import defaultdict
from goody import type_as_str
import prompt
from builtins import StopIteration
#from builtins import False

class Bag:
    def __init__(self, v = []):
        self.val={}
        for i in v:
            if i not in self.val.keys():
                self.val[i]=0
            self.val[i]+= 1
        
    def __repr__(self) -> str:
        ans = []
        for k in self.val:
            for j in range(self.val[k]):
                ans.append(k)
        return 'Bag('+str(ans) + ')'

    def __str__(self) -> str:
        return 'Bag('+','.join(str(k+'['+str(self.val[k])+']') for k in self.val) +')'
    
    def __len__(self) -> int:
        return sum(self.val[k] for k in self.val)
    
    def unique(self) -> int:
        return len(self.val.keys())
    
    def __contains__(self,arg) -> bool: 
        return arg in self.val.keys()
    
    def count(self,arg) -> int:
        return self.val[arg] if arg in self else 0
    
    def add(self,arg):
        self.val[arg] = self.val[arg]+1 if arg in self else 1
        
    def __add__(self, bag1):
        if type(bag1) != Bag:
            raise TypeError
        bag3 = Bag(repr(bag1)[5:len(repr(bag1))-2].split(','))
        for n in repr(self)[5:len(repr(self))-2].split(','):
            bag3.add(n) 
        return bag3
    
    def remove(self,arg):
        if arg not in self.val.keys():
            raise ValueError
        self.val[arg]-=1
        if self.val[arg]<=0:
            self.val.pop(arg) 
            
    def __eq__(self,bag2):
        return True if type(bag2) is Bag and self.val==bag2.val else False
    
    def __iter__(self):
        self.n = ''
        for a in self.val:
            for i in range(self.val[a]):
                self.n += a
        return iter(self.n)
    

            
if __name__ == '__main__':
    
    #Simple tests before running driver
    #Put your own test code here to test Bag before doing the bsc tests
    #Debugging problems with these tests is simpler

    b = Bag(['d','a','d','b','c','b','d'])
    print(repr(b))
    print(str(b))
    print(all((repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())))
    for i in b:
       print(i)

    b2 = Bag(['a','a','b','x','d'])
    print(repr(b2+b2))
    print(str(b2+b2))
    print([repr(b2+b2).count('\''+v+'\'') for v in 'abdx'])
    b = Bag(['a','b','a'])
    print(repr(b))
    print()
    
    import driver
    driver.default_file_name = 'bscp21S21.txt'
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
