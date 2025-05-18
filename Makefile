PLUGIN_NAME = Dict2Anki-by-dream
ZIP_NAME = $(PLUGIN_NAME).zip
IGNORE_PATTERNS = \
    "*/.git/*" \
    "*.md" \
    "*.pyc" \
    "__pycache__/*" \
    "package/" \
    "*/tests/*" \
    ".DS_Store" \
    "Makefile"

.PHONY: all clean package

all: package

package:
	@echo "Packaging $(PLUGIN_NAME) → $(ZIP_NAME)"
	zip -r "package/$(ZIP_NAME)" . package/ -x $(IGNORE_PATTERNS)

clean:
	rm -f "$(ZIP_NAME)"
