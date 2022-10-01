# Submitter: 13704695 (Yu, Ashley)

# import goody


def read_fa(file : open) -> {str:{str:str}}:
    ans = {}
    for lines in open(file):
        a = {}
        for j in lines.rstrip().split(';')[1::2]:
            a[str(j)]=lines.rstrip().split(';')[lines.rstrip().split(';').index(j)+1]
        ans[lines.rstrip().split(';')[0]] = a

    return ans


def fa_as_str(fa : {str:{str:str}}) -> str:
    # sort transitions and input val
    ans = ''
    for trans in sorted(fa):
        ans +='  '+trans+' transitions: '
        a=[]
        for input_val in sorted(fa[trans]):
            a.append((input_val,fa[trans][input_val]))
        ans += str(a) +'\n'
            #+ dict(sorted(fa[trans].items(), key=lambda x:x[1])) + 
    return ans
    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    ans = [state]
    
    current_state = state
    # deteremine next_state
    # make a copy of inputs
    c_inputs = inputs.copy()
    
    # until c_inputs is empty
    while c_inputs != []:
        next_state = None if c_inputs[0] not in fa[current_state].keys() else fa[current_state][c_inputs[0]]
        ans.append((c_inputs[0],next_state))
        current_state=next_state
        c_inputs.pop(0)

    #print(ans)
    return ans
    

def interpret(fa_result : [None]) -> str:
    ans = 'Start state = ' + fa_result[0] + '\n'
    for e in fa_result[1:]:
        if e[1] == None:
            ans +='  Input = ' + e[0] + '; illegal input: simulation terminated' + '\n'
            return ans + 'Stop state = None'
        ans += '  Input = ' + e[0] + '; new state = ' + e[1] + '\n'
    return ans+'Stop state = ' + fa_result[len(fa_result)-1][1]

def read_file(file:open) -> [str]:
    a=[]
    for lines in open(file):
        a.append(lines.rstrip())
    return a


if __name__ == '__main__':
    # Write script here
    file = input('Input the file name detailing the Finite Automaton: ')
    fa_details = read_fa(file)
    #print(fa_details)

    print('\nThe details of the Finite Automaton')
    print(fa_as_str(fa_details))

    i = input('Input the file name detailing groups of start-states and their inputs: ')
    inputs = read_file(i)
    outputs = []
    for ins in inputs:
        outputs.append(process(fa_details, ins.rstrip().split(';')[0], ins.rstrip().split(';')[1:]))

    for out in outputs:
        print('\nFA: the trace from its start-state')
        print(interpret(out))
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    #driver.driver()
