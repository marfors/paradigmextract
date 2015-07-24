# -*- coding: utf-8 -*-  

import re
import sys
import codecs
from collections import defaultdict
import regexmatcher

class Paradigm:
    """A class representing a paradigm.

    Args:
       form_msd:list(tuple)
            Ex: [('1+en',[('tense','pres')]), ...,
       var_insts:list(tuple)
            Ex: [[('1','dimm')],[('1','dank')], ...]
    """
    
    def __init__(self, form_msds, var_insts):
      self.slts = None
      self.name = None
      self.count = None
      self.forms = []
      for (f,msd) in form_msds:
          self.forms.append(Form(f,msd))
      self.var_insts = var_insts

    def p_info(self):
        if self.name != None:
            return (self.name,self.count)
        else:
            if len(self.var_insts) != 0:
                self.name = self.__call__(*[s for (_,s) in self.var_insts[0]])[0][0]
                self.count = len(self.var_insts)
            else:
                self.name = self.__call__()[0][0]
                self.count = 1
            return (self.name, self.count)
              
    def slots(self):
        """Compute the content
         of the slots.
        """
        if self.slts != None:
            return self.slts
        else:
            fs = [f.strs() for f in self.forms]
            str_slots = zip(*fs)
        vt = defaultdict(list)
        for vs in self.var_insts:
            for (v,s) in vs:
                vt[v].append(s)
        var_slots = vt.items()
        self.slts = []
        (s_index,v_index) = (0,0)
        for i in range(len(str_slots) + len(var_slots)): # interleave strings and variables
            if i % 2 == 0:
                    self.slts.append(Slot(str_slots[s_index],False))    
                    s_index += 1
            else:
                self.slts.append(Slot(var_slots[v_index][1]))    
                v_index += 1
        return self.slts

    def fits_paradigm(self,w):
        for f in self.forms:
            if f.match(w):
                return True
        return False

    def p_forms(self):
        if len(self.var_insts) > 0:
            ss = [s for (_,s) in self.var_insts[0]]
        else:
            ss = []
        return [("+".join(f.form),f(*ss)[0]) for f in self.forms]

        
    def __call__(self,*insts):
        table = []
        for f in self.forms:
            table.append(f(*insts))
        return table

    def __str__(self):
        p = "#".join([f.__unicode__() for f in self.forms])
        v = "#".join([",".join(['%s=%s' % v for v in vs]) for vs in self.var_insts])
        return ('%s\t%s' % (p,v)).encode('utf-8')
    
class Form:
    """A class representing a paradigmatic wordform and, possibly, its
    morphosyntactic description.

    Args:
       form:str
            Ex: 1+a+2
       msd:list(tuple)
            Ex: [('num','sg'),('case':'nom') .. ]
                [] no msd available
                [(None,'SGNOM')] no msd type available
    """
    def __init__(self, form, msd=[]):
        (self.form,self.msd) = (form.split('+'), msd)
        r = ''
        for f in self.form:
            if f.isdigit():
                r += '.+'
            else:
                r += f
        self.regex = r 
        self.cregex = re.compile(self.regex)
                 
    def __call__(self,*insts):
        """Instantiate the variables of the wordform.
           Args:
            insts: fun args
                   Ex: f('schr','i','b') 
        """
        (w,vindex) = ('',0) 
        for p in self.form:
            if p.isdigit(): # is a variable
                w += insts[vindex]
                vindex += 1
            else:
                w += p
        return (w, self.msd)

    def match(self,w):
        return self.cregex.match(w)
    
    def match_vars(self,w):
        m = regexmatcher.mregex(r)
        return m.findall(w)
        
    def strs(self):
        """Collects the strings in a wordform.
           A variable is assumed to be surrounded by (possibly empty) strings.
        """
        ss = []
        if self.form[0].isdigit():
           ss.append('_')
        for i in range(len(self.form)):
            if not(self.form[i].isdigit()): 
                ss.append(self.form[i])
            elif i < len(self.form)-1 and self.form[i+1].isdigit():
                ss.append('_')
        if self.form[-1].isdigit():
            ss.append('_')
        return ss
    
    def __unicode__(self):
        ms = []
        for (t,v) in self.msd:
            if t != None:
                if v != None:
                    ms.append('%s=%s' % (t,v))
                else:
                    ms.append(t)
            else:
                if v != None:
                    ms.append(v)
        if len(ms) == 0:
            return "+".join(self.form)
        else:
            return "%s:%s" % ("+".join(self.form), ",".join(ms))

class Slot:
    """A class representing a slot in a wordform.

       Args:
        insts: list(str)
          Ex: ['spr','st']
        is_var: bool
          Is it a variable slot or not?
    """
    
    def __init__(self, insts, is_var = True):
        self.iv = is_var
        self.insts = insts
        
    def is_var(self):
        return self.iv
  
    def members(self):
        return self.insts

# [('1+en',[('tense','pres')]
    
def load_file(file):
    paradigms = []
    with codecs.open(file,encoding='utf-8') as f:
        for l in f:
            try:
                (p,ex) = l.strip().split('\t')
            except:
                p = l.strip()
                ex = ''
            p_members = []
            wfs = []
            for s in p.split('#'):
                (w,m) = s.split(':')
                msd = [tuple(x.split('=')) for x in m.split(',')]
                wfs.append((w,msd))
            if len(ex) > 0:
                for s in ex.split('#'):
                    mem = []
                    for vbind in s.split(','):
                        mem.append(tuple(vbind.split('=')))
                    p_members.append(mem)
            else: # no variables
                p_members = []
            paradigm = Paradigm(wfs, p_members)
            (name,count) = paradigm.p_info()
            paradigms.append((count,name,paradigm))
    paradigms.sort(reverse=True)
    return paradigms

def pr(i,b):
  if b: return '[v] %d' % (i)
  else: return '[s] %d' % (i) 
  
if __name__ == '__main__':
    for (c,n,p) in load_file(sys.argv[1]):
        print ('%s: %d' % (n,c)).encode('utf-8')
        # print the content of the slots
        for (i,s) in enumerate(p.slots()):
            print ('%s: %s' % (pr(i, s.is_var())," ".join(s.members()))).encode('utf-8')
        print
