# -*- coding: utf-8 -*-

import re
import sys
import codecs
from collections import defaultdict
import regexmatcher
import genregex

def overlap(ss):
    count = 0
    for (c1,c2) in zip(prefix[::-1],suffix):
        if c1 == c2:
            count += 1
        else:
            return count
    return count

class Paradigm:
    """A class representing a paradigm.

    Args:
       form_msd:list(tuple)
            Ex: [('1+en',[('tense','pres')]), ...,
       var_insts:list(tuple)
            Ex: [[('1','dimm')],[('1','dank')], ...]
    """
    

    def __init__(self, form_msds, var_insts, prefix=None):
      self.p_info = {}
      self.forms = []
      self.var_insts = var_insts
      if prefix == None:
          self.prefix = ''
      else:
          self.prefix = prefix         
      for (f,msd) in form_msds:
          self.forms.append(Form(f,msd,var_insts))

    def __getattr__(self,attr):
        if len(self.p_info) > 0: # Compute only once.
            return self.p_info[attr]
        else:
            if len(self.var_insts) != 0:
                self.p_info['name'] = self.prefix + self.__call__(*[s for (_,s) in self.var_insts[0]])[0][0]
                self.p_info['count'] = len(self.var_insts)
            else: # no variables
                self.p_info['name'] = self.prefix + self.__call__()[0][0]
                self.p_info['count'] = 1
            self.p_info['slots'] = self.__slots()
        return self.p_info[attr]

    def __slots(self):
        slts = []
        """Compute the content
         of the slots.
        """
        # string slots
        fs = [f.strs() for f in self.forms]
        str_slots = zip(*fs)
        # var slots
        vt = defaultdict(list)
        for vs in self.var_insts:
            for (v,s) in vs:
                vt[v].append(s)        
        var_slots = vt.items()
        var_slots.sort(key=lambda x: x[0])
        (s_index,v_index) = (0,0)
        for i in range(len(str_slots) + len(var_slots)): # interleave strings and variables
            if i % 2 == 0:
                    slts.append((False,str_slots[s_index]))
                    s_index += 1
            else:
                slts.append((True,var_slots[v_index][1]))
                v_index += 1
        return slts

    def fits_paradigm(self,w, constrained=True):
        for f in self.forms:
            if f.match(w, constrained):
                return True
        return False

    def match(self,w, selection=None, constrained=True):
        result = []
        if selection == None:
            forms = self.forms
        else:
            forms = [self.forms[i]  for i in selection]
        for f in forms:
            xs = f.match_vars(w, constrained)
            result.append(xs)
        return result

    def paradigm_forms(self):
        if len(self.var_insts) > 0:
            ss = [s for (_,s) in self.var_insts[0]]
        else:
            ss = []
        return [f.shapes(ss) for f in self.forms]

    def __call__(self,*insts):
        table = []
        for f in self.forms:
            (w,msd) = f(*insts)
            table.append((''.join(w), msd))
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
    def __init__(self, form, msd=[], v_insts=[]):
        (self.form,self.msd) = (form.split('+'), msd)
        self.scount = 0
        r = ''
        for f in self.form:
            if f.isdigit():
                r += '(.+)'
            else:
                r += f
                self.scount += len(f)
        self.regex = r
        self.cregex = re.compile(self.regex)
        # vars
        collect_vars = defaultdict(set)
        for vs in v_insts:
            for (i,v) in vs:
                collect_vars[i].add(v)
        self.v_regex = []
        for (_,ss) in collect_vars.iteritems():
            self.v_regex.append(re.compile(genregex.genregex(ss,pvalue=0.05).pyregex()))

    def shapes(self, ss):
        w = "".join(self.__call__(*ss)[0])
        return {'form':"+".join(self.form),
                'msd':self.msd,
                'w':w,
                'regex':self.regex,
                'cregex':self.cregex,
                'v_regex':self.v_regex}
                                    
    def __call__(self,*insts):
        """Instantiate the variables of the wordform.
           Args:
            insts: fun args
                   Ex: f('schr','i','b')
        """
        (w,vindex) = ([],0)
        for p in self.form:
            if p.isdigit(): # is a variable
                w.append(insts[vindex])
                vindex += 1
            else:
                w.append(p)
        return (w, self.msd)
    
    def match(self,w,constrained=True):
            return self.match_vars(w,constrained) != None
        
    def match_vars(self,w, constrained=True):
        matcher = regexmatcher.mregex(self.regex)
        ms = matcher.findall(w)
        if ms == None:
                return None
        elif ms == []:
            return []
        if not constrained:
            return [(self.scount, m) for m in ms]
        else:
            result = []
            for vs in ms:
                if type(vs) == str:
                    var_and_reg = [(vs,self.v_regex[0])]
                else:
                    var_and_reg = zip(vs,self.v_regex)
                vcount = 0
                m_all = True
                for (s,r) in var_and_reg:
                    m = r.match(s)
                    if m == None:
                            return None
                    xs = m.groups() # .+-matches have no grouping
                    if len(xs) > 0 or r.pattern == '.+':
                        if r.pattern != '.+':
                            vcount += len("".join(xs)) # select the variable specificity
                    else:
                        m_all = False
                        break
                if m_all:
                    result.append((self.scount+vcount, vs))
            if result == []:
                return None
            else:
                return result

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
            paradigms.append((len(p_members),wfs,p_members))
    paradigms.sort(reverse=True)
    return [Paradigm(wfs,p_members, 'p%d_' % i) for (i,(_,wfs,p_members)) in enumerate(paradigms,1)]

def pr(i,b):
  if b: return '[v] %d' % (i)
  else: return '[s] %d' % (i)

if __name__ == '__main__':
    if '-p' in sys.argv:
        for p in load_file(sys.argv[-1]):
            print ('name: %s, count: %d' % (p.name,p.count)).encode('utf-8')
            if len(p.var_insts) > 0:
                print ('members: %s' % (", ".join([p(*[v[1] for v in vs])[0][0] for vs in p.var_insts]))).encode('utf-8')
            else:
                print ('members: %s' % (p()[0][0])).encode('utf-8')
            for f in p.forms:
                print unicode(f).replace(':','\t').encode('utf-8')
            print
    elif '-s' in sys.argv:
        for p in load_file(sys.argv[-1]):
            print ('%s: %d' % (p.name,p.count)).encode('utf-8')
            # print the content of the slots
            for (i,(is_var, s)) in enumerate(p.slots):
                print ('%s: %s' % (pr(i, is_var)," ".join(s))).encode('utf-8')
            print
    else:
            print 'Usage: <program> [-p|-s] <paradigm_file>'
