LATEXFILES=motivation.tex
BIBFILES=motivation.aux
.PHONY: default build docs clean test
docs:
	cd descr; \
	pdflatex -interaction=batchmode $(LATEXFILES); \
	bibtex -terse $(BIBFILES); \
	pdflatex -interaction=batchmode $(LATEXFILES); \
	pdflatex -interaction=batchmode $(LATEXFILES)
	cd descr; \
	rm *.aux *.bbl *.blg *.log *.out
