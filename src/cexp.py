import paradigm
from collections import defaultdict
import sys
import codecs

def var_annot(ss):
    if type(ss) == unicode:
        ss = [ss]
    return ",".join(['%s=%s' % (n,s) for (n,s) in enumerate(ss,1)])

def read_data(file):
    (data,table) = ([],[])
    with codecs.open(file,encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if len(l) > 0:
                table.append(l.split('\t')[0])
            else:
                data.append(table)
                table = []
    return data
     
ps = paradigm.load_file(sys.argv[1])
ds = read_data(sys.argv[2])

for t in ds:
    print ('=> %s <=' % t[0]).encode('utf-8')
    for p in ps: 
        bf_match = p.match(t[0],[0])[0] # baseform match
        if len(bf_match) > 0:
                print (' p_%s_%d' % (p.name, p.count)).encode('utf-8')
                for (sc,bs) in bf_match:
                    tlen = len(t)
                    if type(bs) == unicode:
                        bs = [bs]
                    incorrect = [(w1,w2) for (w1,w2) in zip([w for (w,_) in p(*bs)],t) if w1 != w2]
                    print ('   %s:%d [%.1f%s]' % (var_annot(bs), sc, 100*(float((tlen-len(incorrect)))/tlen), '%')).encode('utf-8')
    print
