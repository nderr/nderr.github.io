all: index.md assets/files/cv.pdf
#all: cv/out.pdf

ENV=.conda
PYTHON=$(shell pwd)/$(ENV)/bin/python

$(PYTHON): environment.yml
	if [ -e $(ENV) ]; then \
		mamba env remove -p ./$(ENV); \
	fi
	mamba env create -p ./$(ENV) -f environment.yml

python: $(PYTHON)

info: info.yaml resume/info_res.yaml

index.md: info.yaml index.md.in write_index.py
	./write_index.py index.md.in

resume: assets/files/resume.pdf python info

assets/files/resume.pdf: resume/*tex.j2
	@cd resume && \
	$(PYTHON) mk_resume_tex.py > resume.tex && \
	xelatex resume.tex && \
	mv resume.pdf ../assets/files/resume.pdf

cv/out.pdf: cv/*tex.j2 info.yaml jinja.py
	$(PYTHON) jinja.py > cv/out.tex
	cd cv && pdflatex out.tex


assets/files/cv.pdf: cv/cv.tex.in info.yaml cv/write_cv.py
	cd cv && ./write_cv.py cv.tex.in && pdflatex cv.tex && pdflatex cv.tex && cp cv.pdf ../assets/files/cv.pdf
