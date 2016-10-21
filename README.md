# Paradigm learning and paradigm prediction

The software collection in this repository is related to a body of
scientific work on paradigm learning and paradigm prediction, of which
the following publication is the latest one. See the reference list
for previous work.

[Forsberg, M; Hulden, M. (2016). Learning Transducer Models for
Morphological Analysis from Example Inflections. In Proceedings of
StatFSM. Association for Computational Linguistics.] (http://anthology.aclweb.org/W16-2405)

## Quick reference

### Paradigm learning: `pextract.py`

#### Description

Extract paradigmatic representations from input inflection tables. See
Section 2 in Forsberg and Hulden (2016) for details.

#### Example

`$ python src/pextract.py < data/es_verb_train.txt > es_verb.p`

### Non-probabilistic morphological analyzers: `morphanalyzer.py`

#### Description

Create a foma-compatible morphological analyzer from a paradigm
file. The analyzer is non-probabilistic.

Options:
* `-o`  recreate original data (all vars must be exactly instantiated as seen in training data)
* `-c`  constrain variables by generalizing (default pvalue = 0.05)
* `-u`  unconstrained (all variables are defined as ?+)
* `-p`  <pvalue>  use <pvalue> together with -c
* `-s`  keep different analyzers separate instead of merging with
priority union (may be necessary for some analyzers)
* `-n`  name of binary foma file to compile to

Any combination of the above may be used. The analyzers are combined
by priority union, e.g. `-o -c -u` would yield an analyzer
`[ Goriginal .P. Gconstrained .P. Gunconstrained ]`.

#### Example

`$ python src/morphanalyzer.py -o -c es_verb.p > es_verb.foma`

### Probabilistic morphological analyzers: `morphparser.py`

#### Description

Create a probabilistic morphological analyzer from a paradigm
file.

Reads one or more whitespace-separated words from STDIN and
returns the most plausible analysis for the set in the format:
`SCORE  NAME_OF_PARADIGM  VARIABLES  WORDFORM1:BASEFORM,MSD#WORDFORM2:BASEFORM,MSD...`

Flags:
* `-k num` print the k best analyses
* `-t`     print the entire table for the best analysis
* `-d`     print debug info
* `-n num` use an nth order ngram model for selecting best paradigm (an n-gram model for variables in the paradigm is used)

#### Example

`$ echo "coger cojo" | python morphparser.py ./../paradigms/spanish_verbs.p -k 1 -t`
