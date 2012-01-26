networkx-wordnet-ja
===================
WordNet-ja graph generator using NetworkX

Support formats : Image file(.png), GraphViz(.dot), GML(.gml), GraphML(.graphml)  
(Automatically detect the output file extension)


How to use
----------
	Usage: wordnet-ja.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -i FILE, --input=FILE
							Japanese WordNet DB path (default=./wnjpn.db)
	  -o FILE, --output=FILE
							output path (default==./wnjpn.png)
	  -d DPI, --dpi=DPI     dpi(default=100)
	  -l LANG, --lang=LANG  language(eng or jpn, default=both)
	  -r LEVEL, --level=LEVEL
							max recursive level(default=4)
	  -w WORD, --word=WORD  word (e.g. network)
	  -y SYNSET, --synset=SYNSET
							synset (e.g. 01586752-a)


Sample
------
	python wordnet-ja.py --word=network -lang==eng

![screenshot] (https://github.com/stakemura/networkx-wordnet-ja/raw/master/sample.png)

License
------
public domain
