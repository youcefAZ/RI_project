import tp
import math
import copy
import json 

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


def replace_logical_by_mathematical_operators(request):
    """

    Keyword arguments:
        request         -- the request with replaced words with 1 and 0. exp: (0 or 1)

    Returns:
        the result of the logical operation!
    
    Note:
        i don't think we took care of the () and the priorities!
        and i think we should!
        TODO: take care of the priorities!
    """
    request = request.replace("and", "*").replace("or", "+")
    partitioned_request = list(request.partition("not"))
    for i in range(0, len(partitioned_request)-1):
        if partitioned_request[i] == "not":
            partitioned_request[i] = "int(not"
            partitioned_request[i+1] = partitioned_request[i+1] + ")"
    
    temp_request = ""
    for i in range(0, len(partitioned_request)):
        temp_request += partitioned_request[i]
    return temp_request


def rsv_boolean(logical_oper):
    """
        take a request of this form :(True or False (not True))
        and evaluate it! 

    Returns:
        True or False
    """

    return eval(logical_oper)


def create_boolean_request(list_boolean):
    """Take a dictionnary of the request with True or False when the term
        is in the document or not, and 0 when it's a logical operator (or, and, not, "(", ")" )
        And transform it into an str logical formula  that can be evaluated!

    Keyword arguments:
        lilst_boolean       -- example: {"word":"True", "(":0 , "not":0, "zrodiya":Fals",...}

    Returns:
        str: the logical formula
    """
    logical_str_req = ""
    for i in list_boolean:

        if (list_boolean[i] == 0 ):
            logical_str_req = logical_str_req + " " + str(i)

        else:
            logical_str_req = logical_str_req+" "+list_boolean[i]
    
    return logical_str_req


def boolean_model(request:str,list_doc):
    """Handle request using the boolean model, return list of pertinent docs.

    Keyword arguments:
        request     --  the boolean request
        list_doc    -- {doc_id:{word:occurence,word2:occ2},doc_id:{word:occurence_in_doc},... }
        
    Returns:
        list of pertinent documents.

    Note:
        The function have been tested on the same request as youcef's(boolean_model0) and had the same result.
    """
    request = request.lower()
    operator_list={'and','or','not','(',')'} # les operation possible dans le modéle booleen
    request_list = request.split() # list des mot de la requete
    termes_in_doc = {} 
    pertinent_docs = []  

    for i in range(1,len(list_doc)+1): # parcourir les documents
        for term in request_list: # parcourir liste des mot de la requete
            if term not in operator_list and term in list_doc[str(i)].keys():
                termes_in_doc[term] = "True"

            elif term in operator_list:
                termes_in_doc[term] = 0

            else: 
                termes_in_doc[term] = "False"

        str_logic = create_boolean_request(termes_in_doc)
        if rsv_boolean(str_logic):
            #add to pertinent 
            pertinent_docs.append(i)

        termes_in_doc.clear()

    return pertinent_docs


def vectorial_model(idf, list_doc, request:str) :
    """TODO: implemnt this!

    Keyword arguments:
        idf             --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        liste_doc       --  {doc_id:{word:occurence},doc_id:{word:occurence_in_doc} }  

    Returns:
        dictionnay {doc_num:{rsv_func:value_of_rsv},..}

    """
    request_list = request.split()
   
    req_words_vector =  {}
    results = {}
    for i in range(1,len(list_doc)+1): # parcourir les documents
        # generer vecteur requete 
        for req_term in request_list:
            # check si mot existe dans dictionaire!
            if  req_term in list_doc[str(i)].keys():
                req_words_vector[req_term] = 1

        # here we can call one of the functions to compute rsv
        res = rsv_produit_interne(idf, str(i) , req_words_vector)

        if res != 0:
            tmp_dic = {"inr_prod":res}
            results[i]= tmp_dic

        req_words_vector.clear()#clear the list!

    return results



def rsv_produit_interne(idf,doc_num:str,req_words_vector):
    """Inner product rsv compute.

    Keyword arguments:
        idf                 --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        doc_num             --  document number (or id) 
        req_words_vector    --  {word:1} (containt only words that exists!)

    Returns:
        inner_product rsv.
    """
    res = 0
    for i in idf: #parcourir tt les mots
        if (doc_num in idf[i].keys()):
            w_i_j = idf[i][doc_num]
        else:
            w_i_j  = 0

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0
        res = res + w_i_j * w_i_q

    return res


