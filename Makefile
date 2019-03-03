paper.pdf: paper.tex title.tex bibliography.bib preamble.sty chapters/* figures/* algorithms/* deps/*
	if command -v latexrun 2>/dev/null; then latexrun paper.tex; else latexmk -pdf paper.tex; fi

.PHONY: clean
clean:
	rm -rf latex.out/
	rm -f paper.pdf
