### Create a foma-compatible morphological analyzer from paradigm file ###

# Options:
# -o  recreate original data (all vars must be exactly instantiated as seen in training data)
# -c  constrain variables by generalizing (default pvalue = 0.05)
# -u  unconstrained (all variables are defined as ?+)
# -p  <pvalue>  use <pvalue> together with -c
# -s  keep different analyzers separate instead of merging with priority union
#     (may be necessary for some analyzers)
# -n  name of binary foma file to compile to

# Any combination of the above may be used. The analyzers are combined by
# priority union, e.g. -o -c -u would yield an analyzer
# [ Goriginal .P. Gconstrained .P. Gunconstrained ]

# Example usage:
# python morphanalyzer.py -o -c ./../paradigms/spanish_verbs.p > spanish_verbs.foma

import sys, getopt
import paradigm, genregex

def escape_fixed_string(string):
    """Fixed strings have _ to represent 0 (epsilon)."""
    if string == u'_':
        return u'0'
    else:
        return u'{' + string + u'}'

def nospace(string):
    return string.replace(' ','=').replace('_','=')

def paradigms_to_alphabet(paradigms):
    """Extracts all used symbols from an iterable of paradigms."""
    alphabet = set()
    for paradigm in paradigms:
          for idx, (is_var, slot) in enumerate(paradigm.slots):
                for word in slot:
                    alphabet |= set(word)
    return alphabet

def paradigms_to_foma(paradigms, grammarname, pval):
    """Converts iterable of paradigms to foma-script (as a string)."""
    parvars = {}
    rstring = u''
    defstring = u''
    substring = u''
    par_is_constrained = {}
    
    alphabet = paradigms_to_alphabet(paradigms)
    alphabet = {'"' + a + '"' for a in alphabet}
    alphstring = 'def Alph ' + u'|'.join(alphabet) + ';\n'
    
    for paradigm in paradigms:
  #      if paradigm.count < 3 and grammarname == 'Gunconstrained':
  #          continue
        par_is_constrained[paradigm.name] = False
        parstrings = []
        for formnumber, form in enumerate(paradigm.forms):
            tagstrings = map(lambda(feature, value): u'"' + feature + u'"' + u' = ' + u'"' + value + u'"' , form.msd)
            parstring = u''
            for idx, (is_var, slot) in enumerate(paradigm.slots):
                if is_var:
                    parvarname = nospace(paradigm.name) + '=var' + str(idx)
                    if parvarname not in parvars:
                        r = genregex.genregex(slot, pvalue = pval, length = False)
                        parvars[parvarname] = True
                        if r.fomaregex() != '?+':
                            par_is_constrained[paradigm.name] = True
                        defstring += 'def ' + parvarname + ' ' + r.fomaregex().replace('?', 'Alph') + ';\n'
                    parstring += ' [' + parvarname + '] '
                else:
                    thisslot = escape_fixed_string(slot[formnumber])
                    baseformslot = escape_fixed_string(slot[0])
                    parstring += u' [' + thisslot + u':' + baseformslot + u'] '
            parstring += u'0:["[" ' + u' " " '.join(tagstrings) + u' "]"]'
            parstrings.append(parstring)
        #if grammarname != 'Gcodnstrained' or par_is_constrained[paradigm.name]:
        rstring += u'def ' + nospace(paradigm.name) + u'|\n'.join(parstrings) + u';\n'
    
    #parnames = [nospace(paradigm.name) for paradigm in paradigms if ' ' not in paradigm.name]
    parnames = []
    for paradigm in paradigms:
        #if ' ' not in paradigm.name and (grammarname != 'Gconstrdained' or par_is_constrained[paradigm.name]):
        parnames.append(nospace(paradigm.name))
    
    rstring += u'def ' + grammarname + u' ' + u' | '.join(parnames) + u';'
    
    return alphstring + defstring + rstring

def main(argv):
    
    options, remainder = getopt.gnu_getopt(argv[1:],
        'ocup:sn:', ['original','constrained','unconstrained','pvalue','separate','name'])
    
    pv = 0.05
    
    (Goriginal, Gconstrained, Gunconstrained, Gseparate, Gname) = False, False, False, False, 'analyzer.bin'
    for opt, arg in options:
        if opt in ('-o', '--original'):
            Goriginal = True
        elif opt in ('-c', '--constrained'):
            Gconstrained = True
        elif opt in ('-u', '--unconstrained'):
            Gunconstrained = True
        elif opt in ('-s', '--separate'):
            Gseparate = True
        elif opt in ('-p', '--pvalue'):
            pv = float(arg)
        elif opt in ('-n', '--name'):
            Gname = arg
    
    paradigms = paradigm.load_file(remainder[0])
    
    analyzers = []
    analyzernames = []
    for analyzertype in (('Goriginal', 1.0), ('Gconstrained', pv), ('Gunconstrained', 0.0)):
        if eval(analyzertype[0]) == True:
            analyzers.append(paradigms_to_foma(paradigms, analyzertype[0], analyzertype[1]))
            analyzernames.append(analyzertype[0])
    
    for a in analyzers:
        print a.encode('utf-8')
    
    if len(analyzers) > 0:
        if Gseparate == True:
            for a in analyzernames:
                print 'regex ' + a + ';'
        else:
            print 'regex ' + u' .P. '.join(analyzernames) + ';'
        print 'save stack ' + Gname


if __name__ == "__main__":
    main(sys.argv)
