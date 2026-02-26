# Pulvermacher – Foundation of Nature
# Makefile: build German and English PDFs

PDFLATEX = pdflatex -interaction=nonstopmode

.PHONY: all german english images clean

all: german english

# ── German PDF ──────────────────────────────────────────────────
german: main.pdf

main.pdf: main.tex Tensor_der_Realitaeten.png Energie_flucht.png \
          Atome_beschreibung.png Neutron_entwicklung.png \
          Superposition.png Materie.png Gravitation.png Zeit.png
	$(PDFLATEX) main.tex
	$(PDFLATEX) main.tex

# ── English PDF ─────────────────────────────────────────────────
english: main_en.pdf

main_en.pdf: main_en.tex Tensor_of_Realities_en.png Superposition_en.png \
             Matter_en.png Gravitation_en.png Time_en.png \
             Energy_Escape_en.png Atomic_Structure_en.png \
             Neutron_Development_en.png
	$(PDFLATEX) main_en.tex
	$(PDFLATEX) main_en.tex

# ── Regenerate English diagram images ───────────────────────────
images:
	python3 /tmp/gen_en_images.py

# ── Clean build artefacts ────────────────────────────────────────
clean:
	rm -f *.aux *.log *.out *.toc *.synctex.gz
