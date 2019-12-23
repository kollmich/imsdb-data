PHONY: clean-dir copy-data go

clean-dir:
	rm -rf output
	mkdir output

copy-data:
	cp output/data_sentiment.txt	/Users/michalkollar/Desktop/Coding/Dataviz/imsdb-web/src/assets/data/

go:
	make clean-dir

	python3 scraping.py
	python3 analysis.py

	make copy-data