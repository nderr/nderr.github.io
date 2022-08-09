all: index.md assets/files/cv.pdf

index.md: info.yaml index.md.in write_index.py
	./write_index.py index.md.in

assets/files/cv.pdf: cv/cv.tex.in info.yaml cv/write_cv.py
	cd cv; ./write_cv.py cv.tex.in; pdflatex cv.tex; cp cv.pdf ../assets/files/cv.pdf
