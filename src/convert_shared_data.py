import codecs
import glob
import sys
from collections import defaultdict

if __name__ == '__main__':
    data = {}
    for filename in glob.glob('data/shared_task_data/splits/*task1-train'):
        with codecs.open(filename, encoding='utf-8') as f:
            data[filename.split('/')[-1]] = [tuple(l.split('\t')) for l in f.read().split('\n')[1:] if len(l) > 0]
            # (u'd\xfcld\xfcl', u'pos=N,case=DAT,num=PL', u'd\xfcld\xfcllere')
    print data
