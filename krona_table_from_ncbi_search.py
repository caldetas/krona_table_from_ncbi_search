#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:34:57 2018

@author: hannes
"""

import sys
import getopt


#instructions
form='krona_table_from_ncbi_search.py <reads_and_searchterms.txt>' 


def main(argv):
    try:
       opts, args = getopt.getopt(argv,"h",["covavg1=f1","covavg2=f2"])
    except getopt.GetoptError:
       print ('{}'.format(form))
       print('hey')
       sys.exit()
    for opt, arg in opts:
       if opt == '-h' or opt == '-help' or opt == '--help':
          print ('{}'.format(form))
          sys.exit()
    print(argv[-1])
    

    import pandas as pd


    def tax_id(lyst):
        from Bio import Entrez

        def get_tax_id(species):
            """to get data from ncbi taxomomy, we need to have the taxid. we can
            get that by passing the species name to esearch, which will return
            the tax id"""
            species = species.replace(' ', "+").strip()
            search = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
            record = Entrez.read(search)
            if species != 'Not assigned' or 'root' and record['IdList'] != []:
                return record['IdList'][0]
      
        def get_tax_data(taxid):
            """once we have the taxid, we can fetch the record"""
            search = Entrez.efetch(id = taxid, db = "taxonomy", retmode = "xml")
            return Entrez.read(search)
        
        Entrez.email = "somemail@smth.ch"
        if not Entrez.email:
            print("you must add your email address")
            sys.exit(2)
        species_list = ['Terrabacteria group', 'Helicobacter pylori 26695', 'Thermotoga maritima MSB8', 'Deinococcus radiodurans R1', 'Treponema pallidum subsp. pallidum str. Nichols', 'Aquifex aeolicus VF5', 'Archaeoglobus fulgidus DSM 4304']
        species_list = lyst
        taxid_list = [] # Initiate the lists to store the data to be parsed in
        data_list = []
        lineage_list = []
        
        print('parsing taxonomic data...') # message declaring the parser has begun
        
        for species in species_list:
            print ('\t'+species) # progress messages
        
            taxid = get_tax_id(species) # Apply your functions
            data = get_tax_data(taxid)
            if 'LineageEx' in data[0]:
                lineage = {d['Rank']:d['ScientificName'] for d in data[0]['LineageEx'] if d['Rank'] in ['phylum']}
            else:
                print('ERROR:', species, 'not found in dictionary')
            taxid_list.append(taxid) # Append the data to lists already initiated
            data_list.append(data)
            lineage_list.append(lineage)
        
        print('complete!')
        print()
        print('TaxId\'s:')
        print(taxid_list)
        print()
    
    
        from ete3 import NCBITaxa
        
        ncbi = NCBITaxa()
        
        def get_desired_ranks(taxid, desired_ranks):
            lineage = ncbi.get_lineage(taxid)   
            names = ncbi.get_taxid_translator(lineage)
            lineage2ranks = ncbi.get_rank(names)
            ranks2lineage = dict((rank,taxid) for (taxid, rank) in lineage2ranks.items())
            return{'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}
        
        if __name__ == '__main__':
            taxids = taxid_list
            desired_ranks = ['superkingdom', 'kingdom', 'class', 'family'] #, 'genus']  #['kingdom', 'phylum', 'class', 'order', 'superfamily', 'family', 'subfamily', 'tribe', 'subtribe', 'genus', 'subgenus', 'species', 'subspecies']
            results = list()
            for taxid in taxids:
                results.append(list())
                results[-1].append(str(taxid))
                ranks = get_desired_ranks(taxid, desired_ranks)
                for key, rank in ranks.items():
                    if rank != '<not present>':
                        results[-1].append(list(ncbi.get_taxid_translator([rank]).values())[0])
                    else:
                        results[-1].append(rank)
        
            #generate the header
            header = ['reads', 'Original search', 'Original_query_taxid']
            header.extend(desired_ranks)
            out = []
#            print('\t'.join(header))
            out.append(header)
        
            #print the results            
            for result, reads, term in zip(results, values, lyst):
                cnt = 0
                for i in result:
                    if 'bacter' in i or 'Bacter' in i:
                        result[2] = 'Bacteria'
                    if i == '<not present>':
                        result[cnt] = ''
                    cnt += 1
                        

                temp = [reads, term]
                temp.extend(result)
                

                out.append(temp)
        out = pd.DataFrame(out)
        return out 
    txt = open(argv[-1])
    lyst = []
    values = []
    for line in txt:
        line = line.strip().split()
        lyst.append(line[1])
        values.append(int(line[0]))
    df = tax_id(lyst)
    headers = df.iloc[0]
    df  = pd.DataFrame(df.values[1:], columns=headers)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
#    df = df.loc[df['superkingdom'] == 'bacteria']
    print()
    print()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df) 
    df.iloc[:,[0,3,4,5,6]].to_csv('output.txt', sep='\t', index = None, header = None)
#    df = df.loc[df['superkingdom'] == 'bacteria']
    print()
    print()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df) 
    sys.exit()
    
if __name__ == "__main__":
    main(sys.argv[1:])
