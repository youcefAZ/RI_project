import tp
import math
import copy
import json 
from boolean_model import *
from vectorial_model import *
from utilities import *
from evaluation import *

stopwordsfile='stopwords/stopwords_eng.txt'
datapath='data/cacm.all'
stopword_list=open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

def read_data() :
    """Read the data and put them somewhere, we just care about I,T,W
        from file, makes dictionarry with doc_id as its key, and
        title+ resume as its content. 

    Returns
     dic : {document_number: 
                        {title:'title', resume:'resume'},
                    document_number: 
                        {title:'title', resume:'resume'},
                        etc etc,..
                    }
    """
    docs={}
    with open(datapath, 'r+', encoding='utf-8') as file:
        res=''
        title=''
        for lines in file :
            if (lines[0]=='.') & (lines[1]=='I') :
                id=lines.strip('.I ')
                id=id.strip()

            if (lines[0]=='.') & (lines[1]=='T'):
                nex=next(file).strip()
                while nex[0]!='.' :
                    title=title+' '+nex
                    nex=next(file).strip()
            
                if (nex[0]=='.') & (nex[1]=='W'):
                    nex=next(file).strip()
                    while nex[0]!='.' :
                        res=res+' '+nex
                        nex=next(file).strip()
                
            if (lines[0]=='.') & (lines[1]=='X'):
                docs[id]={'title':title,'resume':res}
                res=''
                title=''
    return docs


def tokenization(docs) :
    """Take the docs structure and just create a new one, with
        mixing together the T and W (title and resume).
        i don't know if it's a good thing or no but that's how we were 
        told to do!

    Keyword arguments:
        docs -- the dictionary returned by read_data()
    
    Returns:
        {doc_id:{word:occurence},doc_id:{word:occurence_in_doc} }

    Note:

    """
    detailed_doc={}
    for key in docs:
        title=docs[key]['title']
        resume=docs[key]['resume']
        title = tp.Stopword_elimination(title)
        resume = tp.Stopword_elimination(resume)
        content=title+resume
        content=tp.dict_freq(content)

        detailed_doc[key]=content
    return detailed_doc
        

def idf(data):
    """Create the inverse document freequency IDF.

    Keyword arguments:
        data -- the dictionary returned by tokenization { doc_id:{word:occurence},doc_id:{word:occurence_in_doc} }
    
    Returns:
        {
         word: {document_it_appears_in : num_occurences_in_this_doc},
         word: {document_it_appears_in : num_occurences_in_this_doc}   
        }

    """
    idf_list={}
    for d in data :
        for element in data[d]:
            if element not in idf_list :
                doc_fr={}
                for d2 in data :
                    if element in data[d2]:
                        doc_fr[d2]=data[d2][element]
                idf_list[element]=doc_fr
    return idf_list
                

def get_doc_details(data_doc,di):
    """TODO:understand why this funcition exists
    """
    return data_doc[di]


def get_term_details(data_term,term):
    """TODO: understand why this function exists!
    """
    return data_term[term]


def max_freq(dj):
    """Compute maximum occurence in the dj dictionnary.

    Keyword arguments:
        dj      -- {word:occurence,word2:occ2}
    
    Returns:
        the maximum occurence in the dj dictionnary
    """
    all_values = dj.values()
    max_value = max(all_values)
    return max_value


def idf_ponderation(idf_list,list_doc):
    """Create weighted td-idf, using the formula given in part 3.

    Keyword arguments:
        idf_list    -- { word: {document_it_appears_in : num_occurences_in_this_doc},..}
        list_doc    -- {doc_id:{word:occurence,word2:occ2},doc_id:{word:occurence_in_doc},... }
        
    Returns:
        { word: {document_it_appears_in : weight_of_word_in_doc},..}
    """
    n = len(list_doc)
    for term in idf_list:
        ni = len (idf_list[term])
        # ni : nombre de document contenant le terme i

        for doc in idf_list[term]:#pour chaque document contenant le mot
            # idf_list[term][doc]: is the frequence (ti, dj)

            max = max_freq(list_doc[str(doc)])

            idf_list[term][doc]=( idf_list[term][doc] / max) * math.log( (n / ni) +1 , 10)
    
    return idf_list



def main():
    doc=read_data()
    list_doc=tokenization(doc)
    idf_list=idf(list_doc)
    #idf_clone = copy.deepcopy(idf_list)
    #weighted_idf=idf_ponderation(idf_clone,list_doc)

    #print(list_doc)
    #print('----------------\n'*5,print_dico(idf_list))
    #print('----------------\n',print_dico(weighted_idf))
    #print('-----------------\n',boolean_model('goal or parameters',list_doc))

    request_list=read_query()
    pertinent_list=read_qrels()
    rsv=vectorial_model(idf_list,list_doc,request_list[1],1)
    
    print('RESULTAT : ',rsv)
    print('PERTINENT DOCS : ',pertinent_list[1])
    print('PRECISION : ',precision(pertinent_list[1],rsv.keys()))
    print('RECALL : ',recall(pertinent_list[1],rsv.keys()))
    #for request 1, best threshold is > 11

if __name__ == '__main__':
    main()

