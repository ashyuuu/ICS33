# Submitter: 13704695 (Yu, Ashley)

#import goody


def read_ndfa(file : open) -> {str:{str:{str}}}:
    ans = {}
    
    for lines in open(file):
        # each state corresponds to an inner dict
        ans[lines.rstrip().split(';')[0]]={}
        copy = lines.rstrip().split(';').copy()
        for i in lines.rstrip().split(';')[1::2]:
            # if new input add key
            if i not in ans[lines.rstrip().split(';')[0]].keys():
                ans[lines.rstrip().split(';')[0]][i] = set()
            ans[lines.rstrip().split(';')[0]][i].add(copy[copy.index(i)+1])
            copy=copy[2:]
    
    return ans


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    ans = ''
    print(ndfa)
    for key in sorted(ndfa):
        a = []
        for k in sorted(ndfa[key]):
            a.append( (k, sorted(ndfa[key][k]) ))
        ans += '  '+key+' transitions: ' + str(a) + '\n'
    
    return ans
       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    ans = [state]
    current_state = set([state])
    c_inputs = inputs.copy()

    while c_inputs != []:
        next_state = set()
        for c in current_state:
            if len(ndfa[c]) !=0 and c_inputs[0] in ndfa[c].keys(): 
                for s in ndfa[c][c_inputs[0]]:
                    next_state.add(s)
        ans.append( (c_inputs[0],next_state) )
        current_state=next_state
        c_inputs.pop(0)

    return ans


def interpret(result : [None]) -> str:
    ans = 'Start state = ' + result[0] + '\n'
    for e in result[1:]:
        ans += '  Input = '+e[0]+'; new possible states = ' + str(sorted(e[1])) + '\n'
    return ans+'Stop state(s) = '+str(sorted(result[len(result)-1][1]))+'\n'

def read_file(file:open) -> [str]:
    a=[]
    for lines in open(file):
        a.append(lines.rstrip())
    return a


if __name__ == '__main__':
    # Write script here
    file = input('Input the file name detailing the Non-Deterministic Finite Automaton: ')
    ndfa = read_ndfa(file)
    #print(ndfa)

    print('\nThe details of the Non-Deterministic Finite Automaton')
    print(ndfa_as_str(ndfa))

    i = input('Input the file name detailing groups of start-states and their inputs: ')
    inputs = read_file(i)
    outputs = []
    for ins in inputs:
        outputs.append(process(ndfa,ins.rstrip().split(';')[0], ins.rstrip().split(';')[1:]))
    for out in outputs:
        print('\nNDFA: the trace from its start-state')
        print(interpret(out))

    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    #driver.driver()
