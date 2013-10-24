# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 09:36:56 2013

@author: laegrim
"""
import sys
from pycef.lib.mongo.mongo_interface import Mongo
import heapq

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
    #Sort L so that duplication can be checked
    #If the current pseudo clique is a duplicate
    #We can exit early, else
    #Append the most recent pesudo clique to L
#    L.sort(cmp=sort_by_len)
#    [clique.sort() for clique in L]
#    nodes_list = K.nodes()
#    nodes_list.sort()
#    if L.count(nodes_list) > 0 or nodes_list in L > 0:
#        print nodes_list
#        return
#    else:
#        L.append(nodes_list)
#        with Mongo() as interface:
#            interface.push_to_mongo({'_id':'nodes_list', 'list':L},
#                                    'NodesList', 'List', {'_id':'nodes_list'})
        
    L.append(K.nodes())

    #For each vertex in G that is not in K
    for node in [vertex for vertex in G.nodes() if vertex not in K.nodes()]:
        #Add that node to K, (K' = K U {v})
        K.add_node(node)
#        
#        if K.nodes() in L:
#            K.remove_node(node)
#            continue
        
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
                enum_pseudo_clique(G,K,T,L)
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
    #Sort L so that duplication can be checked
    #If the current pseudo clique is a duplicate
    #We can exit early, else
    #Append the most recent pesudo clique to L
    L.sort(cmp=sort_by_len)
    [clique.sort() for clique in L]
    nodes_list = K.nodes()
    nodes_list.sort()
    if L.count(nodes_list) > 0 or nodes_list in L > 0:
        print nodes_list
        return
    else:
        L.append(nodes_list)
        with Mongo() as interface:
            interface.push_to_mongo({'_id':'nodes_list', 'list':L},
                                    'NodesList', 'List', {'_id':'nodes_list'})
        
    #L.append(nodes_list)

    #For each vertex in G that is not in K
    for node in [vertex for vertex in G.nodes() if vertex not in K.nodes()]:
        #Add that node to K, (K' = K U {v})
        K.add_node(node)
#        
#        if K.nodes() in L:
#            K.remove_node(node)
#            continue
        
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
                enum_pseudo_clique(G,K,T,L)
        #K was not a pseudo clique or K was not a child
        K.remove_node(node)
        

def enum_pseudo_cliques(G,K,T,L):
    '''
    Container for a pseudo clique enumeration function with some optimization
    '''
    
    sorted_G = [{'degree(k)':0, 'node':node) for node in G.nodes()]
    sorted_G = heapq.heapify(sorted_G)
    sorted_K = []
    sorted_k = heapq.heapify(sorted_K)
    find_pseudo_cliques(G,K,T,L,sorted_G,sorted_K)

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
        is the difference in number of nodes between G and K.  If the 
        is larger than K, then Q contains all elements of K.
        '''
    
        #Output K
        L.append(K.nodes())
        
        #If the algorithm just started there won't be any nodes in K or 
        #Q.  In this case, for every node v in G: 1) K U {v} is a pseudo clique
        #by definition and 2) v <(k) v*(K) by definition.  Thus every node in G
        #when K is empty is a child clique
        
        #P and Q contain ordered lists using ordering <(k). Given that the 
        #first element in both lists is the lement with the lowest order,
        #and that in order to be a chld node, v in G must meet 1) K U {v} is a 
        #psedo cliqe and 2) v <(k) v*(K), if the fist element of P has lower 
        #than the first element of Q, then no v in P can satisfy the 
        #requirements to make K` = K U {v} a child of K. Additionally, if the
        #last element of P does not satisfy deg(k)(v) > T(K), then no element 
        #v in P can satisfy the requirements to make K` a child either.  Using 
        #a heap to order P yeilds O(log|V|) search for elements v where 
        #K U {v} is a pseudo clique and v <(k) v*(K).
        threshold_K = threshold(K,T)  
        
        #if the first two are not met, there can be no children
        if not order(P,P[0],Q[0]):
            return
        elif not heapq.nlargest(1, P)[0]['degree(k)'] >= threshold_K:
            return
        #find the first element that
        else
            
        #P and Q contain ordered lists using ordering <(k). child elements can 
        #be found by traversing the vertices in Q, which are ordered, and
        #for each u in Q, looking at the neighbors of u.  In this way l(v,k), 
        #where l(v,K) --> (the the first element in Q not adjacent to v: if
        # all elements in Q are adjacent to v, l(v,k) is infinite), can be 
        #computed for each v in G adjacent to at least on u in Q.  Since this
        #operation takes O(delta ** 2) in the worst case, and O(|V|+|E|) in the
        #best case, and if a v satisfies K U {v} is a pseudo clique and 
        #v*(K) <(k) v, then all v where v <(k) l(v,k) satisfy K U {v} is a 
        #child and all children may be found in O(min{delta ** 2, |V| + |E|}).
    
    
def degree_K(G,K,v):
    '''
    Returns the number of adjecent nodes between v in G and not in K and nodes
    in K
    '''
    i = 0
    neighbors = G.neighbors(v)
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