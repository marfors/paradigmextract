import codecs
import glob
import sys
from collections import defaultdict
import paradigm

class PClasses:

    """A class for representing abstractions over incomplete paradigms, i.e., paradigm classes"""
    
    def __init__(self, pfile):
        # (pname, paradigm forms)
        self.ptable = dict([(p.name, [self._convert_holes('+'.join(f.form)) for f in p.forms])
                                                      for p in paradigm.load_file(pfile)])
        # compatibility adjacency graph
        self.compat_graph = self._build_compat_graph()
    
    def _convert_holes(self,f):
        # '@baseform_pattern' => '@'
        if f[0] == '@': return '@'
        else: return f
            
    def _compatible(self,fs1,fs2):
        # check if two paradigms are form compatible.
        for (f1,f2) in zip(fs1,fs2):
            if f1 != f2 and f1[0] != '@' and f2[0] != '@':
                return False 
        return True

    def _build_compat_graph(self):
        # build the compatibility adjacency graph
        compat_graph = defaultdict(set)
        for pid1 in self.ptable:
            for pid2 in self.ptable:
                if pid1 != pid2:
                    if self._compatible(self.ptable[pid1], self.ptable[pid2]):
                        compat_graph[pid1].add(pid2)
        return compat_graph

    def paradigm_classes(self, ps):
        c_classes = []
        # start with the paradigm with the least number of compatible paradigms.
        for (_,n) in sorted([(len(ns),n) for (n,ns) in self.compat_graph.iteritems()]):
            if c_classes == []:
                c_classes = [set([n])]
            else:
                member = False
                for cset in c_classes: # iterate over current classes
                    if all([n2 in self.compat_graph[n] for n2 in cset]):
                        cset.add(n)
                        member = True
                if not member: # if the current paradigm is not compatible with any current class, add it to a new class.
                    c_classes.append(set([n]))
        return c_classes

    def paradigm(self,name):
        # return paradigm forms.
        return self.ptable[name]
    
    def class_paradigm(self,c):
        # derive the class paradigm from the members of the class.
        self.cforms = []
        for xs in zip(*[self.ptable[n] for n in c]):        
            for x in xs:
                f = x
                if f[0] != '@': # instantiation found.
                    break
            self.cforms.append(f)
        return self.cforms
    
    def pr_info(self,cs,ps):
        
        ambi = defaultdict(list)
        for (i,c) in enumerate(cs,1): # compute ambiguity
            for n in c:
              ambi[n].append(i)
                      
        for (i,c) in enumerate(cs,1): # print paradigm classes
            print '\nClass %d' % i 
            for n in c:
                fs = phs.paradigm(n) 
                if len(ambi[n]) > 1:
                    print ('    %s\t[%s:%d]' % (' '.join(fs), n,len(ambi[n]))).encode('utf-8')
                else:
                    print ('    %s\t%s' % (' '.join(fs), n)).encode('utf-8')
            print (' => %s' % (' '.join(phs.class_paradigm(c)))).encode('utf-8')

        # print some stats.
        print '\n  hole_pcount: %d\n  org_pcount: %d\n  merged_pcount: %d\n  ambi_count: %d' % (len(phs.ptable),len(ps), i, len([xs for (_,xs) in ambi.iteritems() if len(xs) > 1]))

        
if __name__ == '__main__':
    try:
        phs = PClasses(sys.argv[1]) # paradigms with holes
        ps  = paradigm.load_file(sys.argv[2]) # paradigms without holes as reference
        cs  = phs.paradigm_classes(phs) # compute paradigm classes
        phs.pr_info(cs,ps)
    except:
        print 'usage: python compat.py ph_file p_file'
