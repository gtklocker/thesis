paper.pdf: paper.tex bibliography.bib preamble.sty chapters/* figures/* algorithms/* deps/*
	command -v latexrun 2>/dev/null && latexrun paper.tex || latexmk -pdf

.PHONY: clean
clean:
	git clean -Xdf
