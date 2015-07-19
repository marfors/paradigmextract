import codecs
import sys
import itertools

# Wordgraph class to extract LCS

class wordgraph:

    """Convert word to directed graph that contains all subsequences of word."""
    @classmethod
    def wordtograph(cls, word):
        trans = {}
        for i in xrange(len(word)):
            for j in xrange(i,len(word)):
                if (i,word[j]) not in trans:
                    trans[(i,word[j])] = j+1
        grph = cls(trans)
        return grph

    """Simple directed graph class."""
    def __init__(self, transitions):
        self.alphabet = {symbol for (state,symbol) in transitions}
        self.states = {state for (state,symbol) in transitions} | set(transitions.values())
        self.transitions = transitions
        self.revtrans = {}
        for (state,sym) in self.transitions:
            if self.transitions[(state,sym)] in self.revtrans:
                self.revtrans[self.transitions[(state,sym)]] |= {(state,sym)}
            else:
                self.revtrans[self.transitions[(state,sym)]] = {(state,sym)}
                
    def __getattr__(self, attr):
        if attr == 'longestwords':
            self._maxpath()
            return self.longestwords
        raise AttributeError("%r object has no attribute %r" % (self.__class__, attr))

    def __and__(self, other):
        return self.intersect(other)

    def intersect(self, other):
        """Calculate intersection of two directed graphs."""
        alphabet = self.alphabet & other.alphabet
        stack = [(0,0)]
        statemap = {(0,0):0}
        nextstate = 1
        trans = {}
        while len(stack) > 0:
            (asource,bsource) = stack.pop()
            for sym in alphabet:
                if (asource, sym) in self.transitions and (bsource, sym) in other.transitions:
                    atarget = self.transitions[(asource, sym)]
                    btarget = other.transitions[(bsource, sym)]
                    if (atarget,btarget) not in statemap:
                        statemap[(atarget,btarget)] = nextstate
                        nextstate += 1
                        stack.append((atarget,btarget))
                    trans[(statemap[(asource,bsource)], sym)] = statemap[(atarget,btarget)]
                    
        return wordgraph(trans)
    
    def _backtrace(self, maxsources, maxlen, state, tempstring):
        if state not in self.revtrans:
            tempstring.reverse()
            self.longestwords.append("".join(tempstring))
            return
        for (backstate, symbol) in self.revtrans[state]:
            if maxlen[backstate] == maxlen[state] - 1:
                self._backtrace(maxsources, maxlen, backstate, tempstring + [symbol])

    def _maxpath(self):
        tr = {}
        # Create tr which simply has graph structure without symbols
        for (state,sym) in self.transitions:
            if state not in tr:
                tr[state] = set()
            tr[state].update({self.transitions[(state,sym)]})

        S = {0}
        maxlen = {}
        maxsources = {}
        for i in self.states:
            maxlen[i] = 0
            maxsources[i] = {}

        step = 1
        while len(S) > 0:
            Snew = set()
            for state in S:
                if state in tr:
                    for target in tr[state]:
                        if maxlen[target] < step:
                            maxsources[target] = {state}
                            maxlen[target] = step
                            Snew.update({target})
                        elif maxlen[target] == step:
                            maxsources[target] |= {state}
            S = Snew
            step += 1

        endstates = [key for key,val in maxlen.iteritems() if val == max(maxlen.values())]
        self.longestwords = []
        for w in endstates:
            self._backtrace(maxsources, maxlen, w, [])


factors = []

