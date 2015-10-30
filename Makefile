.PHONY: venv
venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	touch venv/bin/activate

.PHONY: clean
clean: venv
	for _kill_path in $$(find . -type f -name "*.pyc"); do rm -f $$_kill_path; done
	for _kill_path in $$(find . -name "__pycache__"); do rm -rf $$_kill_path; done

.PHONY: deps
deps: venv
	. venv/bin/activate; pip install -r requirements.txt
