

PYTHON=python3


reduc:
	cp ~/sofa/fullcompress/stats_reduction.csv ./
	$(PYTHON) cli.py stats_reduction.csv "#node" density "#aggregation" "#association"

comp:
	cp ~/Python/benchmark_compression/stats/stats ./stats_compression.csv
	$(PYTHON) cli.py stats_compression.csv node density "fc e.r." "pg e.r."
