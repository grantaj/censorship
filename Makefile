TEX_DIR := latex
TEX_MAIN := main.tex
PDF := $(TEX_DIR)/main.pdf
PANDOC := pandoc
SRC := $(TEX_DIR)/$(TEX_MAIN)
BIB := $(TEX_DIR)/main.bib
CSL := chicago-notes-bibliography.csl
TPL := template.html
FILTER := ignore-spacing.lua
CSS := style.css

BASENAME := censorship
OUTDIR := docs
HTML := $(OUTDIR)/index.html
VERSION := 1.0
RELEASE_DIR := docs/releases
RELEASE_NAME := $(BASENAME)-$(VERSION).pdf

.PHONY: all pdf html release clean

all: pdf

pdf:
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=$(TEX_DIR) $(TEX_DIR)/$(TEX_MAIN)

html: $(HTML)

$(HTML): $(SRC) $(BIB) $(CSL) $(TPL) $(CSS) $(FILTER)
	@mkdir -p $(OUTDIR)/assets
	cp $(CSS) $(OUTDIR)/style.css
	cd $(OUTDIR) && $(PANDOC) ../$(SRC) \
	  --standalone \
	  --mathjax \
	  --citeproc \
	  --bibliography=../$(BIB) \
	  --csl=../$(CSL) \
	  --lua-filter=../$(FILTER) \
	  --metadata=suppress-bibliography=true \
	  --template=../$(TPL) \
	  --resource-path=..:../figures \
	  --extract-media=assets \
	  -o index.html
	@echo "Built -> $(HTML)"

release: pdf
	@test -n "$(VERSION)" || (echo "VERSION is required, e.g. make release VERSION=0.3" && exit 1)
	mkdir -p $(RELEASE_DIR)
	cp $(PDF) $(RELEASE_DIR)/$(RELEASE_NAME)

clean:
	latexmk -C -output-directory=$(TEX_DIR)
	rm -f $(PDF)
