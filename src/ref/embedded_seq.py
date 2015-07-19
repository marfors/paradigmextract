import codecs
import sys
import glob
from collections import defaultdict

def is_var(s):
    return s.isdigit()

def extract_embedded(wf,em_d):
    pre_var = False
    pvar = ''
    index = ''
    for i in range(0,len(wf)-1):
        if is_var(wf[i]):
            pre_var = True
            pvar = wf[i]
            if is_var(wf[i+1]):
                em_d[wf[i]+':'+wf[i+1]].add('0')
        else:
            if pre_var and is_var(wf[i+1]):
               em_d[pvar+':'+wf[i+1]].add(wf[i].replace('"',''))
            pre_var = False
    return em_d

for fp in glob.glob('paradigms/*.para'):
  p_em_d = defaultdict(list)
  print '\n[%s]\n' % fp
  with codecs.open(fp,encoding='utf-8') as f:    
    for (i,l) in enumerate(f,1):
      em_d = defaultdict(set)
      (p,ex) = l.split('\t')
      pid = ex.split(',')[0].split('=')[1]
      wfs = p.split('#')
    
      for wf in wfs:
        em_d = extract_embedded(wf.split('+'),em_d)
      for (i,st) in em_d.iteritems():
            s = '[%s] %s' % (i,"-".join(st))
            p_em_d[s].append(pid)

    p_em_l = []
    for (s,pids) in p_em_d.iteritems():
      p_em_l.append((len(pids), (s,pids)))
    p_em_l.sort(reverse=True)
    for (i,(s,pids)) in p_em_l:
      if i > 1:
        print ('%s\t%s' % (s,", ".join(pids))).encode('utf-8')
