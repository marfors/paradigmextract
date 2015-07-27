import paradigm
from collections import defaultdict
import sys

def ralign(ss):
    m = max([len(s) for s in ss])
    return [(1+m-len(s))*' '+s for s in ss]

def lalign(ss):
    m = max([len(s) for s in ss])
    return [(s+(1+m-len(s))*' ') for s in ss]

def extract_form_information(ps,only_lemma=False):
    pss = [(n, # paradigm name
            c, # member count
            [p.p_forms()[0]] if only_lemma else p.p_forms(), # form patterns + form insts
            ' '.join(['[%s]' % ",".join(list(set(s.members()))[:5]) for s in p.slots() if s.is_var()])) # slots (< 5 members)
                for (c,n,p) in ps]
    result = defaultdict(set)
    for (n1,c,fs,s) in pss:
        for (f,wf) in fs:
            result[f].add((c,n1, wf, s))
    result = [(len(xs),f,xs) for (f,xs) in result.iteritems()] # sort with respect to the ambiguity count
    result.sort(reverse=True)
    return result

for (n,f,xs) in extract_form_information(paradigm.load_file(sys.argv[1]),'-l' in sys.argv):
      if len(xs) > 1: # we only print the ambiguous forms.
        xs = sorted(xs,reverse=True)
        wfs = ralign([x[2] for x in xs])
        lms = lalign(['p_%s %d' % (x[1],x[0]) for x in xs])
        sls = [x[3] for x in xs]
        print ((len(wfs[0])+len(lms[0]) - len(f)-3)*' ' + '=> %s <=' % f).encode('utf-8')
        for t in zip(lms,wfs,sls):
            print ('%s%s  %s' % t).encode('utf-8')
        print
