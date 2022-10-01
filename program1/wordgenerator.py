# Submitter: 13704695 (Yu, Ashley)

#import goody
#from goody import irange
#import prompt
from random import choice


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    i = word_at_a_time(open(file))
    keys = [next(i),next(i)]
    ans = {}
    
    # repeatedly read the next word and store the value into corpus    
    for c in i:
        if tuple(keys) not in ans.keys():
            ans[tuple(keys)] = []
        if c not in ans[tuple(keys)]:
            ans[tuple(keys)].append(c)
        keys.pop(0)
        keys.append(c)
    return ans


def corpus_as_str(corpus : {(str):[str]}) -> str:
    ans = ''
    a = []
    for c in corpus:
        a.append(len(corpus[c]))
        ans += '  '+str(c)+' can be followed by any of '+str(corpus[c])+'\n'
    return ans+'min/max list lengths = ' + str(min(a))+'/'+str(max(a))+'\n'


def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    # Construct 2 lists initially storing start
    # a will always contain only most recent n words # to be tupled for dict
    # b will contain all generated words
    keys = start.copy()
    random_text = start.copy()
    
    # generate random next from corpus using choice from random module
    for c in range(int(count)):
        # choice returns random val from list to be added to a and b
        r_next = choice(corpus[tuple(keys)])
        keys.append(r_next)
        random_text.append(r_next)    
        # pop first in a 
        keys.pop(0)

    return random_text



        
if __name__ == '__main__':
    # Write script here
    os = input('Input an order statistic: ')
    file = input('Input the file name detailing the text to read: ')
    corpus = read_corpus(os,file)
    print('Corpus')
    print(corpus_as_str(corpus))
    print(f'\nInput {os} words at the start of the list')
    start=[]
    for a in range(int(os)):
        start.append(input(f'Input word {a}: '))
    count=input('Input # of words to append to the end of the list: ')
    print('Random text =',produce_text(corpus,start,count))
              
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    #driver.driver()
