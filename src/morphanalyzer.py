### Create a foma-compatible morphological analyzer from paradigm files ###

import sys, paradigm

paradigms = paradigm.load_file(sys.argv[1])

def escape_fixed_string(string):
    if string == u'_':
        return u'0'
    else:
        return u'{' + string + u'}'
        
for (pcount, pname, paradigm) in paradigms:
    parstrings = []
    for formnumber, form in enumerate(paradigm.forms):
        tagstrings = map(lambda(feature, value): u'"' + feature + u'"' + u' = ' + u'"' + value + u'"' , form.msd)
        parstring = u''
        for (is_var,slot) in paradigm.info()['slots']:
            if is_var:
                parstring += u'?+'
            else:
                thisslot = escape_fixed_string(slot[formnumber])
                baseformslot = escape_fixed_string(slot[0])
                parstring += u' ' + thisslot + u':' + baseformslot + u' '
        parstring += u'0:["[" ' + u' " " '.join(tagstrings) + u' "]"]'
        parstrings.append(parstring)
    print (u'def ' + pname + u'|\n'.join(parstrings) + u';').encode('utf-8')

parnames = [pname for (pcount, pname, paradigm) in paradigms]
print (u'def Grammar ' + u' | '.join(parnames) + u';').encode('utf-8')
print u'regex Grammar;'
