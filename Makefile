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
cparadigm:
	python src/cparadigm.py -c paradigms/shared1_de_noun_train.p
cparadigmi:
	python src/cparadigm.py -i paradigms/shared1_de_noun_train.p
shared:
	python src/convert_shared_data.py data/sigmorphon2016/data/arabic-task1-train V   > data/shared1_ar_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/arabic-task1-train N   > data/shared1_ar_noun_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/arabic-task1-train ADJ > data/shared1_ar_adj_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/georgian-task1-train V   > data/shared1_ka_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/georgian-task1-train N   > data/shared1_ka_noun_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/georgian-task1-train ADJ > data/shared1_ka_adj_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/navajo-task1-train V   > data/shared1_nv_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/navajo-task1-train N   > data/shared1_nv_noun_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/spanish-task1-train V   > data/shared1_es_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/spanish-task1-train N   > data/shared1_es_noun_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/spanish-task1-train ADJ > data/shared1_es_adj_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/finnish-task1-train V   > data/shared1_fi_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/finnish-task1-train N   > data/shared1_fi_noun_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/finnish-task1-train ADJ > data/shared1_fi_adj_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/german-task1-train V   > data/shared1_de_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/german-task1-train N   > data/shared1_de_noun_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/german-task1-train ADJ > data/shared1_de_adj_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/russian-task1-train V   > data/shared1_ru_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/russian-task1-train N   > data/shared1_ru_noun_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/russian-task1-train ADJ > data/shared1_ru_adj_train.txt

	python src/convert_shared_data.py data/sigmorphon2016/data/turkish-task1-train V   > data/shared1_tr_verb_train.txt
	python src/convert_shared_data.py data/sigmorphon2016/data/turkish-task1-train N   > data/shared1_tr_noun_train.txt

pshared:
	python src/pextract.py < data/shared1_ar_verb_train.txt > paradigms/shared1_ar_verb_train.p 
	python src/pextract.py < data/shared1_ar_noun_train.txt > paradigms/shared1_ar_noun_train.p 
	python src/pextract.py < data/shared1_ar_adj_train.txt > paradigms/shared1_ar_adj_train.p 

	python src/pextract.py < data/shared1_ka_verb_train.txt > paradigms/shared1_ka_verb_train.p 
	python src/pextract.py < data/shared1_ka_noun_train.txt > paradigms/shared1_ka_noun_train.p 
	python src/pextract.py < data/shared1_ka_adj_train.txt > paradigms/shared1_ka_adj_train.p 

	python src/pextract.py < data/shared1_nv_verb_train.txt > paradigms/shared1_nv_verb_train.p 
	python src/pextract.py < data/shared1_nv_noun_train.txt > paradigms/shared1_nv_noun_train.p 

	python src/pextract.py < data/shared1_es_verb_train.txt > paradigms/shared1_es_verb_train.p 
	python src/pextract.py < data/shared1_es_noun_train.txt > paradigms/shared1_es_noun_train.p 
	python src/pextract.py < data/shared1_es_adj_train.txt > paradigms/shared1_es_adj_train.p 

	python src/pextract.py < data/shared1_fi_verb_train.txt > paradigms/shared1_fi_verb_train.p 
	python src/pextract.py < data/shared1_fi_noun_train.txt > paradigms/shared1_fi_noun_train.p 
	python src/pextract.py < data/shared1_fi_adj_train.txt > paradigms/shared1_fi_adj_train.p 

	python src/pextract.py < data/shared1_de_verb_train.txt > paradigms/shared1_de_verb_train.p 
	python src/pextract.py < data/shared1_de_noun_train.txt > paradigms/shared1_de_noun_train.p 
	python src/pextract.py < data/shared1_de_adj_train.txt > paradigms/shared1_de_adj_train.p 

	python src/pextract.py < data/shared1_ru_verb_train.txt > paradigms/shared1_ru_verb_train.p
	python src/pextract.py < data/shared1_ru_noun_train.txt > paradigms/shared1_ru_noun_train.p
	python src/pextract.py < data/shared1_ru_adj_train.txt > paradigms/shared1_ru_adj_train.p

	python src/pextract.py < data/shared1_tr_verb_train.txt > paradigms/shared1_tr_verb_train.p
	python src/pextract.py < data/shared1_tr_noun_train.txt > paradigms/shared1_tr_noun_train.p

cpshared:
	python src/cparadigm.py -c paradigms/shared1_ar_verb_train.p > paradigms/shared1_ar_verb_train.cp 
	python src/cparadigm.py -c paradigms/shared1_ar_noun_train.p > paradigms/shared1_ar_noun_train.cp 
	python src/cparadigm.py -c paradigms/shared1_ar_adj_train.p > paradigms/shared1_ar_adj_train.cp 

	python src/cparadigm.py -c paradigms/shared1_ka_verb_train.p > paradigms/shared1_ka_verb_train.cp 
	python src/cparadigm.py -c paradigms/shared1_ka_noun_train.p > paradigms/shared1_ka_noun_train.cp 
	python src/cparadigm.py -c paradigms/shared1_ka_adj_train.p > paradigms/shared1_ka_adj_train.cp 

	python src/cparadigm.py -c paradigms/shared1_nv_verb_train.p > paradigms/shared1_nv_verb_train.cp 
	python src/cparadigm.py -c paradigms/shared1_nv_noun_train.p > paradigms/shared1_nv_noun_train.cp 

	python src/cparadigm.py -c paradigms/shared1_es_verb_train.p > paradigms/shared1_es_verb_train.cp 
	python src/cparadigm.py -c paradigms/shared1_es_noun_train.p > paradigms/shared1_es_noun_train.cp 
	python src/cparadigm.py -c paradigms/shared1_es_adj_train.p > paradigms/shared1_es_adj_train.cp 

	python src/cparadigm.py -c paradigms/shared1_fi_verb_train.p > paradigms/shared1_fi_verb_train.cp 
	python src/cparadigm.py -c paradigms/shared1_fi_noun_train.p > paradigms/shared1_fi_noun_train.cp 
	python src/cparadigm.py -c paradigms/shared1_fi_adj_train.p > paradigms/shared1_fi_adj_train.cp 

	python src/cparadigm.py -c paradigms/shared1_de_verb_train.p > paradigms/shared1_de_verb_train.cp 
	python src/cparadigm.py -c paradigms/shared1_de_noun_train.p > paradigms/shared1_de_noun_train.cp 
	python src/cparadigm.py -c paradigms/shared1_de_adj_train.p > paradigms/shared1_de_adj_train.cp 

	python src/cparadigm.py -c paradigms/shared1_ru_verb_train.p > paradigms/shared1_ru_verb_train.cp
	python src/cparadigm.py -c paradigms/shared1_ru_noun_train.p > paradigms/shared1_ru_noun_train.cp
	python src/cparadigm.py -c paradigms/shared1_ru_adj_train.p > paradigms/shared1_ru_adj_train.cp

	python src/cparadigm.py -c paradigms/shared1_tr_verb_train.p > paradigms/shared1_tr_verb_train.cp
	python src/cparadigm.py -c paradigms/shared1_tr_noun_train.p > paradigms/shared1_tr_noun_train.cp


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
