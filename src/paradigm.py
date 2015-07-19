def load_file(f):
    pass

# aakkosteta,aakkostaa,mood=indicative:tense=present:aspect=passive:polarity=negative
# wordform \t lemma \t pos \t msd \t ID

# p = Paradigm([(msd,Form)])

# p('schr','i','b')

# p.instansiate('schr','i','b')

# p['tense']['Sg'] <- throws Uninst

class Form:

    def __init__(self):
        pass

class Slot:

    def __init__(self, type, insts):

    def is_var(self):
        pass
        
    def is_str(self):
        pass

[''][1]['a'][2]['']

[('MSD':'form'), ... ]
            
class Paradigm:

    def __init__(self, forms):
      self.forms = forms
      self.num_vars = forms[0].num_vars
      pass

    def __call__(self,*insts):
        
    def instansiate(self, *insts): # vars = [(v_id, str)]
        pass

    def slots(self):
        pass

    def forms(self):
        pass

    def __str__(self):
        pass
        
    def __iter__(self):
        pass
        
    def __getitem__(self):
        pass
           
