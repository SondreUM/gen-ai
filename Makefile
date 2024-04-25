
OUTPUT_DIR = output
TMP_DIR = $(OUTPUT_DIR)/tmp
DATA_DIR = $(OUTPUT_DIR)/data
KEYS_DIR = src/keys

all: run

install:
	mkdir $(KEYS_DIR)
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@read -p "Enter a GPT key: " key; \
	echo "$$key" > $(KEYS_DIR)/gpt_key.txt
	
activate:
	. venv/bin/activate

run:
	python3 src/processing.py

clean:
	rm -r $(TMP_DIR) $(DATA_DIR)

cleanall: clean
	rm -rf $(TMP_DIR)

PHONY: all install activate run clean cleanall