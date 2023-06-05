export EMERALD_OUTPUT_DIR=./var

send:
	poetry run python src/send.py "$(c)"
