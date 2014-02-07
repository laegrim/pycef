# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 09:36:07 2013

@author: laegrim
"""
from networkx import Graph
from numpy import corrcoef
from pycef.lib.analytics.fundamentals import polyfit_ratio

def build_graph_dummy(args):
    return args[0]
    
def build_propagation_graph(sequences, cor_threshold, best_fit_threshold):
    '''
    sequence should be a tupple (id, array)
    threshold should exist in [0,1]
    '''
    #list to hold tuple associations
    tups_list = []
    #for each sequence in sequences
    for sequence in sequences:
        #find the corrcoef in relation to all other sequences
        for sec in [o_sec for o_sec in sequences if o_sec != sequence]:
            #if correlated within threshold bounds, ensure not already in list
            cor = corrcoef(sequence[1], sec[1])[0,1]
            ratio = polyfit_ratio(sequence[1], sec[1])
            if cor <= cor_threshold and abs(1 - ratio) <= best_fit_threshold and ([tup for tup in tups_list if sequence[0] and sec[0] in tup] == []):
                #if not already in list, append (_id1, _id2, corrcoef) tuple
                tups_list.append((sequence[0], sec[0], {'weight':cor}))
    #build graph from association list
    graph = Graph()
    graph.add_edges_from(tups_list)
    #return graph
    return graph
    
def build_cluster_graph(sequences, threshold):
    '''
    sequence should be a tupple (id, array)
    threshold should exist in [0,1]
    '''
    #list to hold tuple associations
    tups_list = []
    #for each sequence in sequences
    for sequence in sequences:
        #find the corrcoef in relation to all other sequences
        for sec in [o_sec for o_sec in sequences if o_sec != sequence]:
            #if correlated within threshold bounds, ensure not already in list
            cor = corrcoef(sequence[1], sec[1])[0,1]
            if cor >= threshold and ([tup for tup in tups_list if sequence[0] and sec[0] in tup] == []):
                #if not already in list, append (_id1, _id2, corrcoef) tuple
                tups_list.append((sequence[0], sec[0], {'weight':cor}))
    #build graph from association list
    graph = Graph()
    graph.add_edges_from(tups_list)
    #return graph
    return graph