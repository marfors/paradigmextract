import codecs
import glob
import sys
import random
from collections import defaultdict

SEED = 17
random.seed(SEED)

def create_holes(l,t):
    num_of_holes = int(round(random.normalvariate(len(t)/2.0, len(t)/4.0)))
    num_of_holes = max(1, min(len(t)-1, num_of_holes))
    for i in random.sample(xrange(0,len(t)), num_of_holes):
        t[i] = ('@%s' % l,t[i][1])
    return (l,t)
    
def read_tables(file):
    tables = []
    table = []
    with codecs.open(file, encoding='utf-8') as f:
        new_lemma = True
        lemma = ''
        for l in f:
            s = l.strip()
            if len(s) > 0:
                (w,msd) = s.split('\t')
                if new_lemma:
                    (lemma,new_lemma) = (w,False) # first form in a table
                table.append((w,msd))
            else: # a blank line separates the tables
                new_lemma = True
                tables.append(create_holes(lemma,table))
                table = []
    return tables

if __name__ == '__main__':
    lang = sys.argv[1]
    for f in glob.glob('../data/' + lang + '*test.txt'):
        for (_,t) in read_tables(f):
            for (w,msd) in t:
                print '%s\t%s' % (w,msd)
            print

        
