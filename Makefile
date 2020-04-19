PHONY: clean-dir copy-data go

clean-dir:
	rm -rf output
	mkdir output

copy-data:
	cp output/data_sentiment.csv	/Users/michalkollar/Desktop/Coding/Dataviz/movies/assets/
	cp output/data_aggs.csv		/Users/michalkollar/Desktop/Coding/Dataviz/movies/assets/

go:
	make clean-dir

	python3 scraping.py
	python3 analysis.py

	make copy-data