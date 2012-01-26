# -*- coding:utf-8 -*-

"""
  @brief Japanese WordNet Visualization by NetworkX
  @author Shintaro Takemura(stakemura@gmail.com)
 
  This code is public domain, no warranty expressed or implied, 
  Functionality is thought to be correct, but it's up to you to make
  sure it does what you want.
"""

import sys
if not hasattr(sys, "setdefaultencoding"):
    reload(sys)
sys.setdefaultencoding('utf-8')
    
import networkx as nx
import os
import sqlite3
from decimal import Decimal

# Open SQLite3 DB
def openSQLite3DB(file_path):
    db = sqlite3.connect(
        os.path.join(os.path.dirname(__file__), file_path),
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES )
    db.row_factory = sqlite3.Row
    return db

def name(word,lexid):
    if lexid:
        return word+"#"+str(lexid)
    return word

def expand_synset(synset,jpWN,options,G,level):
    level -= 1
    if level<0:
        return
    
    if options.lang:
        cur_neighbor = jpWN.execute("select word.lemma,sense.lexid from word,sense where sense.synset=? and word.wordid=sense.wordid and word.lang=?", (synset,options.lang))
    else:
        cur_neighbor = jpWN.execute("select word.lemma,sense.lexid from word,sense where sense.synset=? and word.wordid=sense.wordid", (synset,))
    for neighbor in cur_neighbor.fetchall():
        word = neighbor['lemma']
        if G.has_node(word):
            continue
        G.add_node(word, weight=1.0, kind="word")
        G.add_edge(synset, word)
        expand_word(word,jpWN,options,G,level)
    cur_neighbor.close()

def expand_word(word,jpWN,options,G,level):
    level -= 1
    if level<0:
        return

    cur_neighbor = jpWN.execute("select sense.synset,sense.lexid from word,sense where sense.wordid=word.wordid and word.lemma=?", (word,))
    for neighbor in cur_neighbor.fetchall():
        synset = neighbor['synset']
        if G.has_node(synset):
            continue
        G.add_node(synset, weight=2.0, kind="synset")
        G.add_edge(word, synset)
        expand_synset(synset,jpWN,options,G,level)
    cur_neighbor.close()

def main():
    from optparse import OptionParser

    parser = OptionParser()
    
    parser.add_option("-i", "--input", dest="dict",
      default="./wnjpn.db",
      help="Japanese WordNet DB path (default=./wnjpn.db)", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
      default="./wnjpn.graphml",
      help="output path (default==./wnjpn.png)", metavar="FILE")    
    parser.add_option("-d", "--dpi", dest="dpi",
      default=100,
      help="dpi(default=100)")    

    parser.add_option("-l", "--lang", dest="lang",
      default="",
      help="language(eng or jpn, default=both)")
    parser.add_option("-r", "--level", dest="level",
      default=4,
      help="max recursive level(default=4)")    
    parser.add_option("-w", "--word", dest="word",
      default=u"network",
      help="word (e.g. network)")
    parser.add_option("-y", "--synset", dest="synset",
#      default="01586752-a",
      help="synset (e.g. 01586752-a)")
        
    options, args = parser.parse_args()
    
    filename, ext = os.path.splitext(options.output)    

    try:
        jpWN = openSQLite3DB(options.dict)
        
        G=nx.Graph()
        
        if options.synset:
            G.add_node(options.synset, weight=2.0, kind="synset")
            expand_word(options.synset,jpWN,options,G,options.level)
            
        elif options.word:
            G.add_node(options.word, weight=2.0, kind="word")
            expand_word(options.word,jpWN,options,G,options.level)

        if ext==".gml":
            nx.write_gml(G,options.output)
        elif ext==".graphml":
            nx.write_graphml(G,options.output)
        elif ext==".dot":
            #nx.draw_graphviz(G)
            nx.write_dot(G,options.output)
        else:
            import matplotlib.pyplot as plt

            pos=nx.spring_layout(G,iterations=20) # positions for all nodes
            
            # nodes
            nlarge=[u for (u,d) in G.nodes(data=True) if d['kind']=='synset']
            nsmall=[u for (u,d) in G.nodes(data=True) if d['kind']=='word']
    
            nx.draw_networkx_nodes(G,pos,nodelist=nlarge,node_size=400,node_color="red",alpha=0.3,linewidths=0.5)
            nx.draw_networkx_nodes(G,pos,nodelist=nsmall,node_size=400,node_color="blue",alpha=0.3,linewidths=0.5)
            
            # edges            
            nx.draw_networkx_edges(G,pos,width=1,alpha=0.2)
                
            # labels
            nx.draw_networkx_labels(G,pos,font_size=10,font_family='Meiryo')
            
            plt.axis('off')
            plt.savefig(options.output, dpi=options.dpi)
            plt.show() # display
        
    except IOError, (errno, msg):
        print('except: Cannot open "%s"' % options.input)
        print('  errno: [%d] msg: [%s]' % (errno, msg))                


if __name__ == "__main__":
    main()