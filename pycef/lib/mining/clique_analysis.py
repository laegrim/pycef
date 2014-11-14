# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 09:36:56 2013

@author: laegrim
"""

import sys
sys.path.append('/home/laegrim/pycef')
from pycef.lib.mongo.mongo_interface import Mongo
import heapq
from networkx.readwrite import json_graph
import networkx as nx
import time

def simple_enum_pseudo_clique(G,K,T,L):
    '''
    Based on algorithm by Takeaki Uno, in his paper 
    "An Efficient Algorithm for Enumerating Pseudo
    Cliques"
    
    The paper describes an adjacency relation on pseudo cliques:
    
        Given any maximal pseudo clique, removing a vertex with degree below
        or equal to the average vertex degree yeilds a child pseudo clique.
        Thus all maximal pseudo cliques can be found by traversing the tree 
        implied by this relationship in reverse (i.e. by taking an empty set, 
        and adding minimum degree vertices to that set to see if they form a 
        pseudo clique).
        
        Children are found in O(nlogn + |V||K|)
    
    Enumerates all pseudo cliques in a given graph:
    G: Non-directed Graph (Networkx Graph Object)
    K: Empty Non-directed Graph (Networkx Graph Object)
    T: Pseudo clique denisty threshold as a float
    L: List of pseudo cliques
    '''
        
    L.append(K.nodes())

    #For each vertex in G that is not in K
    for node in [vertex for vertex in G.nodes() if vertex not in K.nodes()]:
        #Add that node to K, (K' = K U {v})
        K.add_node(node)
        
        #Add associated edges between recently added none and
        #nodes already in K
        for other_node in K.nodes():
            if G.has_edge(other_node, node):
                K.add_edge(other_node, node)
        #An empty graph by definition is a pseudo clique
        #Find the density of K
        if K.nodes() == [] or density(K) >= T:
            #If K is dense enough, greater than threshold T,
            #then it is a pseudo clique
            #K.nodes() returns a list of nodes; altering it doesn't
            #alter K
            #To this end, we want a list of all the nodes in K that arn't
            #the current node
            index = K.nodes().index(node)
            parent_nodes_list = K.nodes().pop(index)
            #Grab the degrees of each node in the list
            degree_list = K.degree(parent_nodes_list)
            #if the list has one element, degrees returns an int;
            #account for this
            if type(degree_list) == int:
                degree_list = [degree_list]
            #By lemma, K' (The current K) is a child of K 
            #(the previous iteration K) if 
            #the current node is the smallest node in K'.  
            if ([degree for degree in degree_list if
                degree < K.degree(node)] == []):
                #print "K of length " + str(K.number_of_nodes()) +
                #" has child with member: " + node
                #Since K' is a child of K, then look for children of K
                simple_enum_pseudo_clique(G,K,T,L)
        #K was not a pseudo clique or K was not a child
        K.remove_node(node)
        

def simple_enum_pseudo_clique_no_repeat(G,K,T,L):
    '''
    Based on algorithm by Takeaki Uno, in his paper 
    "An Efficient Algorithm for Enumerating Pseudo
    Cliques"
    
    The paper describes an adjacency relation on pseudo cliques:
    
        Given any maximal pseudo clique, removing a vertex with degree below
        or equal to the average vertex degree yeilds a child pseudo clique.
        Thus all maximal pseudo cliques can be found by traversing the tree 
        implied by this relationship in reverse (i.e. by taking an empty set, 
        and adding minimum degree vertices to that set to see if they form a 
        pseudo clique).
        
        Children are found in O(nlogn + |V||K|)
    
    Enumerates all pseudo cliques in a given graph:
    G: Non-directed Graph (Networkx Graph Object)
    K: Empty Non-directed Graph (Networkx Graph Object)
    T: Pseudo clique denisty threshold as a float
    L: List of pseudo cliques
    '''
    
    L.sort(cmp=sort_by_len)
    [clique.sort() for clique in L]
    nodes_list = K.nodes()
    nodes_list.sort()
    if L.count(nodes_list) > 0 or nodes_list in L > 0:
        #print nodes_list
        return
    else:
        L.append(nodes_list)
#        with Mongo() as interface:
#            interface.push_to_mongo({'_id':'nodes_list', 'list':L},
#                                    'NodesList', 'List', {'_id':'nodes_list'})
        
    #For each vertex in G that is not in K
    for node in [vertex for vertex in G.nodes() if vertex not in K.nodes()]:
        #Add that node to K, (K' = K U {v})
        K.add_node(node)

        #Add associated edges between recently added none and
        #nodes already in K
        for other_node in K.nodes():
            if G.has_edge(other_node, node):
                K.add_edge(other_node, node)
        #An empty graph by definition is a pseudo clique
        #Find the density of K
        if K.nodes() == [] or density(K) >= T:
            #If K is dense enough, greater than threshold T,
            #then it is a pseudo clique
            #K.nodes() returns a list of nodes; altering it doesn't
            #alter K
            #To this end, we want a list of all the nodes in K that arn't
            #the current node
            index = K.nodes().index(node)
            parent_nodes_list = K.nodes().pop(index)
            #Grab the degrees of each node in the list
            degree_list = K.degree(parent_nodes_list)
            #if the list has one element, degrees returns an int;
            #account for this
            if type(degree_list) == int:
                degree_list = [degree_list]
            #By lemma, K' (The current K) is a child of K 
            #(the previous iteration K) if 
            #the current node is the smallest node in K'.  
            if ([degree for degree in degree_list if
                degree < K.degree(node)] == []):
                #print "K of length " + str(K.number_of_nodes()) +
                #" has child with member: " + node
                #Since K' is a child of K, then look for children of K
                simple_enum_pseudo_clique_no_repeat(G,K,T,L)
        #K was not a pseudo clique or K was not a child
        K.remove_node(node)
    
def enum_pseudo_cliques(G,K,T,L):
    '''
    Container for a pseudo clique enumeration function with some optimization
    '''
    
    sorted_G = {}
    for node in G.nodes():
        sorted_G[node] = 0
    sorted_K = []

    def find_pseudo_cliques(G,K,T,L,P,Q):
        '''
        Based on algorithm by Takeaki Uno, in his paper 
        "An Efficient Algorithm for Enumerating Pseudo
        Cliques"
        
        The paper describes an adjacency relation on pseudo cliques:
        
            Given any maximal pseudo clique, removing a vertex with degree
            below or equal to the average vertex degree yeilds a child pseudo
            clique.Thus all maximal pseudo cliques can be found by traversing
            the tree implied by this relationship in reverse (i.e. by taking an
            empty set, and adding minimum degree vertices to that set to see if
            they form a pseudo clique).
            
            Optimized to find children of a given pseudo clique in O(V)
        
        Enumerates all pseudo cliques in a given graph:
        G: Non-directed Graph (Networkx Graph Object)
        K: Empty Non-directed Graph (Networkx Graph Object)
        T: Pseudo clique denisty threshold as a float
        L: List of pseudo cliques
        P: sorted list of nodes in G, ordered by <(k)
        Q: sorted list of first delta nodes in K, ordered by <(k), where delta
        is the difference in number of nodes between G and K.  If delta
        is larger than K, then Q contains all elements of K.
        '''
        
        #If the algorithm just started there won't be any nodes in K or 
        #Q.  In this case, for every node v in G: 1) K U {v} is a pseudo clique
        #by definition and 2) v <(k) v*(K) by definition.  Thus every node in G
        #when K is empty is a child clique
        
        #P and Q contain ordered lists using ordering <(k). Given that the 
        #first element in both lists is the element with the lowest order,
        #and that in order to be a chld node, v in G must meet 1) K U {v} is a 
        #psedo cliqe and 2) v <(k) v*(K), if the fist element of P has lower 
        #than the first element of Q, then no v in P can satisfy the 
        #requirements to make K` = K U {v} a child of K. Additionally, if the
        #last element of P does not satisfy deg(k)(v) > T(K), then no element 
        #v in P can satisfy the requirements to make K` a child either.  Using 
        #a heap to order P yeilds O(log|V|) search for elements v where 
        #K U {v} is a pseudo clique and v <(k) v*(K).
        
        if density(K) < T:
            print "not a pseudo clique...."
        threshold_K = threshold(K, T)
        L.append(K.nodes())
        
        #If there are no nodes in Q, start from the begining
        if Q == []:
            for node in G:
                #add a node
                K.add_node(node)
                #append the node to Q and remove it from P
                heapq.heappush(Q,{'node':node, 'degree(k)':0})
                P.pop(node)
                for neighbor_v in G[node]:
                    P[neighbor_v] += 1
                #start the recursion
                find_pseudo_cliques(G,K,T,L,P,Q)
                #when returning, put things back the way they were
                P[node] = 0
                for neighbor_v in G[node]:
                    P[neighbor_v] = 0
                Q.pop()
                K.remove_node(node)
                
        else:
            diff = min(len(Q), abs(len(P) - len(Q)))

            #only need to do the first few
            for i in range(diff):
                #look at each neighbor of u in Q
                for neighbor in [node for node in G[Q[i]['node']] if node in P]:
                    #if K U {v} is a pseudo clique and v*(K) <(k) v and 
                    #v <(k) l(v,K) then v K U {v} is a child
                    n_deg = P[neighbor]
                    min_deg = Q[0]['degree(k)']
                    min_name = Q[0]['node']
                    lesser = less(neighbor, G, Q)
                    #nasty compound if to check for the above
                    if ((min_deg < n_deg or (min_deg == n_deg and
                        min_name <= neighbor)) and 
                        n_deg >= threshold_K and 
                        (n_deg < lesser['degree(k)'] or 
                        (n_deg == lesser['degree(k)'] and 
                        neighbor <= lesser['node']))):         
                        #given that K U {v} is a child, then recurse
                        #add v to k
                        K.add_node(neighbor)
                        #get all the appropriate edges
                        for other_node in K:
                            if G.has_edge(other_node, neighbor):
                                K.add_edge(other_node, neighbor)
                                
                        #pop neighbor from P
                        P.pop(neighbor)
                        #update degree K for nodes in P
                        for neighbor_v in G[neighbor]:
                            if P.has_key(neighbor_v):
                                P[neighbor_v] += 1
                                
                        #update degree Q for nodes in Q
                        Q = [{'node':node, 'degree(k)':len(K[node])} for node
                            in K]
                            
                        heapq.heapify(Q)
                        
                        #call new iter
                        find_pseudo_cliques(G,K,T,L,P,Q)
                        
                        #replace values for P and Q
                        P[neighbor] = degree_K(G,K,neighbor)
                        for neighbor_v in G[neighbor]:
                            if P.has_key(neighbor_v):
                                P[neighbor_v] -= 1
                                
                        K.remove_node(neighbor)
                        
                        Q = [{'node':node, 'degree(k)':len(K[node])} for node
                            in K]
                            
                        heapq.heapify(Q)
                        
    find_pseudo_cliques(G,K,T,L,sorted_G,sorted_K)
    
def enum_pseudo_cliques_no_repeat(G,K,T,L):
    '''
    Container for a pseudo clique enumeration function with some optimization
    '''
    
    sorted_G = {}
    for node in G.nodes():
        sorted_G[node] = 0
    sorted_K = []

    def find_pseudo_cliques_no_repeat(G,K,T,L,P,Q):
        '''
        Based on algorithm by Takeaki Uno, in his paper 
        "An Efficient Algorithm for Enumerating Pseudo
        Cliques"
        
        The paper describes an adjacency relation on pseudo cliques:
        
            Given any maximal pseudo clique, removing a vertex with degree
            below or equal to the average vertex degree yeilds a child pseudo
            clique.Thus all maximal pseudo cliques can be found by traversing
            the tree implied by this relationship in reverse (i.e. by taking an
            empty set, and adding minimum degree vertices to that set to see if
            they form a pseudo clique).
            
            Optimized to find children of a given pseudo clique in O(V)
        
        Enumerates all pseudo cliques in a given graph:
        G: Non-directed Graph (Networkx Graph Object)
        K: Empty Non-directed Graph (Networkx Graph Object)
        T: Pseudo clique denisty threshold as a float
        L: List of pseudo cliques
        P: sorted list of nodes in G, ordered by <(k)
        Q: sorted list of first delta nodes in K, ordered by <(k), where delta
        is the difference in number of nodes between G and K.  If delta
        is larger than K, then Q contains all elements of K.
        '''
        
        #If the algorithm just started there won't be any nodes in K or 
        #Q.  In this case, for every node v in G: 1) K U {v} is a pseudo clique
        #by definition and 2) v <(k) v*(K) by definition.  Thus every node in G
        #when K is empty is a child clique
        
        #P and Q contain ordered lists using ordering <(k). Given that the 
        #first element in both lists is the element with the lowest order,
        #and that in order to be a chld node, v in G must meet 1) K U {v} is a 
        #psedo cliqe and 2) v <(k) v*(K), if the fist element of P has lower 
        #than the first element of Q, then no v in P can satisfy the 
        #requirements to make K` = K U {v} a child of K. Additionally, if the
        #last element of P does not satisfy deg(k)(v) > T(K), then no element 
        #v in P can satisfy the requirements to make K` a child either.  Using 
        #a heap to order P yeilds O(log|V|) search for elements v where 
        #K U {v} is a pseudo clique and v <(k) v*(K).
        
        if density(K) < T:
            print "not a pseudo clique...."
        threshold_K = threshold(K, T)
        L.sort(cmp=sort_by_len)
        [clique.sort() for clique in L]
        nodes_list = K.nodes()
        nodes_list.sort()
        if L.count(nodes_list) > 0 or nodes_list in L > 0:
            #print nodes_list
            return
        else:
            L.append(nodes_list)
#            with Mongo() as interface:
#                interface.push_to_mongo({'_id':'nodes_list', 'list':L},
#                                    'NodesList', 'List', {'_id':'nodes_list'})        
        #If there are no nodes in Q, start from the begining
        if Q == []:
            for node in G:
                #add a node
                K.add_node(node)
                #append the node to Q and remove it from P
                heapq.heappush(Q,{'node':node, 'degree(k)':0})
                P.pop(node)
                for neighbor_v in G[node]:
                    P[neighbor_v] += 1
                #start the recursion
                find_pseudo_cliques_no_repeat(G,K,T,L,P,Q)
                #when returning, put things back the way they were
                P[node] = 0
                for neighbor_v in G[node]:
                    P[neighbor_v] = 0
                Q.pop()
                K.remove_node(node)
                
        else:
            diff = min(len(Q), abs(len(P) - len(Q)))

            #only need to do the first few
            for i in range(diff):
                #look at each neighbor of u in Q
                for neighbor in [node for node in G[Q[i]['node']] if node in P]:
                    #if K U {v} is a pseudo clique and v*(K) <(k) v and 
                    #v <(k) l(v,K) then v K U {v} is a child
                    n_deg = P[neighbor]
                    min_deg = Q[0]['degree(k)']
                    min_name = Q[0]['node']
                    lesser = less(neighbor, G, Q)
                    #nasty compound if to check for the above
                    if ((min_deg < n_deg or (min_deg == n_deg and
                        min_name <= neighbor)) and 
                        n_deg >= threshold_K and 
                        (n_deg < lesser['degree(k)'] or 
                        (n_deg == lesser['degree(k)'] and 
                        neighbor <= lesser['node']))):         
                        #given that K U {v} is a child, then recurse
                        #add v to k
                        K.add_node(neighbor)
                        #get all the appropriate edges
                        for other_node in K:
                            if G.has_edge(other_node, neighbor):
                                K.add_edge(other_node, neighbor)
                                
                        #pop neighbor from P
                        P.pop(neighbor)
                        #update degree K for nodes in P
                        for neighbor_v in G[neighbor]:
                            if P.has_key(neighbor_v):
                                P[neighbor_v] += 1
                                
                        #update degree Q for nodes in Q
                        Q = [{'node':node, 'degree(k)':len(K[node])} for node
                            in K]
                            
                        heapq.heapify(Q)
                        
                        #call new iter
                        find_pseudo_cliques_no_repeat(G,K,T,L,P,Q)
                        
                        #replace values for P and Q
                        P[neighbor] = degree_K(G,K,neighbor)
                        for neighbor_v in G[neighbor]:
                            if P.has_key(neighbor_v):
                                P[neighbor_v] -= 1
                                
                        K.remove_node(neighbor)
                        
                        Q = [{'node':node, 'degree(k)':len(K[node])} for node
                            in K]
                            
                        heapq.heapify(Q)
                        
    find_pseudo_cliques_no_repeat(G,K,T,L,sorted_G,sorted_K)
    
def less(v, G, Q):
    '''
    Returns the node of least order in graph K not adjacent to v.  If all nodes
    in K are adjacent to v, then returns high value.
    '''
    
    for node in Q:
        if not G.has_edge(v, node['node']):
            return node
    return {'node':'temp', 'degree(k)':1000000000}
    
def degree_K(G,K,v):
    '''
    Returns the number of adjecent nodes between v in G and not in K and nodes
    in K
    '''
    i = 0
    neighbors = G[v]
    for neighbor in neighbors:
        if neighbor in K:
            i += 1
    return i
    
def threshold(K,T):
    '''
    Returns the threshold for which a node v must have degree(k) greater than
    or equal to for K U {v} to be a pseudo clique
    '''
    order = K.order()
    return T * ((order + 1) * order)/2 - K.number_of_edges()
    
def orderK(v1,v2):
    '''
    Used for sort functionality, returns v1 <(k) v2 if 
    degree(k)(v1) < degree(k)(v2) or (degree(k)(v1) == degree(k)(v2) and 
    v1 <= v2 where <= compares the two node's indexes in P, the sorted list
    of nodes in G)
    
    each vertex must contain information about it's degree(k) and index in P
    '''
    
    if v1['degree(k)'] < v2['degree(k)']:
        return 1
    elif v1['degree(k)'] == v2['degree(k)']:
        return 0
    else:
        return -1
        
def density(G):
    '''
    Returns the edge density of given graph G
    '''
    #edge density is defined as the number of edges in G over the total
    #possible number of edges in G
    #Calculate the maximum number of edges
    order = G.order()
    max_edges = (order * (order -1))/2
    #By definition, a graph of order 0 or 1 has a density of 1
    if max_edges == 0:
        return 1
    else:
        return float(G.number_of_edges()) / max_edges
        
def sort_by_len(l1, l2):
    '''
    sort by longest list
    '''
    if len(l1) < len(l2):
        return 1
    elif len(l2) < len(l1):
        return -1
    else:
        return 0
        
def find_interesting_keywords(graph, cliques_list, pageranks, keyword_list,
                              view_threshold, bid_threshold,
                              distance_threshold, pageranks_cutoff):
    
    interesting_keywords = []
    #traverse the pageranks list
    for page in pageranks:
        #find the keywords in the keyword list that match a keyword in the
        #pagerank list
        keyword = [keyword for keyword in keywords_list if
                    keyword[0] == page[0]][0]
        #make sure all of the information is there
        if len(keyword) != 5:
            print "Not All There!"
            print keyword[0]
            continue
        # sort by keywords that match up to the thresholds
        if (int(keyword[1]) > view_threshold and
            float(keyword[3].strip('$')) < bid_threshold):
            # If the current keyword is within distance 3 of a clique member
            if [clique for clique in cliques_list if
                [word for word in clique if (len(
                nx.shortest_path(word, keyword)) -1) >= distance_threshold]
                != [] ] != []: 
                interesting_keywords.append((keyword, page[1]))
                print keyword[0] + ', ' + keyword[1] + ', ' + keyword[3]
                
#G = json_graph.load(open('/home/laegrim/pycef/pycef/visualizations/exp.json'))
#K = nx.Graph()
#T = .9
#
#L = []
#total = 0
#for i in range(6):
#    
#    
#    L = []
#
#    start = time.time()
#    simple_enum_pseudo_clique_no_repeat(G,K,T,L)
#    end = time.time()
#    total += end - start
#    print "finished"
#
#print "Average Time: " + str(total/6.0)
#
#total = 0
#M = []
#for i in range(6):
#    
#    M = []
#    start = time.time()
#    enum_pseudo_cliques(G,K,T,M)
#    end = time.time()
#    total += end - start
#    
#    print "finished"
#
#print "Average Time: " + str(total/6.0)
#
#
#total = 0
#N = []
#for i in range(6):
#    
#    N = []
#
#    start = time.time()
#    enum_pseudo_cliques_no_repeat(G,K,T,N)
#    end = time.time()
#    total += end - start
#    print "finished"
#
#print "Average Time: " + str(total/6.0)
#
#print "finished"