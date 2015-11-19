import codecs
import glob
import sys
import random
from collections import defaultdict

SEED = 17
random.seed(SEED)

def create_holes(l,t):
    num_of_holes = int(round(random.normalvariate(len(t)/2.0, len(t)/4.0)))
    num_of_holes = max(1, min(len(t)-2, num_of_holes))
    for i in random.sample(xrange(2,len(t)), num_of_holes):
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

def hole_filename(f):
    xs = f.split('_')
    return "_".join([xs[0],xs[1],'h'] + xs[2:])
    
if __name__ == '__main__':
    for f in glob.glob('../data/*.txt'):
        if '_h_' not in f:
            with codecs.open(hole_filename(f), encoding='utf-8', mode='w') as fout:
                for (_,t) in read_tables(f):
                    for (w,msd) in t:
                        fout.write('%s\t%s\n' % (w,msd))
                    fout.write('\n')
