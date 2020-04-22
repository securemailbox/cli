PYTHON3=$(shell which python3)
obj = scmail.py

# just run python for test
runpy:
	pipenv run python

run: $(obj)
	pipenv run python $(obj)

clear:
	rm -rf gnupgkeys/* jskey.asc scmail.conf log
