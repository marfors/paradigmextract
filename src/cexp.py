# -*- coding: utf-8 -*-

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

total_number_of_words = float(sum([p.count for p in ps]))

for t in ds:
    w_result = (t[0],[])
    for p in ps:
        bf_match = p.match(t[0],[0])[0] # baseform match
        if bf_match == None:
            bf_match = p.match(t[0],[0],constrained=False)[0] 
        if bf_match != None:
                for (sc,bs) in bf_match[::-1]:
                    tlen = len(t)
                    correct = len([(w1,w2) for (w1,w2) in zip([w for (w,_) in p(*bs)],t) if w1 == w2])
                    w_result[1].append((sc, p.count/total_number_of_words, p.name, var_annot(bs), 100*float(correct)/tlen))
    w_result[1].sort(key=lambda res:(res[0],res[1]), reverse=True)
    if len(w_result[1]) > 0:
        acc = w_result[1][0][4]
    else:
        acc = 0.0
    exp.append((acc,w_result))

exp.sort(reverse=True)

form = 0
tot = 0
table = 0

for (acc,w_result) in exp:
        tot += 1
        form += acc
        found_paradigm = '   PARADIGM NOT FOUND\n'
        print ('%s\n   %.2f%s\t%s\t%s\t%d\t%d (%.2f%s)' % (w_result[0], acc,'%', w_result[1][0][2], w_result[1][0][3], w_result[1][0][0], w_result[1][0][1]*total_number_of_words,  w_result[1][0][1]*100,'%')).encode('utf-8')
        if int(acc) == 100:
                table += 1
                found_paradigm = ''
        else:
                for res in w_result[1][1:]:
                        print ('   %.2f%s\t%s\t%s\t%d\t%d (%.2f%s)' % (res[4],'%', res[2], res[3], res[0], res[1]*total_number_of_words, res[1]*100,'%')).encode('utf-8')
                        if int(res[4]) == 100:
                                found_paradigm = ''
                                break
        print found_paradigm
print '== result =='
print 'table: %.2f%s' % (100*float(table)/tot,'%')
print 'form: %.2f%s' % (form/tot,'%')
