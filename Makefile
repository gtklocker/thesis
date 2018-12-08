paper.pdf: paper.tex bibliography.bib preamble.sty chapters/* figures/* algorithms/* deps/*
	if command -v latexrun 2>/dev/null; then latexrun paper.tex; else latexmk -pdf; fi

.PHONY: clean
clean:
	git clean -Xdf
