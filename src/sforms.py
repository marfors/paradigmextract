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

pss = [(n,p.p_forms(), ' '.join(['[%s]' % ",".join(list(set(s.members()))[:5]) for s in p.slots() if s.is_var()])) for (_,n,p) in ps]
result = defaultdict(set)

for (n1,fs,s) in pss:
    for (f,wf) in fs:
        result[f].add((wf, n1, s))

result = [(len(xs),f,xs) for (f,xs) in result.iteritems()]
result.sort(reverse=True)

for (c,f,xs) in result:
      if len(xs) > 1:
        wfs = ralign([x[0] for x in xs])
        lms = lalign(['p_' + x[1] for x in xs])
        sls = [x[2] for x in xs]
        print ((len(wfs[0])+len(lms[0]) - len(f)-3)*' ' + '=> %s <=' % f).encode('utf-8')
        for t in zip(lms,wfs,sls):
            print ('%s%s  %s' % t).encode('utf-8')
        print


