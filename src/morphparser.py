import sys, math, paradigm, codecs, getopt

class stringngram:

    def __init__(self, stringset, alphabet = None, order = 2, ngramprior = 0.01):
        """Read a set of strings and create a n-gram model."""
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



def main(argv):

    options, remainder = getopt.gnu_getopt(argv[1:], 'tk:n:p:', ['tables','kbest','ngram','prior'])

    print_tables, kbest, ngramorder, ngramprior = False, 1, 3, 0.01
    for opt, arg in options:
        if opt in ('-t', '--tables'):
            print_tables = True
        elif opt in ('-k', '--kbest'):
            kbest = int(arg)
        elif opt in ('-n', '--ngram'):
            ngramorder = int(arg)
        elif opt in ('-p', '--prior'):
            ngramprior = float(arg)

               
    paradigms = paradigm.load_file(sys.argv[1]) # [(occurrence_count, name, paradigm),...,]
    alphabet = paradigms_to_alphabet(paradigms)

    numexamples = sum(map(lambda x: x.count, paradigms))

    lms = []
    for pindex, p in enumerate(paradigms):
        numvars = (len(p.slots) - 1)/2
        slotmodels  = []
        for v in xrange(0, numvars):
            varinsts = p.slots[v*2+1][1]
            model = stringngram(varinsts, alphabet = alphabet, order = ngramorder, ngramprior = ngramprior)
            slotmodels.append(model)
        lms.append((numvars, slotmodels))

    def eval_vars(matches, lm):
        matchpossibilities = [matches[z] for z in range(1,len(matches),2)] # get every other element
        #print "MPOSS", matchpossibilities
        maxscore = -1000000
        for mp in matchpossibilities:
            #print "MP", mp
            score = 0
            for midx, m in enumerate(mp):
                score += lm[1][midx].evaluate(m)
            if score > maxscore:
                maxscore = score
        return maxscore


    for line in iter(lambda: sys.stdin.readline().decode('utf-8'), ''):
        word = line.strip()
        analyses = []
        for pindex, p in enumerate(paradigms):
            for f in p.forms:
                matching = f.match_vars(word, constrained = False)
                # [(2, ('v', 'enc')), (2, ('ve', 'nc')), (2, ('ven', 'c'))]
                if matching != None:
                    if len(matching) == 0:
                        score = 0
                        analyses.append((p, score, p.name, (len(word), ()), f.msd))
                    else:
                        for m in matching:
                            #score = math.log(p.count/float(numexamples)) + eval_vars(m, lms[pindex])
                            score = eval_vars(m, lms[pindex])
                            analyses.append((p, score, p.name, m, f.msd))

        sortedanalyses = sorted(analyses, key = lambda a: a[1], reverse = True)

        for n in xrange(min(len(sortedanalyses), kbest)):
            msdprint = ','.join([m[0] + '=' + m[1] for m in sortedanalyses[n][4]])
            pout = [str(sortedanalyses[n][1]), sortedanalyses[n][2], str(sortedanalyses[n][3][0]) + ':' + ','.join(sortedanalyses[n][3][1]), msdprint]
            print ('\t'.join(pout)).encode('utf-8')
            if print_tables:
                # Instantiate table
                table = sortedanalyses[n][0](*sortedanalyses[n][3][1])
                for form, msd in table:
                    msdprint = ','.join([m[0] + '=' + m[1] for m in msd])
                    print (form + '\t' + msdprint).encode("utf-8")
            print

if __name__ == "__main__":
    main(sys.argv)
