PYTHON ?= python3
.PHONY: all verify recurrence gatezero clean
all:
	./run_all.sh
verify:
	$(PYTHON) verify_package.py
recurrence:
	$(PYTHON) experiments/direct_recurrence/code/run_recurrence.py --out experiments/direct_recurrence
gatezero:
	@echo "unzip original_inputs and run run_experiment.py under the pinned env (see run_all.sh step 2)"
