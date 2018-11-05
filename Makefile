paper.pdf: paper.tex bibliography.bib preamble.sty
	latexmk -pdf

.PHONY: clean
clean:
	git clean -Xdf
