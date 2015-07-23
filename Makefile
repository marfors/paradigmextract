all:
	python src/pextract.py < icelandic/icelandic1.txt > paradigms/icelandic1.p
	python src/pextract.py < icelandic/icelandic2.txt > paradigms/icelandic2.p
	python src/pextract.py < icelandic/icelandic3.txt > paradigms/icelandic3.p
	python src/pextract.py < icelandic/icelandic4.txt > paradigms/icelandic4.p
p:
	cd src;python paradigm.py

