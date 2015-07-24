import paradigm
from collections import defaultdict
import sys

ps = paradigm.load_file(sys.argv[1])

pss = [(n,p.p_forms()) for (_,n,p) in ps]
result = defaultdict(set)

for (n1,fs) in pss:
    for (f,str) in fs:
        result[f].add(str+'\t'+n1)

result = [(len(xs),f,xs) for (f,xs) in result.iteritems()]

result.sort(reverse=True)

for (c,f,xs) in result:
    if len(xs) > 1:
        print f.encode('utf-8')
        for x in xs:
            print ('   %s' % x).encode('utf-8')
        print

