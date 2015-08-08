class genregex:
    
    """Generalizes a list of strings into a regex.
       The main strategy is to find those complete strings, suffixes, or
       prefixes in the set that seem to be restricted in their distribution
       and issue a regular expression (Python or foma), that matches a limited
       set of strings.

       This is achieved through a number of tests.
       We first make the assumption that strings in a set are drawn from a
       uniform distribution with n members.  Then, we
        (1) ask how likely it is to draw this particular sequence, assuming the
       set really has n+1 members (i.e. where we never happened to see the
       n+1th member) which is
             p = 1-(1/(n+1)) ** num_draws
       where num draws is the length of the list of strings. If this p < 0.05 (by default)
       we assume we have seen all members of the set and declare the set to be fixed.
       
       If the set of members is not found to be fixed, we further investigate
       the suffixes and prefixes in the set. We the find the longest
        (2a) set of suffixes that can be assumed to be fixed
        (2b) prefix that fulfills the same conditions.
       We also examine the distribution of string lengths. If, by the same analysis,
       the lengths of strings can be assumed to be drawn from a fixed set, we
       limit the set of allowable lengths.

       A regex can be returned either for python or foma. The regex
       may need to check both the prefix and suffixes separately, which
       is easily done in a foma-style regex since we can intersect the
       prefix and suffix languages separately:
       
         [?* suffixes] & [prefixes ?*] & [?^{minlen, maxlen}]

       However, this can't be directly done in Python.  To simulate this,
       we check the suffix (and possible length constraints) by a lookahead
       which doesn't consume any symbols, before the checking the prefix, ie.
       
         ^(?=.*suffixes$)(?=.{minlen, maxlen})prefixes

       Example:
       >>>words = ['ab','ab','ab','ba','ba','ba','ab','ba','a','b']
       >>>r = genregex.genregex(words)
       >>>print r.pyregex()
       ^(?=.*(a|b)$)(?=.{1,2}$)(a|b)
       >>>print r.fomaregex()
       [?* [{a}|{b}]] & [?^{1,2}] & [[{a}|{b}] ?*]
       """
    
    def __init__(self, strings, pvalue = 0.05):
        self.strings = strings
        self.numstrings = len(self.strings)
        self.pvalue = pvalue
        self.minlen = len(min(self.strings, key = len))
        self.maxlen = len(max(self.strings, key = len))
        
        self.stringset = set()
        self.prefixset = set()
        self.suffixset = set()
        self.lenrange = ()
        
        # Case (1): if the totality of strings seems to have a limited distribution
        if self._significancetest(self.numstrings, len(set(self.strings))):
            self.stringset = set(self.strings)
            return
        # Case (2a): find longest suffix that has limited distribution
        for i in xrange(-self.minlen, 0):
            suffstrings = map(lambda x: x[i:], self.strings)
            if self._significancetest(len(suffstrings), len(set(suffstrings))):
                self.suffixset = set(suffstrings)
                break
        # Case (2b): find longest prefix that has limited distribution
        for i in xrange(self.minlen, 0, -1):
            prefstrings = map(lambda x: x[:i], self.strings)
            if self._significancetest(len(prefstrings), len(set(prefstrings))):
                self.prefixset = set(prefstrings)
                break
        # Case (2c): find out if stringlengths have limited distribution
        stringlengths = set(map(lambda x: len(x), self.strings))
        if self._significancetest(self.numstrings, len(stringlengths)):
            self.lenrange = (self.minlen, self.maxlen)
        return

    def fomaregex(self):
        # [?* suffix] & [prefix ?*] & [?^{min,max}]
        def explode(string):
            return '{' + string + '}'
        
        re = []
        if len(self.stringset) > 0:
            return '[' + u'|'.join(map(explode, self.stringset)) + ']'
        if len(self.suffixset) > 0:
            re.append('[?* [' + '|'.join(map(explode, self.suffixset)) + ']]')
        if len(self.lenrange) > 0:
            re.append('[?^{' + str(self.lenrange[0]) + ',' + str(self.lenrange[1]) + '}]')
        if len(self.prefixset) > 0:
            re.append('[[' + '|'.join(map(explode, self.prefixset)) + '] ?*]')
        if len(re) == 0:
            return u'?+'
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
            return u'.+'
        else:
            return '^' + re
                    
    def _significancetest(self, num, uniq):
        if (1.0-(1.0/(uniq+1.0))) ** num <= self.pvalue:
            return True
        return False
