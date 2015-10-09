import subprocess
import codecs
import glob
import sys
from collections import defaultdict


def processes(models):
    ps = []
    for m in models: # a model file ends with train_dev.foma.bin
        c = 'flookup -b -i -a ' + m
        proc = subprocess.Popen(c, shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, )
        ps.append(proc)
    return ps

def analyze(w, ps):
    out = set()
    for p in ps:
        p.stdin.write(w.encode('utf-8')+'\n')
        while True: # collect all FST analyses
            o = p.stdout.readline().decode('utf-8').strip()
            if len(o) > 0:
                if out != '+?': # +? = no analysis
                    out.add(o.split('\t')[1])
            else: # blank line = no more analyses 
                break
    return out

def read_data(fs):
    d = defaultdict(set)
    for f in fs:
        with codecs.open(f, encoding='utf-8') as f:
            new_lemma = True
            lemma = ''
            for l in f:
                s = l.strip()
                if len(s) > 0:
                    (w,msd) = s.split('\t')
                    if new_lemma:
                        (lemma,new_lemma) = (w,False) # first form in a table
                    d[w].add('%s[%s]' % (lemma,msd.replace(',', ' '))) # convert to FST format
                else: # a blank line separates the tables
                    new_lemma = True
    return d

def exp(lang):
    models = glob.glob('../morph/' + lang + '*train_dev.foma.bin')
    data = glob.glob('../data/' + lang + '*test.txt')
    ps = processes(models)
    d = read_data(data)
    result = []
    for (w,xs) in d.iteritems():
        mas = analyze(w,ps)
        common = xs.intersection(mas)
        diff = xs.difference(mas)
        result.append((len(diff),(w,mas,xs,common,diff)))
    result.sort(reverse=True)
    return result

def pr_diff(diff):
    # print a compact representation of the missed lemma+msd pairs.
    ss = []
    d = defaultdict(set)
    for x in diff:
        (l,msd) = x.split('[',1)
        msd = "+".join([p.split('=')[1] for p in msd[:-1].split(' ')])
        d[l].add(msd)
    for (l,msd) in d.iteritems():
        ss.append('%s+{%s}' % (l,", ".join(msd)))
    return ", ".join(ss)
    
if __name__ == '__main__':
    lang = sys.argv[1]
    result = exp(lang)
    (wcount, total,correct,mcount) = (0,0,0,0)
    for (dl,(w,mas,xs,common,diff)) in result:
        wcount += 1
        total += len(xs)
        correct += len(common)
        mcount += len(mas)
        print ('%s\t missing:%d (d:%d m:%d)\t%s' % (w,dl,len(xs), len(mas), pr_diff(diff))).encode('utf-8')
    recall = '    recall: %.2f%s (%d of %d lemma+msd)' % (100*float(correct)/total,'%', correct, total)
    sd = '    M/D: %.2f' % (float(mcount)/total)
    sys.stderr.write('\n    lang: %s\n'%lang+recall+'\n')
    sys.stderr.write('    unique wfs: %d' % (wcount) + '\n')
    sys.stderr.write(sd+'\n\n')
