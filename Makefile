

PYTHON=python3


reduc:
	cp ~/packages/fullcompress/stats_reduction.csv ./
	$(PYTHON) cli.py stats_reduction.csv "#node" density "#aggregation" "#association"

comp:
	cp ~/programs/benchmark_compression/stats/stats ./stats_compression.csv
	$(PYTHON) cli.py stats_compression.csv node density "fc e.r." "pg e.r."

concept_gen:
	$(PYTHON) cli.py ~/programs/pocs/concept_generation/output.csv "context size" "context density" time --select="method=method_sum_1"
	$(PYTHON) cli.py ~/programs/pocs/concept_generation/output.csv "context size" "context density" time --select="method=method_sum_2"
	$(PYTHON) cli.py ~/programs/pocs/concept_generation/output.csv "context size" "context density" time --select="method=method_sum_3"
