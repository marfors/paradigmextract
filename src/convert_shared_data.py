import codecs
import glob
import sys
from collections import defaultdict

if __name__ == '__main__':
    data = defaultdict(dict)
    msds = defaultdict(set)
        
    with codecs.open(sys.argv[1], encoding='utf-8') as f:
        for (l,msd,wf) in [l.split('\t') for l in f.read().split('\n')[1:] if len(l) > 0]:
            pos = msd.split(',')[0].split('=')[1]
            msd = ",".join(msd.split(',')[1:])
            data[(l,pos)][msd] = wf
            msds[pos].add(msd)
        for ((l,pos),d) in data.iteritems():
            if pos == sys.argv[2]:
                print ('%s\tBF' % l).encode('utf-8')
                for m in msds[pos]:
                    if m in d:
                        print ('%s\t%s' % (d[m],m)).encode('utf-8')
                    else:
                        print ('@%s\t%s' % (l,m)).encode('utf-8')
                print
