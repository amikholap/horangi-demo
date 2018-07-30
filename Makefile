start:
	./scripts/start.sh

test:
	DJANGO_SETTINGS_MODULE=demo.settings_test ./manage.py test

PHONY: start test
