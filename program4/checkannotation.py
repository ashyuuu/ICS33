from goody import type_as_str
import inspect
from types import LambdaType
import bag

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
       
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')


class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check,param,value,check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 



class Check_Annotation:
    # Begin by binding the class attribute to True allowing checking to occur
    #   (only if the object's attribute self._checking_on is also bound to True)
    checking_on  = True
  
    # To check the decorated function f, begin by binding self._checking_on to True
    def __init__(self, f):
        self._f = f
        self._checking_on = True

    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):
        
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)
        
        # Begin by comparing check's function annotation with its arguments
        if annot is None:
            pass
        #elif type(annot) == str: 
        #    sig = signature()
        #    eval(annot)
        #    try:
        #        except_to_raise = None
        #        if eval(annot):
        #            except_to_raise = AssertionError()
        #    except AssertionError as e:
        #        except_to_raise = AssertionError(e)
        #    except:
        #        except_to_raise = AssertionError()
        #    finally:
        #        if except_to_raise != None:
        #            raise except_to_raise
        elif isinstance(annot,type):
            if not isinstance(value,annot):
                raise AssertionError(f'\'{param}\' failed annotation check(wrong type): value = {value}\n  was type {type(value).__name__} ...should be type {annot.__name__}\n{check_history}')
        elif isinstance(annot,list) or isinstance(annot,tuple):
            if (isinstance(annot,list) and not isinstance(value,list)) or (isinstance(annot,tuple) and not isinstance(value, tuple)):
                raise AssertionError(f'\'{param}\' failed annotation check(wrong type): value = {value}\n  was type {type(value).__name__} ...should be type {type(annot).__name__}')
            if len(annot) == 1:
                for e in value:
                    orig = check_history
                    check_history+=f'{type(annot).__name__}[{value.index(e)}] check: {annot[0]}\n'# if isinstance(annot, list) else f'tuple[{value.index(e)}] check: {annot[0]}\n'
                    self.check(param,annot[0],e,check_history)
                    check_history=orig
            elif len(value) != len(annot):
                raise AssertionError(f'\'{param}\' failed annotation check(wrong number of elements): value = {value}\n  annotation had {len(annot)} elements{annot}\n{check_history}')
            else:
                for e in range(len(value)):
                    orig = check_history
                    check_history+=f'{type(annot).__name__}[{e}]] check: {annot[0]}\n'# if isinstance(annot, list) else f'tuple[{e}] check: {annot[0]}\n'
                    self.check(param,annot[e],value[e],check_history)
                    check_history=orig
        elif isinstance(annot, dict) or isinstance(annot, set) or isinstance(annot,frozenset):
            if (isinstance(annot,dict) and not isinstance(value,dict)) or (isinstance(annot,set) and not isinstance(value,set)) or (isinstance(annot,frozenset) and not isinstance(value,frozenset)):
                raise AssertionError(f'\'{param}\' failed annotation check(wrong type): value = {value}\n  was type {type(value).__name__} ...should be type {type(annot).__name__}')
            if len(annot) > 1:
                raise AssertionError(f'\'{param}\' annotation inconsistency: {type(annot).__name__} should have 1 item but had {len(value)}\n  annotation = {annot}')
            elif len(annot) == 1:
                if isinstance(annot,dict):
                    for k in value.keys():
                        orig = check_history
                        check_history+=f'{type(annot).__name__} key check: {list(annot.keys())[0]}\n'
                        self.check(param,list(annot.keys())[0],k,check_history)
                        check_history=orig
                    for v in value.values():
                        orig = check_history
                        check_history+=f'{type(annot).__name__} value check: {list(annot.values())[0]}\n'
                        self.check(param,list(annot.values())[0],v,check_history)
                        check_history=orig
                elif isinstance(annot, set) or isinstance(annot,frozenset):
                    for v in value:
                        orig = check_history
                        check_history+=f'{type(annot).__name__} value check: {min(annot)}\n'
                        self.check(param,min(annot),v,check_history)
                        check_history=orig
        # lambda
        elif inspect.isfunction(annot):
            if annot.__code__.co_argcount != 1:
                raise AssertionError(f'\'{param}\' annotation inconsistency: predicate should have 1 parameter but had {annot.__code__.co_argcount}\n  predicate = {annot}')            
            try:
                annot(value)            
            except Exception as e:
                raise AssertionError(f'\'{param}\' annotation predicate({annot}) raised exception\n  exception = {type(e).__name__}: {e}\n{check_history}')
            if not annot(value):                
                raise AssertionError(f'\'{param}\' failed annotation check: value = {value}\n  predicate = {annot}\n{check_history}')
        else:
            try:
                except_to_raise = None  
                annot.__check_annotation__(self.check,param,value,check_history)
            except AttributeError:
                except_to_raise = AssertionError(f'\'{param}\' annotation undecipherable: {annot}')
            except AssertionError as e:
                except_to_raise = AssertionError(e)
            except Exception as e:
                except_to_raise = AssertionError(e)
            finally:
                if except_to_raise != None:
                    raise except_to_raise
            
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        
        # Return the argument/parameter bindings in an OrderedDict (it's derived
        #   from a dict): bind the function header's parameters in its order
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if not (param.name in bound_f_signature.arguments):
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments

        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        a = param_arg_bindings()
        if not self._checking_on:
            return self._f(*args,**kargs)
        
        try:
            sig = inspect.signature(self._f)
            # For each found annotation, check it using the parameter's value
            for annot in a:
                self.check(annot,sig.parameters[annot].annotation,a[annot])
            # Compute/remember the value of the decorated function
            result = self._f(*args,**kargs)
            # If 'return' is in the annotation, check it
            if sig.return_annotation != inspect._empty:
                self.check('_return',sig.return_annotation,result)
            # Return the decorated answer
            return result
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
            #print(80*'-')
            #for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
            #    print(l.rstrip())
            #print(80*'-')
            raise




  
if __name__ == '__main__':     
    # an example of testing a simple annotation  
    #def f(x:int): pass
    #f = Check_Annotation(f)
    #f(3)
    #f('a')
    
    #def f(x:[int]): pass
    #f = Check_Annotation(f)
    #f({1,2})
    #f([1,'a'])
    
    #def f(x:[int,str]): pass
    #f = Check_Annotation(f)
    #f([1])
    #f([1,2])
    
    #print('no exception')
    #def f(x:[int,None]): pass
    #f([1,'a'])
    
    #print('no exception')
    #def f(x:[[str]]): pass
    #f = Check_Annotation(f)
    #f([['a','b'],['c','d']])
    #print('exception')
    #f([['a',2],['c','d']])
    #driver tests
    
    #def f(x:{str : int}): pass
    #f = Check_Annotation(f)
    #f(['a',0])
    
    #def f(x:{str : int}): pass
    #f= Check_Annotation(f)
    #f({1:0})
    #f({'a':'b'}) 
    
    #def f(x:[lambda x : isinstance(x,int) and x>0]): pass
    #def f(x : {Check_All_OK(str,lambda x : len(x)<=3):Check_Any_OK(str,int)}): pass
    #f= Check_Annotation(f)
    #f({'a' : 1, 'b': 1., 'c':'c'})
    
    #f([1,'a'])
    
    
    
    import driver
    driver.default_file_name = 'bscp4S21.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
