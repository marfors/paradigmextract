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

exp = []

for t in ds:
    w_result = (t[0],[])
    for p in ps: 
        bf_match = p.match(t[0],[0])[0] # baseform match
        if bf_match == None: # unconstrained as fallback
            bf_match = p.match(t[0],[0],False)[0] 
        if bf_match != None:
                # print (' p_%s_%d' % (p.name, p.count)).encode('utf-8')
                for (sc,bs) in bf_match:
                    tlen = len(t)
                    if type(bs) == unicode:
                         bs = [bs]
                    correct = len([(w1,w2) for (w1,w2) in zip([w for (w,_) in p(*bs)],t) if w1 == w2])
                    w_result[1].append((sc, p.count, p.name, var_annot(bs), 100*float(correct)/tlen))
    w_result[1].sort(key=lambda res:(res[0], res[1]), reverse=True)
    if len(w_result[1]) > 0:
        acc = w_result[1][0][4]
    else:
        acc = 0
    exp.append((acc, w_result))

exp.sort(reverse=True)

form = 0
tot = 0
table = 0

for (acc, w_result) in exp:
        tot += 1
        form += acc
        if int(acc) == 100:
                table += 1
        print ('%s\t%d\t%s\t%s\t%d\t%d' % (w_result[0], acc, w_result[1][0][2], w_result[1][0][3], w_result[1][0][0], w_result[1][0][1])).encode('utf-8')
                
print 'table: %.1f%s' % (100*float(table)/tot,'%')
print 'form: %.1f%s' % (form/tot,'%')