def rec(word, lcs, posw, posl, inmatch, tempstring):
    global factors
    if posw == len(word) and posl != len(lcs):
        return
    if posw != len(word) and posl == len(lcs):
        if inmatch:
            rec(word, lcs, posw + 1, posl, 0, tempstring + [u']'] + [word[posw]])
        else:
            rec(word, lcs, posw + 1, posl, 0, tempstring + [word[posw]])
        return

    if posw == len(word) and posl == len(lcs):
        if inmatch:
            factors.append("".join(tempstring + [u']']))
        else:
            factors.append("".join(tempstring))
        return

    if word[posw] ==  lcs[posl]:
        if inmatch:
            rec(word, lcs, posw + 1, posl + 1, 1, tempstring + [word[posw]])
        else:
            rec(word, lcs, posw + 1, posl + 1, 1, tempstring + [u'['] + [word[posw]])

    if inmatch:
        rec(word, lcs, posw + 1, posl, 0, tempstring + [u']'] + [word[posw]])
    else:
        rec(word, lcs, posw + 1, posl, 0, tempstring + [word[posw]])

def longest_variable(string):
    thislen = 0
    maxlen = 0
    inside = 0
    for s in string:
        if inside and s != u']':
            thislen += 1
        elif s == u']':
            inside = 0
            maxlen = max(thislen, maxlen)
        elif s == u'[':
            inside = 1
            thislen = 0
    return maxlen

def count_infixes(string):
    totalinfixes = 0
    infix = 0
    runninginfixcount = 0
    totalinfixes = 0
    for idx, val in enumerate(string):
        if val == u'[':
            infix = 0
            totalinfixes += runninginfixcount
            runninginfixcount = 0
        elif val != u']' and infix:
            runninginfixcount += 1
        elif val == u']':
            infix = 1
    return totalinfixes


def string_to_varstring(string, vars):
    varpos = 0
    s = []
    idx = 0
    while idx < len(string):
        if string[idx] == u'[':
            if idx != 0:
                s.append(u'+')
            idx += 1
            while string[idx] != u']':
                idx += len(vars[varpos])
                s.append(unicode(varpos+1))
                if idx < len(string) - 1:
                    s.append(u'+')
                varpos += 1
            idx += 1
            continue
        else:
            s.append(string[idx])
            idx += 1

    return u''.join(s)


def lcp(lst):
    """Returns the longest common prefix from a list."""
    if not lst: return ''
    cleanlst = map(lambda x: x.replace(u'[','').replace(u']','') , lst)
    s1 = min(cleanlst)
    s2 = max(cleanlst)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

def firstvarmatch(string, prefix):
    """See if first var is exactly prefix."""
    if string[1:1+len(prefix)] == prefix:
        return True
    else:
        return False


def eval(lcs, c):
    """Input: a list of variable-bracketed strings, the known LCS
       Output: number of variables needed and the variables themselves in a list."""
    allbreaks = []
    for w in c:
        breaks = [0] * len(lcs)
        p = 0
        inside = 0
        for pos in w:
            if pos == u'[':
                inside = 1
            elif pos == u']':
                inside = 0
                breaks[p-1] = 1
            else:
                if inside:
                    p += 1
                
        allbreaks.append(breaks)
    finalbreaks = [0] * len(lcs)
    for br in allbreaks:
        for idx, val in enumerate(br):
            if val == 1:
                finalbreaks[idx] = 1
    
    # Extract vars
    vars = []
    currvar = u''
    for idx, val in enumerate(lcs):
        currvar += lcs[idx]
        if finalbreaks[idx] == 1:
            vars.append(currvar)
            currvar = u''
        
    numvars = sum(finalbreaks)
    return (numvars, vars)

def findfactors(word, lcs):
    """Recursively finds the different ways to place an LCS in a string."""
    global factors
    word = list(word)
    lcs = list(lcs)
    factors = []
    rec(word, lcs, 0, 0, 0, [])
    return factors[:]

# [table, c,variabletable,variablelist,numvars,infixcount]

def vars_to_string(baseform, varlist):
    """Input: baseform, variable list
       Output: string of type '0=baseform,1=var1,2=var2...'"""
    vstr = [u'0=' + baseform]    
    for idx, v in enumerate(varlist):
        vstr.append(unicode(idx+1) + u'=' + v)
    return u",".join(vstr)

