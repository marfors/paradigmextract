PYTHONPATH=$PYTHONPATH:./src
exp:
	cd src; python mexp.py de > ../output/de_morph.txt
	cd src; python mexp.py de_noun > ../output/de_noun_morph.txt
	cd src; python mexp.py de_verb > ../output/de_verb_morph.txt
	cd src; python mexp.py es > ../output/es_morph.txt
	cd src; python mexp.py fi > ../output/fi_morph.txt
	cd src; python mexp.py fi_noun > ../output/fi_noun_morph.txt
	cd src; python mexp.py fi_verb > ../output/fi_verb_morph.txt

slots:
	cd src; python paradigm.py -s ../paradigms/german_nouns.p > ../output/german_nouns_slots.txt
	cd src; python paradigm.py -s ../paradigms/german_verbs.p > ../output/german_verbs_slots.txt
	cd src; python paradigm.py -s ../paradigms/finnish_nounadj.p > ../output/finnish_nounadj_slots.txt
	cd src; python paradigm.py -s ../paradigms/finnish_verbs.p > ../output/finnish_verbs_slots.txt
	cd src; python paradigm.py -s ../paradigms/spanish_verbs.p > ../output/spanish_verbs_slots.txt

.PRECIOUS: morph/%.foma morph/%.foma.bin

morph: $(patsubst paradigms/%.p,morph/%.foma.bin,$(wildcard paradigms/*.p))

morph/%.foma.bin: morph/%.foma
	cd morph; foma -f $(notdir $<)

morph/%.foma: paradigms/%.p
	mkdir -p morph ; python src/morphanalyzer.py -o -c -u -s -n $(notdir $@.bin) $< > $@
holes:
	cd src; python hole.py
htest:
	python src/pextract.py < data/de_noun_h_train_dev.txt > paradigms/de_noun_h_train_dev.p
	python src/paradigm.py -p paradigms/de_noun_h_train_dev.p
clean:
	rm -f morph/*.foma morph/*.bin

#dev:
#	mkdir -p output
#	cd src;python cexp.py ../paradigms/es_verb_train.p ../data/es_verb_dev.txt > ../output/es_verb.txt
#	cd src;python cexp.py ../paradigms/de_verb_train.p ../data/de_verb_dev.txt > ../output/de_verb.txt
#	cd src;python cexp.py ../paradigms/fi_verb_train.p ../data/fi_verb_dev.txt > ../output/fi_verb.txt
#	cd src;python cexp.py ../paradigms/de_noun_train.p ../data/de_noun_dev.txt > ../output/de_noun.txt
#	cd src;python cexp.py ../paradigms/fi_nounadj_train.p ../data/fi_nounadj_dev.txt > ../output/fi_nounadj.txt
#	tail -n 3 output/*
#test:
#	mkdir -p output
#	cd src;python cexp.py ../paradigms/es_verb_train_dev.p ../data/es_verb_test.txt > ../output/es_verb.txt
#	cd src;python cexp.py ../paradigms/de_verb_train_dev.p ../data/de_verb_test.txt > ../output/de_verb.txt
#	cd src;python cexp.py ../paradigms/fi_verb_train_dev.p ../data/fi_verb_test.txt > ../output/fi_verb.txt
#	cd src;python cexp.py ../paradigms/de_noun_train_dev.p ../data/de_noun_test.txt > ../output/de_noun.txt
#	cd src;python cexp.py ../paradigms/fi_nounadj_train_dev.p ../data/fi_nounadj_test.txt > ../output/fi_nounadj.txt
#	tail -n 3 output/*
