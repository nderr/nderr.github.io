all: index.md

index.md: info.yaml index.md.in write_index.py
	./write_index.py index.md.in
