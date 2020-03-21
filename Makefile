help:
	@echo "    clean"
	@echo "        Remove Python/build artifacts."
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    types"
	@echo "        Check for type errors using pytype."
	@echo "    submission"
	@echo "        Prepare files for submission to GitLab."
	@echo "    test"
	@echo "        Run pytest on tests/."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf .pytype/
	rm -rf .pytest_cache/

formatter:
	black healthqa

submission:
	pytest tests/
	black healthqa
	pytype --keep-going cora

types:
	pytype --keep-going cora

test:
	pytest tests/

