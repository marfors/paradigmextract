from collections import defaultdict

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
      self.forms = []
      for (f,msd) in form_msds:
          self.forms.append(Form(f,msd))
      self.var_insts = var_insts

    def slots(self):
        """Compute the content
         of the slots.
        """
        if self.slts != None:
            return self.slts
        else:
            str_slots = zip(*[f.strs() for f in self.forms])
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

    def __call__(self,*insts):
        table = []
        for f in self.forms:
            table.append(f(*insts))
        return table

    def __str__(self):
        return "#".join([str(f) for f in self.forms])


                
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

    def strs(self):
        """Collects the strings in a wordform.
           A variable is assumed to be surrounded by (possibly empty) strings.
        """
        ss = []
        if self.form[0].isdigit():
           ss.append('')
        for i in range(len(self.form)):
            if not(self.form[i].isdigit()) or (len(self.form) < i and self.form[i+1].isdigit()):
             ss.append(self.form[i])
        if self.form[-1].isdigit():
            ss.append('')
        return ss
        
class Slot:
    """A class representing a slot in a wordform.

       Args:
        insts: list(str)
          Ex: ['spr','st']
        is_var: bool
          Is it a variable slot or not?
    """
    
    def __init__(self, insts, is_var = True):
        self.is_var = is_var
        self.insts = insts
        
    def is_var(self):
        return self.is_var
        
    def is_str(self):
        return not(self.is_var)

    def members(self):
        return self.insts

if __name__ == '__main__':
    p = Paradigm([('1+i+2+er',[]), ('1+a+2',[])],[[('1','spr'),('2','ng')], [('1','st'),('2','ck')]])
    print p('spr','ng')
    # print the content of the slots
    for (i,s) in enumerate(p.slots()):
        print '%d: %s' % (i," ".join(s.members()))

