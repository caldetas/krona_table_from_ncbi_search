# krona_table_from_ncbi_search.py

make a Krona chart from a txt file with read counts and search term.  
The taxids and desired ranks are fetched with Entrez  
  
some search terms give obviously wrong results and have to be deleted/handled manually  
for example: Bacteria, Terrabacteria

## MANUAL

    krona_table_from_ncbi_search.py reads_and_searchterms.txt

  

the txt file should have the following format:

    16627690	Cladonia
    1000000	Asterochloris
    488826	leotiomyceta
    337129	Alphaproteobacteria
    262506	Parmeliaceae
    197793	Proteobacteria
    151892	Rhizobiales
    135949	Methylobacterium


The krona creator can be downloaded here:  
[a link](https://github.com/marbl/Krona)  
  
The .txt file can then be imported(linux)  
    ktImportText output.txt

