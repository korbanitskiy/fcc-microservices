SHELL = /bin/bash


.PHONY: format
format:
	@ pre-commit run --all-files
