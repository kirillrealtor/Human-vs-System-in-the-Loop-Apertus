.PHONY: run run-local

# Forward command to track_2b/
run:
	$(MAKE) -C track_2b run

run-local:
	$(MAKE) -C track_2b run-local
