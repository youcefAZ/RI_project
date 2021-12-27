"""All the general components of our app are here."""
import math
import copy
import json 
from ir  import utilities,app,boolean_model,vectorial_model,tp,plots
"""
import traceback
import logging
from utilities import *
from tp import * 
from vectorial_model import *
from boolean_model  import *
from evaluation import *
"""
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
    """Create weighted tf-idf, using the formula given in part 3.

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


def multi_test(request_list,idf_list,list_doc,pertinent_list):
    """

    Keyword arguments:
        request_list    -- { "query_number" :  {"word_in_qury":num_of_occurences,"word_i_q":num_oc,...}, ... }
        idf_list        -- { word: {document_it_appears_in : num_occurences_in_this_doc},..} (can be the weighted one)
        list_doc        -- {doc_id:{word:occurence,word2:occ2},doc_id:{word:occurence_in_doc},... }
        pertinent_list  -- { "query_number":[list, of, pertinent,document],...}

    Returns:


    """
    results={}

    threshold_tests={}
    threshold_tests[1]=list(np.arange(1,13,1))
    threshold_tests[2]=list(np.arange(0.1,1,0.1))
    threshold_tests[3]=list(np.arange(0.1,1,0.1))
    threshold_tests[4]=list(np.arange(0.1,1,0.1))
    for i in range(1,5):
        print('TYPE : ',i) # the rsv function 
        for threshold in threshold_tests[i]: # test all the threasholds for that rsv function
            print('THRESHOLD : ', threshold)
            mean_precision=0
            mean_recall=0
            for j in range(1,len(request_list)+1): # test all the requests!
                #print('REQUEST : ',j)
                try :
                    pertinent_docs =pertinent_list[j] 
                except Exception as e:
                    # the exception is made for the request that don't have any pertinent doc
                    # so we can't campute the precision and recall of those
                    print("WARNING: the pertinent list of query number: ",j," doesn't exist,\n \
                            therefore we can't comute percision and recall for them")
                    continue
                rsv=vectorial_model(idf_list,list_doc,request_list[j],i,threshold)
                mean_precision+=precision(pertinent_docs,rsv.keys())
                mean_recall+=recall(pertinent_docs,rsv.keys())
            
            results[threshold]={mean_precision/(len(request_list)-12),mean_recall/len(request_list)}
        output_results(i,results)
        results.clear()


def get_them_all():
    """
    create all the the pkl files that we need if they dont exist.
    """

    pickl_list = ["list_doc.pkl","idf_list.pkl","weighted_idf.pkl", \
       "request_list.pkl","pertinent_list.pkl"]

    if (not utilities.check_pickle("list_doc.pkl")):
        doc=read_data()
        list_doc=tokenization(doc)
        idf_list=idf(list_doc)
        idf_clone = copy.deepcopy(idf_list)
        weighted_idf=idf_ponderation(idf_clone,list_doc)
        request_list=read_query()
        pertinent_list=read_qrels()
    """
    savePkl(idf_list,"idf_list.pkl","pickle/")
    savePkl(list_doc,"list_doc.pkl","pickle/")
    savePkl(pertinent_list,"pertinent_list.pkl","pickle/")
    savePkl(request_list,"request_list.pkl","pickle/")
    savePkl(weighted_idf,"weighted_idf.pkl","pickle/")
    """

    for i in range(len(pickl_list)):
        if (not utilities.check_pickle(pickl_list[i] ) ):#if it doesn"t exist create it!
            #TODO: optimize it's very poorly written
            doc=read_data()
            list_doc=tokenization(doc)
            idf_list=idf(list_doc)
            idf_clone = copy.deepcopy(idf_list)
            weighted_idf=idf_ponderation(idf_clone,list_doc)
            request_list=read_query()
            pertinent_list=read_qrels()
            pickle_objects= [list_doc, idf_list, weighted_idf, \
                request_list, pertinent_list]

            utilities.savePkl(pickle_objects[i],pickl_list[i],"pickle/")


def get_sort_result(results):
    """Get a sorted results dictionnary.
    
    Keyword arguments:
        results     -- dictionnay {doc_num:selected_rsv_func_value_for_doc , ...}

    Returns:
        results dictionnary sorted by values.
    """
    results = sorted(results.items(), key=lambda x:x[1],reverse=True)
    sortdict = dict(results)
    return sortdict



def main():
    get_them_all()
    list_doc=openPkl('list_doc.pkl','pickle/')
    idf_list=openPkl('idf_list.pkl','pickle/')
    weighted_idf=openPkl('weighted_idf.pkl','pickle/')
    
    #print(list_doc)
    #print('----------------\n'*5,print_dico(idf_list))
    #print('----------------\n',print_dico(weighted_idf))
    #print('-----------------\n',boolean_model('goal or parameters',list_doc))

    request_list=read_query()
    pertinent_list=read_qrels()
    
    #print('RESULTAT : ',rsv)
    #print('PERTINENT DOCS : ',pertinent_list[10])
    
    multi_test(request_list,weighted_idf,list_doc,pertinent_list)

if __name__ == '__main__':
    main()
