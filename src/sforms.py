import paradigm
from collections import defaultdict
import sys

def ralign(ss):
    m = max([len(s) for s in ss])
    return [(1+m-len(s))*' '+s for s in ss]

def lalign(ss):
    m = max([len(s) for s in ss])
    return [(s+(1+m-len(s))*' ') for s in ss]

ps = paradigm.load_file(sys.argv[1])

pss = [(n,c, p.p_forms(), ' '.join(['[%s]' % ",".join(list(set(s.members()))[:5]) for s in p.slots() if s.is_var()])) for (c,n,p) in ps]
result = defaultdict(set)

for (n1,c,fs,s) in pss:
    for (f,wf) in fs:
        result[f].add((c,n1, wf, s))

result = [(len(xs),f,xs) for (f,xs) in result.iteritems()]
result.sort(reverse=True)

for (n,f,xs) in result:
      if len(xs) > 1:
        xs = sorted(xs,reverse=True)
        wfs = ralign([x[2] for x in xs])
        lms = lalign(['p_%s %d' % (x[1],x[0]) for x in xs])
        sls = [x[3] for x in xs]
        print ((len(wfs[0])+len(lms[0]) - len(f)-3)*' ' + '=> %s <=' % f).encode('utf-8')
        for t in zip(lms,wfs,sls):
            print ('%s%s  %s' % t).encode('utf-8')
        print