def rsv_dice_coef(idf,doc_num:str,req_words_vector):
    """dice coef rsv compute.

    Keyword arguments:
        idf                 --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        doc_num             --  document number (or id) 
        req_words_vector    --  {word:1} (containt only words that exists!)

    Returns:
        dice coef rsv.
    """

    res_top   = 0
    res_w_ij2 = 0
    res_w_iq2 = 0

    for i in idf: #parcourir tt les mots
        if (doc_num in idf[i].keys()):
            w_i_j = idf[i][doc_num]
        else:
            w_i_j  = 0

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0
        res_w_ij2 = res_w_ij2 + w_i_j**2
        res_w_iq2 = res_w_iq2 + w_i_q**2
        res_top = res_top + w_i_j * w_i_q

    res_top = 2 *res_top

    result = res_top / ( res_w_ij2 +res_w_iq2 )

    return result


def rsv_cosinus(idf,doc_num:str,req_words_vector):
    """cosinus rsv compute.

    Keyword arguments:
        idf                 --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        doc_num             --  document number (or id) 
        req_words_vector    --  {word:1} (containt only words that exists!)

    Returns:
        cosinus rsv.
    """

    res_top   = 0
    res_w_ij2 = 0
    res_w_iq2 = 0

    for i in idf: #parcourir tt les mots
        if (doc_num in idf[i].keys()):
            w_i_j = idf[i][doc_num]
        else:
            w_i_j  = 0

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0
        res_w_ij2 = res_w_ij2 + w_i_j**2
        res_w_iq2 = res_w_iq2 + w_i_q**2
        res_top = res_top + w_i_j * w_i_q

    
    res_down = math.sqrt( res_w_ij2  * res_w_iq2 )
    result = res_top / res_down
    return result


def rsv_jaccard(idf,doc_num:str,req_words_vector):
    """jaccard rsv compute.

    Keyword arguments:
        idf                 --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        doc_num             --  document number (or id) 
        req_words_vector    --  {word:1} (containt only words that exists!)

    Returns:
        jaccard rsv.
    """
    res_top   = 0
    res_w_ij2 = 0
    res_w_iq2 = 0

    for i in idf: #parcourir tt les mots
        if (doc_num in idf[i].keys()):
            w_i_j = idf[i][doc_num]
        else:
            w_i_j  = 0

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0

        res_top = res_top + w_i_j * w_i_q

        res_w_ij2 = res_w_ij2 + w_i_j**2
        res_w_iq2 = res_w_iq2 + w_i_q**2

    
    res_down = res_w_ij2 + res_w_iq2 - res_top

    result = res_top / res_down
    return result


def boolean_model0(request:str,list_doc):
    """Youcef's implementatino of the boolean model.

    Keyword arguments:
        request     -- the boolean request!
        list_doc    -- {doc_id:{word:occurence,word2:occ2},doc_id:{word:occurence_in_doc},... }
        
    Returns:
        list of pertinent document
    """
    request = request.lower()
    operator_list={'and','or','not','(',')'}
    request_list = request.split() 
    termes_in_doc = {} 
    pertinent_docs = [] 

    for i in range(1,len(list_doc)+1): # parcourir les documents
        for term in request_list: # parcourir liste des mot de la requete
            if term not in operator_list and term in list_doc[str(i)].keys():
                termes_in_doc[term] = 1
            else:
                termes_in_doc[term] = 0

        # term in doc contient donc {terme:0,terme2:1,...} appartenance terme 

        temp_request = request
        for term in termes_in_doc.keys():
            if term not in operator_list:
                # on remplace le mot par sa valeur (0 ou 1)
                temp_request = temp_request.replace(term, str(termes_in_doc[term])) 
        
        if eval(replace_logical_by_mathematical_operators(temp_request)):
            pertinent_docs.append(i)

        termes_in_doc.clear()
    return pertinent_docs


def print_dico(dico):
    """Print any dictionary in a json way(more beautiful manner)."""
    return json.dumps(dico, indent=4, sort_keys=True)


def main():
    doc=read_data()
    list_doc=tokenization(doc)
    idf_list=idf(list_doc)
    idf_clone = copy.deepcopy(idf_list)
    weighted_idf=idf_ponderation(idf_clone,list_doc)

    print(list_doc)
    print('----------------\n'*5,print_dico(idf_list))
    print('----------------\n',print_dico(weighted_idf))
    print('-----------------\n',boolean_model('goal or parameters',list_doc))
    

if __name__ == '__main__':
    main()

