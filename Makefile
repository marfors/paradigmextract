all:
	mkdir -p output
	cd src;python cexp.py ../paradigms/es_verb_train_dev.p ../data/es_verb_test.txt > ../output/es_verb.txt
	cd src;python cexp.py ../paradigms/de_verb_train_dev.p ../data/de_verb_test.txt > ../output/de_verb.txt
	cd src;python cexp.py ../paradigms/fi_verb_train_dev.p ../data/fi_verb_test.txt > ../output/fi_verb.txt
	cd src;python cexp.py ../paradigms/de_noun_train_dev.p ../data/de_noun_test.txt > ../output/de_noun.txt
	cd src;python cexp.py ../paradigms/fi_nounadj_train_dev.p ../data/fi_nounadj_test.txt > ../output/fi_nounadj.txt
	tail -n 2 output/*
