# Submitter: 13704695(Yu, Ashley)


#import goody
#import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    graph={}
    
    for lines in open(file):
        if lines.split(';')[0] not in graph.keys():
            graph[lines.split(';')[0]] = [lines.split(';')[1].rstrip()]
        else:
            graph[lines.split(';')[0]].append(lines.split(';')[1].rstrip())
            graph[lines.split(';')[0]] = sorted(graph[lines.split(';')[0]])
    #print(graph)
    return(dict(sorted(graph.items())))
    #return sorted(graph, key=lambda x:x)


def graph_as_str(graph : {str:{str}}) -> str:
    ans = ''
    for source_node in graph:
        ans += '  '+source_node+' -> '+str(graph[source_node])+'\n'
    return ans
        
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    # create a set of reached nodes
    # list of to be explored nodes
    reached = set()
    exploring = []
    exploring.extend(start)
    #reached.add(start)
    while not exploring == []:
        #print(trace)
        if trace:
            print(f'reached set    = {reached}')
            print(f'exploring list = {exploring}')
            print(f'transferring node {exploring[0]} from the exploring list to the reached set')
            print(f'after adding all nodes reachable directly from {exploring[0]} but not already in reached, exploring = ', end='')
        if not exploring[0] in reached:
            if exploring[0] in graph.keys(): 
                exploring.extend(graph[exploring[0]])
            reached.add(exploring[0])
        if exploring[0] in reached:
            exploring.pop(0)
        if trace:
            print(exploring,'\n')
    return reached

    

def print_sorted_nodes(graph : str) -> None:
    print('Graph: str (source node) -> [str] (sorted destination nodes)')
    print(graph)
    print()

if __name__ == '__main__':
    # Write script here
    
    # store file path 
    file_path = input('Input the file name detailing the graph: ')
    print()
    # define graph_dict as the dictionary representing the graph 
    # that is returned from read_path with the given file path
    graph_dict : {str:{str}} = read_graph(file_path)   
    # define sorted_nostes as the str that graph_as_str returns
    graph : str = graph_as_str(graph_dict)
    # print the graph out in the formatted way
    print_sorted_nodes(graph)
    
    # set input as a string to record the input response (node/invalid/done)
    start:str = ''
    init = True
    while (start!='done'):
        # update & check input
        start = input('Input one starting node (or input done): ')
        if start == 'done':
            break

        # while input is not done and is not an available starting node
        while start not in graph_dict.keys(): 
            # return error until proper starting node is given
            print(f'  Entry Error: \'{start}\';  Illegal: not a source node')
            print('  Print enter a legal String')
            start = input('Input one starting node (or input done): ')
            if start == 'done':
                break           
            
        t = input('Input tracing algorithm option[True]: ')
        trace = True if t == 'True' else False
        #print(type(trace))
        reachable_nodes=reachable(graph_dict,start,bool(trace))
        print(f'From the starting node {start}, its reachable nodes are {reachable_nodes}')
    
    
    
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
