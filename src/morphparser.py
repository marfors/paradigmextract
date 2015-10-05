# Do morphological analysis based on learned paradigms
# Reads one or more whitespace-separated words from STDIN and
# returns the most plausible analysis for the set in the format:
# SCORE  NAME_OF_PARADIGM  VARIABLES  WORDFORM1:BASEFORM,MSD#WORDFORM2:BASEFORM,MSD...

# Flags:
# -k num   print the k best analyses
# -t       print the entire table for the best analysis
# -d       print debug info
# -n num   use an nth order ngram model for selecting best paradigm
#          (an n-gram model for variables in the paradigm is used)

# Example:
# echo "coger cojo" | python morphparser.py ./../paradigms/spanish_verbs.p -k 1 -t
#
# Output:

# -11.231539838 coger (1=co) coger:coger,type=infinitive#cojo:coger,person=1st,number=singular,tense=present,mood=indicative
# *coger*	type=infinitive
# cogiendo	type=participle,tense=present
# cogido	type=participle,tense=past
# *cojo*	person=1st,number=singular,tense=present,mood=indicative
# coges	person=2nd,number=singular,tense=present,mood=indicative
# coge	person=3rd,number=singular,tense=present,mood=indicative
# ...

import sys, math, paradigm, codecs, getopt

class stringngram:

    def __init__(self, stringset, alphabet = None, order = 2, ngramprior = 0.01):
        """Read a set of strings and create an n-gram model."""
        self.stringset = [u'#'*(order-1) + s + u'#' for s in stringset]
        self.alphabet = {char for s in self.stringset for char in s}
        self.order = order
        self.ngramprior = ngramprior
        if alphabet:
            self.alphabet |= alphabet
        ngrams = [x for word in self.stringset for x in self._letter_ngrams(word, order)]
        self.ngramcounts = {}
        # Collect counts for n-grams and n-1 grams (mgrams)
        for ngram in ngrams:
            self.ngramcounts[ngram] = self.ngramcounts.get(ngram, 0) + 1
        mgrams = [x for word in self.stringset for x in self._letter_ngrams(word, order-1)]
        for mgram in mgrams:
            self.ngramcounts[mgram] = self.ngramcounts.get(mgram, 0) + 1

    def evaluate(self, string):
        s = u'#'*(self.order-1) + string + u'#'
        return sum(self._getprob(x) for x in self._letter_ngrams(s, self.order))

    def _getprob(self, ngram):
        numerator = self.ngramcounts.get(ngram, 0) + self.ngramprior
        denominator = self.ngramcounts.get(ngram[:-1], 0) + len(self.alphabet) * self.ngramprior
        return math.log(numerator/float(denominator))
                                
    def _letter_ngrams(self, word, n):
        return [''.join(x) for x in zip(*[word[i:] for i in range(n)])]


def paradigms_to_alphabet(paradigms):
    """Extracts all used symbols from an iterable of paradigms."""
    alphabet = set()
    for paradigm in paradigms:
          for idx, (is_var, slot) in enumerate(paradigm.slots):
                for word in slot:
                    alphabet |= set(word)
    return alphabet - {'_'}

def eval_vars(matches, lm):
    return sum(lm[1][midx].evaluate(m) for midx, m in enumerate(matches))

def eval_multiple_entries(p, words):
    """Returns a set of consistent variable assigment to all words."""
    wmatches = []
    for w in words:
        wmatch = set()
        for m in filter(lambda x: x != None, p.match(w, constrained = False)):
            if m == []:
                m = [(0,())] # Add dummy to show match is exact without vars
            for submatch in m:
                if len(submatch) > 0:
                    wmatch.add(submatch[1])
        wmatches.append(wmatch)
    consistentvars = reduce(lambda x,y: x & y, wmatches)
    return consistentvars

    
def main(argv):

    options, remainder = getopt.gnu_getopt(argv[1:], 'tk:n:p:dr:', ['tables','kbest','ngram','prior','debug','pprior'])

    print_tables, kbest, ngramorder, ngramprior, debug, pprior = False, 1, 3, 0.01, False, 1.0
    for opt, arg in options:
        if opt in ('-t', '--tables'):
            print_tables = True
        elif opt in ('-k', '--kbest'):
            kbest = int(arg)
        elif opt in ('-n', '--ngram'):
            ngramorder = int(arg)
        elif opt in ('-p', '--prior'):
            ngramprior = float(arg)
        elif opt in ('-d', '--debug'):
            debug = True
        elif opt in ('-d', '--debug'):
            debug = True
        elif opt in ('-r', '--pprior'):
            pprior = float(arg)
               
    paradigms = paradigm.load_file(sys.argv[1]) # [(occurrence_count, name, paradigm),...,]
    alphabet = paradigms_to_alphabet(paradigms)

    numexamples = sum(map(lambda x: x.count, paradigms))

    lms = []
    # Learn n-gram LM for each variable
    for pindex, p in enumerate(paradigms):
        numvars = (len(p.slots) - 1)/2
        slotmodels  = []
        for v in xrange(0, numvars):
            varinsts = p.slots[v*2+1][1]
            model = stringngram(varinsts, alphabet = alphabet, order = ngramorder, ngramprior = ngramprior)
            slotmodels.append(model)
        lms.append((numvars, slotmodels))

            
    for line in iter(lambda: sys.stdin.readline().decode('utf-8'), ''):
        words = line.strip().split()
        if len(words) == 0:
            continue
        
        # Quick filter out most paradigms
        fittingparadigms = [(pindex, p) for pindex, p in enumerate(paradigms) if all(p.fits_paradigm(w, constrained = False) for w in words)]
        fittingparadigms = filter(lambda p: eval_multiple_entries(p[1], words), fittingparadigms)
        
        if debug:
            print "Plausible paradigms:"
            for pnum, p in fittingparadigms:
                print pnum, p.name

        analyses = []
        # Calculate score for each possible variable assignment
        for pindex, p in fittingparadigms:
            prior = math.log(p.count/float(numexamples))
            vars = eval_multiple_entries(p, words) # All possible instantiations
            if len(vars) == 0:
                # Word matches
                score = prior
                analyses.append((score, p, ()))
            else:
                for v in vars:
                    score = prior * pprior + len(words) * eval_vars(v, lms[pindex])
                    #score = len(words) * eval_vars(v, lms[pindex])
                    analyses.append((score, p, v))

        analyses.sort(reverse = True, key = lambda x: x[0])

        # Print all analyses + optionally a table        
        for aindex, (score, p, v) in enumerate(analyses):
            if aindex >= kbest:
                break
            wordformlist = []
            varstring = '(' + ','.join([str(feat) + '=' + val for feat,val in zip(range(1,len(v)+1), v)]) + ')'
            table = p(*v)          # Instantiate table with vars from analysis
            baseform = table[0][0]
            matchtable = [(form, msd) for form, msd in table if form in words]
            wordformlist = [form +':' + baseform + ',' + ','.join([m[0] + '=' + m[1] for m in msd]) for form, msd in matchtable]                    
            print (unicode(score) + ' ' + p.name + ' ' + varstring + ' ' + '#'.join(wordformlist)).encode("utf-8")
            if print_tables:
                for form, msd in table:
                    if form in words:
                        form = "*" + form + "*"
                    msdprint = ','.join([m[0] + '=' + m[1] for m in msd])
                    print (form + '\t' + msdprint).encode("utf-8")

        print
                    

if __name__ == "__main__":
    main(sys.argv)
