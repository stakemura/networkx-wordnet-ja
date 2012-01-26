networkx-wordnet-ja
===================
WordNet-ja graph generator using NetworkX

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
wordnet-ja.py -w network -l eng
(sample.png)

Licene
------
public domain