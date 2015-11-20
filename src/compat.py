import codecs
import glob
import sys
from collections import defaultdict
import paradigm

def pr_form(f):
    if f[0] == '@':
        return '@'*len(f)
    else:
        return f

def compatible(fs1,fs2):
    for (f1,f2) in zip(fs1,fs2):
        if f1 != f2 and f1[0] != '@' and f2[0] != '@':
            return False 
    return True

def compatibility_classes(ps):
    c_classes = []
    for (fs,n) in [([pr_form('+'.join(f.form)) for f in p.forms], p.name) for p in ps]:
        if c_classes == []:
            c_classes = [[(fs,n)]]
        else:
            mem = False
            for cset in c_classes:
                if all([compatible(fs,fs2) for (fs2,_) in cset]):
                    cset.append((fs,n))
                    mem = True
            if not mem:
                c_classes.append([(fs,n)])
    return c_classes

if __name__ == '__main__':
    try:
        phs = paradigm.load_file(sys.argv[1])
        ps  = paradigm.load_file(sys.argv[2])
        ambi = defaultdict(list)
        for (i,c) in enumerate(compatibility_classes(phs),1):
            print 'Class %d' % i
            for (fs,n) in c:
                ambi[n].append(i)
            for (fs,n) in c:
                if len(ambi[n]) > 1:
                    print ('    %s\t[%s:%d]' % (' '.join(fs), n,len(ambi[n]))).encode('utf-8')
                else:
                    print ('    %s\t%s' % (' '.join(fs), n)).encode('utf-8')
        print '\n  hole_pcount: %d\n  org_pcount: %d\n  merged_pcount: %d\n  ambi_count: %d' % (len(phs),len(ps), i, len([xs for (_,xs) in ambi.iteritems() if len(xs) > 1]))
    except:
        print 'usage: python compat.py ph_file p_file'