def collapse_tables(tables):
    """Input: list of tables
       Output: Strings of collapsed tables."""
    tablestrings = []
    collapsedidx = set() # Store indices to collapsed tables
    for idx, t in enumerate(tables):
        if idx in collapsedidx:
            continue
        varstring = []
        vartable = t[2]
        # Find similar tables
        for idx2, t2 in enumerate(tables):
            if idx2 != idx and vartable == t2[2]:
                varstring.append(vars_to_string(t2[0][0], t2[3]))
                collapsedidx.update({idx2})
        varstring.append(vars_to_string(t[0][0], t[3]))
        rhs = u'#'.join(varstring)
        lhs = u'#'.join(t[2])
        tablestrings.append(u"\t".join([lhs,rhs]))
    return tablestrings


####################################################################

lines = [l.decode('utf-8').strip() for l in sys.stdin]
tables = []
thistable = []
for l in lines:
    if l == u'':
        if len(thistable) > 0:
            tables.append(thistable)
            thistable = []
        else:
            continue
    else:
        thistable.append(l)

tables.append(thistable)

vartables = []        
TABLELIMIT = 16
for table in tables:    
    wg = [wordgraph.wordtograph(x) for x in table]
    result = reduce(lambda x, y: x & y, wg)
    lcss = result.longestwords
    if not lcss:
        vartables.append([[table,table,table,[],0,0]])
        continue

    combos = []
    for lcs in lcss:
        factorlist = [findfactors(w, lcs) for w in table]
        numcombinations = reduce(lambda x, y: x*len(y), factorlist, 1)
        # Filter out factors that can't be handled quickly
        if numcombinations > TABLELIMIT:
            flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]
            lcprefix = lcp(flatten(factorlist))
            factorlist = [[x for x in w if firstvarmatch(x, lcprefix)] for w in factorlist]
            numcombinations = reduce(lambda x, y: x*len(y), factorlist, 1)
            if numcombinations > TABLELIMIT:
                factorlist = [[x for x in w if len(x) == len(min(w, key=len))] for w in factorlist]
                numcombinations = reduce(lambda x, y: x*len(y), factorlist, 1)
                if numcombinations > TABLELIMIT:
                    factorlist = [[x for x in w if count_infixes(x) == count_infixes(min(w, key=lambda x: count_infixes(x)))] for w in factorlist]
                    numcombinations = reduce(lambda x, y: x*len(y), factorlist, 1)
                    if numcombinations > TABLELIMIT:
                        factorlist = [[x for x in w if longest_variable(x) == longest_variable(max(w, key=lambda x: longest_variable(x)))] for w in factorlist]
                        numcombinations = reduce(lambda x, y: x*len(y), factorlist, 1)
                        if numcombinations > TABLELIMIT:

                            min(map(lambda x: x.find('['),w))
                            factorlist = [[x for x in w if x.find(u'[') == min(map(lambda x: x.find('['),w))] for w in factorlist]
                            numcombinations = reduce(lambda x, y: x*len(y), factorlist, 1)
                        
        # Evaluate all combinations of factorizations of LCS
        combinations = itertools.product(*factorlist)
        for c in combinations:
            (numvars, variablelist) = eval(lcs, c)
            infixcount = reduce(lambda x,y: x + count_infixes(y), c, 0)
            variabletable = [string_to_varstring(s, variablelist) for s in c]
            combos.append([table,c,variabletable,variablelist,numvars,infixcount])

    vartables.append(combos)

MODE_STANDARD = 1
MODE_COMPRESS_TABLES = 0

if MODE_STANDARD:
    filteredtables = []
    for t in vartables:
        besttable = min(t, key = lambda s: (s[4],s[5]))
        filteredtables.append(besttable)
    collapsedtables = collapse_tables(filteredtables)
    out = ("\n".join(collapsedtables)).encode('utf-8','replace')
    print out

elif MODE_COMPRESS_TABLES:
    #TODO: Add code to choose tables based on how collapsible they are
    print "x"
