class genregex:
    
    """Generalizes a list of strings into a regex.
       The main strategy is to find those complete strings, suffixes, or
       prefixes in the set that seem to be restricted in their distribution
       and issue a regular expression (python or foma), that matches a limited
       set of strings."""
    
    def __init__(self, strings, pvalue = 0.05):
        self.strings = strings
        self.numstrings = len(self.strings)
        self.pvalue = pvalue
        self.minlen = min(map(lambda x: len(x), self.strings))
        self.maxlen = max(map(lambda x: len(x), self.strings))
        
        self.stringset = set()
        self.prefixset = set()
        self.suffixset = set()
        self.lenrange = ()
        # Case (1): if the totality of strings seem to have a limited distribution
        if self._significancetest(self.numstrings, len(set(self.strings))):
            self.stringset = set(self.strings)
            return
        # Case (2a): find longest suffix that has limited distribution
        for i in xrange(-self.minlen, 0):
            suffstrings = map(lambda x: x[i:], self.strings)
            print "SUFFTEST:", suffstrings
            if self._significancetest(len(suffstrings), len(set(suffstrings))):
                self.suffixset = set(suffstrings)
                break
        # Case (2b): find longest prefix that has limited distribution
        for i in xrange(self.minlen, 0, -1):
            prefstrings = map(lambda x: x[:i], self.strings)
            print "PREFTEST:", prefstrings
            if self._significancetest(len(prefstrings), len(set(prefstrings))):
                self.prefixset = set(prefstrings)
                break
        # Case (2c): find out if stringlengths have limited distribution
        lenrange = []
        stringlengths = self.maxlen - self.minlen
        if self._significancetest(self.numstrings, stringlengths):
            self.lenrange = (self.minlen, self.maxlen)
        return

    def fomaregex(self):
        # [?* suffix] & [prefix ?*] & [?^{min,max}]
        def explode(string):
            return '{' + string + '}'
        
        re = []
        if len(self.stringset) > 0:
            return '[' + u'|'.join(self.stringset) + ']'
        if len(self.suffixset) > 0:
            re.append('[?* [' + '|'.join(map(explode, self.suffixset)) + ']]')
        if len(self.lenrange) > 0:
            re.append('[?^{' + str(self.lenrange[0]) + ',' + str(self.lenrange[1]) + '}]')
        if len(self.prefixset) > 0:
            re.append('[[' + '|'.join(map(explode, self.prefixset)) + '] ?*]')
        if len(re) == 0:
            return u'?*'
        else:
            return ' & '.join(re)
        
    def pyregex(self):
        # ^(?=.*suffix$)(?=.{min,max}$)prefix
        re = u''
        if len(self.stringset) > 0:
            return '^(' + u'|'.join(self.stringset) + ')$'
        if len(self.suffixset) > 0:
            re += '(?=.*(' + '|'.join(self.suffixset) + ')$)'
        if len(self.lenrange) > 0:
            re += '(?=.{' + str(self.lenrange[0]) + ',' + str(self.lenrange[1]) + '}$)'
        if len(self.prefixset) > 0:
            re += '(' + '|'.join(self.prefixset) + ')'
        if len(re) == 0:
            return u'.*'
        else:
            return '^' + re
                    
    def _significancetest(self, num, uniq):
        if (1.0-(1.0/(uniq+1.0))) ** num <= self.pvalue:
            return True
        return False
