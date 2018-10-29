paper.pdf: paper.tex bibliography.bib preamble.sty llncs.cls
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex
