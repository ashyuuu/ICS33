# Submitter: 13704695(Yu, Ashley)

#import prompt
#import goody

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    # reads the file and output in the desired dict format
    # {name : [ partner, [preferences] ] }
    match_preferences ={}

    for lines in open(open_file):
        match_preferences[lines.rstrip().split(';')[0]] = [None, lines.rstrip().split(';')[1:]]
    # print(match_preferences)
    return match_preferences


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    # returns multi-line string like reachable
    # key function assumes var to be a key in dict
    # similar to sorted
    ans=''
    
    for name in sorted(d,key=key,reverse=reverse):
        ans+='  '+name+' -> '+str(d[name])+'\n'

    return ans


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    # given the preference list order, determine who is prefered, p1 or p2?
    return p1 if order.index(p1) < order.index(p2) else p2


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    # returns set of tuples being a match between men in 0 and women in 1
    ans = set()
    for name in men:
        if men[name][0] != None:
            ans.add((name,men[name][0]))
    return ans


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    # returns set of tuples each has a match
    # Gale/Shapley algorithm

    final_match = set()

    # make a copy of men's data struct as back up for mutation
    men_backup = dict(men)

    # single men set = all men initially
    unmatched = list(men_backup.keys())
    if trace:
        print (f'Women Preferences (unchanging)\n{dict_as_str(women)}')

    # repeat until unmatched is empty
    while len(unmatched) != 0:
        if trace:
            print (f'Men Preferences (current)\n{dict_as_str(men_backup)}\nunmatched men =',set(unmatched),'\n')
        single=unmatched[0]
        unmatched.pop(0)
                
        # high_pref = his first choice
        high_pref = men_backup[single][1][0]
        # pop first choice from rest of prefs
        men_backup[single][1].pop(0)

        if women[high_pref][0] == None:
            # match them
            men_backup[single][0]=high_pref
            women[high_pref][0]=single
            if trace:
                print (single,'proposes to',high_pref,'(an unmatched woman); so she accepts the proposal')

        elif who_prefer(women[high_pref][1], women[high_pref][0], single) == single:
            # if prefer this man
            unmatched.append(women[high_pref][0])
            men_backup[women[high_pref][0]][0]=None
            men_backup[single][0]=high_pref
            women[high_pref][0]=single
            if trace:
                print (single,'proposes to',high_pref,'(a matched woman); she prefers her new match, so she accepts the proposal')
                
        elif who_prefer(women[high_pref][1], women[high_pref][0], single) == women[high_pref][0]:
            # if prefer current
            unmatched.append(single)
            if trace:
                print (single,'proposes to',high_pref,'(a matched woman); she prefers her current match, so she rejects the proposal')

            
    return extract_matches(men_backup) 


  
    
if __name__ == '__main__':
    # Write script here
    men = input('Input the file name detailing the preferences for men: ')
    women = input('Input the file name detailing the preferences for women: ')
    m_match_pref = read_match_preferences(men)
    w_match_pref = read_match_preferences(women)

    print('\nMen Preferences')
    for lines in dict_as_str(m_match_pref).split('\n'):
        print(lines)

    print('\nWomen Preferences')
    for lines in dict_as_str(w_match_pref).split('\n'):
        print(lines)
    
    t = input('\nInput tracing algorithm option[True]: ')
    trace = True if t == 'True' else False

    print('\nThe final matches =', make_match(m_match_pref,w_match_pref,trace))
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
    #driver.default_show_traceback = True
    #driver.default_show_exception = True
    #driver.default_show_exception_message = True
    #driver.driver()
