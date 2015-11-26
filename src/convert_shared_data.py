import codecs
import glob
import sys
from collections import defaultdict

if __name__ == '__main__':
    for filename in glob.glob('data/shared_task_data/splits/german-task1-train'):
        data = defaultdict(dict)
        msds = defaultdict(set)
        
        with codecs.open(filename, encoding='utf-8') as f:
            for (l,msd,wf) in [l.split('\t') for l in f.read().split('\n')[1:] if len(l) > 0]:
                pos = msd.split(',')[0].split('=')[1]
                msd = ",".join(msd.split(',')[1:])
                data[(l,pos)][msd] = wf
                msds[pos].add(msd)
        for ((l,pos),d) in data.iteritems():
         if pos == 'V':
            print ('%s\tBF' % l).encode('utf-8')
            for m in msds[pos]:
                if m in d:
                    print ('%s\t%s' % (d[m],m)).encode('utf-8')
                else:
                    print ('@%s\t%s' % (l,m)).encode('utf-8')
            print
