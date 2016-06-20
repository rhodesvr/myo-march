all:	thesis.pdf

%.pdf:	export TEXINPUTS=.:figures:

%.pdf: %.tex bib.bib
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make $<

clean:
	rm *.log *.aux
