# Submitter: ashley5(Yu, Ashley)

import re, traceback, keyword
    
def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    def show_listing(s):
        for ln_number, text_of_ln in enumerate(s.split('\n'),1):     
            print(f' {ln_number: >3} {text_of_ln.rstrip()}')

    # put your code here    
    fields = []
    if type(field_names) == list:
        fields = field_names
    elif type(field_names) == str:
        fields = re.split("[\s|,]\s*,*",field_names)
    else:
        raise SyntaxError
    
    to_checks = [type_name]+fields
    for c in to_checks:
        if type(c) != str or not re.match(r"[A-Z|a-z]+[0-9|A-Z|a-z|_]*",c) or c in keyword.kwlist:
            raise SyntaxError
    
    # generates the init str to put into class_definition
    def gen_init():
        ans = '    def __init__(self'
        for j in fields:
            ans += ','+str(j)
            if j in defaults.keys():
                ans+='='+defaults[j]
        ans +='):\n'
        for j in fields:
            ans += '        self.'+j+' = '+j+'\n'
        return ans
    
    # generates the repr str 
    def gen_repr():
        ans = '    def __repr__(self):\n        return f\''+type_name+'('
        for i in fields:
            ans += f'{i}={{self.{i}}},'
        return ans[:-1]+')\''
    
    # generates the get str
    def gen_get():
        ans = ''
        for j in fields:
            ans +=f'\n    def get_{j}(self):\n        return self.{j}\n'
        return ans
    
    # generates the __getitem__ str
    def gen_getitem():
        ans = '    def __getitem__(self,index):\n'
        c = 0
        ans += '        if type(index) == int and index < len(self._fields):'
        for j in fields:
            if c==0:
                ans += f'\n            if index == {c}:\n                return self.get_{j}()'
            else:
                ans += f'\n            elif index == {c}:\n                return self.get_{j}()'   
            c+=1
        ans += '\n        elif type(index) == str and index in self._fields:'
        c=0
        for j in fields:
            if c == 0:
                ans += f'\n            if index == \'{j}\':\n                return self.get_{j}()'
            else:
                ans += f'\n            elif index == \'{j}\':\n                return self.get_{j}()'
        ans += '\n        else:\n            raise IndexError(\'Index number out of range or string not in field or index type is not str or int\')\n'
        return ans
    
    # generates the eq str
    def gen_eq():
        return ('    def __eq__(self,other):\n        if type(other) != type(self):\n            return False'+
               '\n        a=self._fields.copy()\n        for i in a:\n            if self[i] != other[i]:\n'+
               '                return False\n        return True\n')
        
    # generates the asdict str
    def gen_asdict():
        ans = '    def _asdict(self):\n        return {'
        for j in fields:
            ans+=f'\'{j}\':self.{j},'
        return ans[:-1] + '}\n'
    
    # generates the make str
    def gen_make():
        ans= f'    def _make(i):\n        return {type_name}('
        for j in range(len(fields)):
            ans +=f'i[{j}],'
        return ans[:-1]+')\n'
    
    # generates the _replace str
    def gen_repl():
        ans = ('    def _replace(self,**kargs):\n        for i in kargs:\n'+
              '            if i not in self._fields:\n                raise TypeError\n        if self._mutable:\n')
        for j in fields:
            ans+=f'            if \'{j}\' in kargs:\n                self.{j}=kargs[\'{j}\']\n'
        return (ans+'        else:\n            b={}\n            for j in self._fields:\n'+
                '                b[j]=self[j]\n            for a in kargs:\n                if a in b.keys():\n'+
              f'                    b[a]=kargs[a]\n            return {type_name}._make(list(b.values()))\n')
        
    def gen_setattr():
        return (f'    def __setattr__(self,n,v):\n        if (not self._mutable and not hasattr(self,n)) '+
                'or self._mutable:\n'+'            super().__setattr__(n,v)\n        else:'+
                '\n            raise AttributeError(\'{type_name} is not mutable\')\n')

        
    # bind class_definition (used below) to the string constructed for the class
    class_definition = (f"\nclass {type_name}:\n    _fields = {fields}\n    _mutable = {mutable}"+
                        f"\n{gen_init()}\n{gen_repr()}\n{gen_get()}\n{gen_getitem()}"+
                        f"\n{gen_eq()}\n{gen_asdict()}\n{gen_make()}\n{gen_repl()}\n{gen_setattr()}") 

    # Debugging aid: uncomment show_listing here so always display source code
    #show_listing(class_definition)
    
    # Execute class_definition's str inside name_space; followed by binding the
    #   attribute source_code to the class_definition; after the try/except then
    #   return the created class object; if any syntax errors occur, show the
    #   listing of the class and also show the error in the except clause
    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )              
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                  
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    # Test simple pnamedtuple below in script: Point=pnamedtuple('Point','x,y')

    #driver tests
    import driver  
    driver.default_file_name = 'bscp3S21.txt'
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
