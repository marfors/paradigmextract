class mregex:

    """Simple re.findall replacement that returns all possible matches -
       not just the leftmost-longest match.
       Only handles (.+) and c constructs (c being an arbitrary character).
       Expressions are automatically anchored in the head and the tail,
       i.e. the regexes behave as if they began with ^ and ended with $.

       Example usage:
       >>> from regexmatcher import mregex
       >>> m = mregex('(.+)a(.+)as')
       >>> m.findall('bananas')
       [('b', 'nan'), ('ban', 'n')]
    """
    def __init__(self, regex):
        self.regex = regex
        self.regexlen = len(regex)
        self.text = ''
        self.textlen = 0
        self.matches = []
        
    def findall(self, text):
        strindex = 0
        regindex = 0
        self.text = text
        self.textlen = len(text)
        self.results = []
        self.matched = 0
        self.match(strindex, regindex, [])
        if self.matched:
            return [tuple(self.text[i:j] for i,j in r) for r in self.results]
        return None
    
    def match(self, strindex, regindex, groups):
        # Are we at end of regex _and_ text?
        if strindex == self.textlen and regindex == self.regexlen:
            self.matched = 1
            if groups:
                self.results.append(groups)
            return
        # Jump out if only regex or text is consumed
        if strindex == self.textlen or regindex == self.regexlen:
            return
        # Match (.+)-construct
        if self.regex[regindex:regindex+4] == '(.+)':
            for i in range(strindex + 1, self.textlen + 1):
                self.match(i, regindex + 4, groups + [(strindex, i)])
        # Normal match (one character)
        else: 
            if self.text[strindex] == self.regex[regindex]:
                self.match(strindex + 1, regindex + 1, groups)
        return
