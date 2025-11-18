.PHONY: install run test verify

install:
	python -m pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	python -m pytest

verify:
	./scripts/verify.sh
