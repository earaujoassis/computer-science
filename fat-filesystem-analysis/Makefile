LATEXFILES=
BIBFILES=
.PHONY: default docs clean
docs:
	cd article; \
	pdflatex -interaction=batchmode article.tex; \
	bibtex -terse article.aux; \
	pdflatex -interaction=batchmode article.tex; \
	pdflatex -interaction=batchmode article.tex; \
	rm *.aux *.bbl *.blg *.log *.out
