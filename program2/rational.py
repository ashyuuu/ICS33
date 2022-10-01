from goody import irange, type_as_str
import math
from builtins import AssertionError

class Rational:
    @staticmethod
    # Called as Rational._gcd(...); no self parameter
    # Helper method computes the Greatest Common Divisor of x and y
    def _gcd(x : int, y : int) -> int:
        assert type(x) is int and type(y) is int and x >= 0 and y >= 0,\
          'Rational._gcd: x('+str(x)+') and y('+str(y)+') must be integers >= 0'
        while y != 0:
            x, y = y, x % y
        return x
    
    @staticmethod
    # Called as Rational._validate_arithmetic(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), lt (left type) and rt (right type)
    # An example call (from my __add__ method), which checks whether the type of
    #   right is a Rational or int is...
    # Rational._validate_arithmetic(right, {Rational,int},'+','Rational',type_as_str(right))
    def _validate_arithmetic(v : object, t : {type}, op : str, left_type : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unsupported operand type(s) for '+op+
                            ': \''+left_type+'\' and \''+right_type+'\'')        

    @staticmethod
    # Called as Rational._validate_relational(..); no self parameter
    # Helper method raises exception with appropriate message if type(v) is not
    #   in the set of types t; the message includes the values of the strings
    #   op (operator), and rt (right type)
    def _validate_relational(v : object, t : {type}, op : str, right_type : str):
        if type(v) not in t:
            raise TypeError('unorderable types: '+
                            'Rational() '+op+' '+right_type+'()') 
                   
   # Put all other methods here
    def __init__ (self, n = 0, d = 1):
        
        if type(n) != int or type(d) != int or d==0:
            print('Rational.__init__ numerator numerator or/and denominator is not int or denominator is 0')
            raise AssertionError
        
        self.num=(n//Rational._gcd(abs(n), abs(d)))*-1 if d<0 else n//Rational._gcd(abs(n), abs(d))
        self.denom = (d//Rational._gcd(abs(n), abs(d)))*-1 if d<0 else d//Rational._gcd(abs(n), abs(d))
        
    def __str__(self):
        return str(self.num)+'/'+str(self.denom)
    
    def __repr__(self):
        return 'Rational(' + str(self.num) +',' + str(self.denom) + ')'
    
    def __bool__(self):
        return False if self.num == 0 and self.denom == 1 else True
    
    def __getitem__(self, index):
        if (type(index)==int and index == 0) or (type(index)==str and index!='' and index.lower() in 'numerator'):
            return self.num         
        elif (type(index)==int and index == 1) or (type(index)==str and index !='' and index.lower() in 'denominator'):
            return self.denom
        raise TypeError 
    
    def __pos__(self):     
        return Rational(self.num,self.denom)    
    
    def __neg__(self):
        return Rational(-1*self.num,self.denom)
    
    def __abs__(self):
        return Rational(abs(self.num),self.denom)
    
    def __add__(self,rat):  
        Rational._validate_arithmetic(rat,{int,Rational},'+','Rational',type(rat))
        rat = Rational(rat,1) if type(rat) == int else rat 
        return Rational( self.num*rat.denom + rat.num*self.denom, self.denom*rat.denom) 
    
    def __radd__(self,a):
        Rational._validate_arithmetic(a,{int,Rational},'+',type(a),'Rational')       
        return self+a   
    
    def __sub__(self,rat):  
        Rational._validate_arithmetic(rat,{int,Rational},'-','Rational',type(rat))
        rat = Rational(rat,1) if type(rat) == int else rat 
        return Rational( self.num*rat.denom - rat.num*self.denom, self.denom*rat.denom) 
    
    def __rsub__(self,a):
        Rational._validate_arithmetic(a,{int,Rational},'-',type(a),'Rational')
        return -1*(self-a)
    
    def __mul__(self,rat):
        Rational._validate_arithmetic(rat,{int,Rational},'*','Rational',type(rat))
        rat = Rational(rat,1) if type(rat) == int else rat 
        return Rational( self.num*rat.num, self.denom*rat.denom) 
    
    def __rmul__(self,a):
        Rational._validate_arithmetic(a,{int,Rational},'*',type(a),'Rational')
        return self*a
    
    def __truediv__(self,rat):
        Rational._validate_arithmetic(rat,{int,Rational},'/','Rational',type(rat))
        rat = Rational(rat,1) if type(rat) == int else rat 
        return self * Rational(rat.denom,rat.num)
    
    def __rtruediv__(self,rat):
        Rational._validate_arithmetic(rat,{int,Rational},'/',type(rat),'Rational')
        rat = Rational(rat,1) if type(rat) == int else rat            
        return rat*Rational(self.denom,self.num)
    
    def __pow__(self,p):
        Rational._validate_arithmetic(p,{int},'**','Rational',type(p))
        return Rational (self.num**p, self.denom**p) if p > 0 else Rational (self.denom**abs(p),self.num**abs(p))  
    
    def __eq__(self,a):
        Rational._validate_relational(a,{int,Rational},'==',type(a))
        return True if (self/a).num == 1 and (self/a).denom ==1  else False
    
    def __ne__(self,a):
        Rational._validate_relational(a,{int,Rational},'!=',type(a))
        return False if (self/a).num == 1 and (self/a).denom ==1  else True
    
    def __lt__(self,a):
        Rational._validate_relational(a,{int,Rational},'<',type(a))
        return True if (self/a).num < (self/a).denom else False
    
    def __gt__(self,a):
        Rational._validate_relational(a,{int,Rational},'>',type(a))
        return True if (self/a).num > (self/a).denom else False
    
    def __le__(self,a):
        Rational._validate_relational(a,{int,Rational},'<=',type(a))
        return True if (self/a).num <= (self/a).denom else False
    
    def __ge__(self,a):
        Rational._validate_relational(a,{int,Rational},'>=',type(a))
        return True if (self/a).num >= (self/a).denom else False
    
    def __call__(self,dec:int):
        sign = '-' if self.num<0 else ''            
        return sign+str(self.num//self.denom)+'.'+str((self.num - (self.num//self.denom)*self.denom)*10**dec//self.denom)
        #return sign+str(self.num/self.denom)+'.'+str((self.num - (self.num/self.denom)*self.denom)*10**dec/self.denom)
    
    def __setattr__(self,att,val):
        if not hasattr(self,att) and (att=='num' or att=='denom'):
            super().__setattr__(att,val)
        else:
            raise NameError('Denominator and Numerator of a Rational cannot be changed. Other attribute may not be added.')

        
# e ~ 1/0! + 1/1! + 1/2! + 1/3! ... 1/n!
def compute_e(n):
    answer = Rational(1)
    for i in irange(1,n):
        answer += Rational(1,math.factorial(i))
    return answer

# Newton: pi = 6*arcsin(1/2); see the arcsin series at http://mathforum.org/library/drmath/view/54137.html
# Check your results at http://www.geom.uiuc.edu/~huberty/math5337/groupe/digits.html
#   also see http://www.numberworld.org/misc_runs/pi-5t/details.html
def compute_pi(n):
    def prod(r):
        answer = 1
        for i in r:
            answer *= i
        return answer
    
    answer = Rational(1,2)
    x      = Rational(1,2)
    for i in irange(1,n):
        big = 2*i+1
        answer += Rational(prod(range(1,big,2)),prod(range(2,big,2)))*x**big/big       
    return 6*answer


if __name__ == '__main__':
    #Simple tests before running driver

    x = Rational(8,29) 
    #print(x+x)
    #print(2*x)
    #print(x(30))
    
    print(compute_pi(15)(15))
    import driver    
    
    
    driver.default_file_name = 'bscp22S21.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    #driver.driver()
