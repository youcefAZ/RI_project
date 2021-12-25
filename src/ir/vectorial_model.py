import math
"""All the functions related to the vectorial Model."""

def vectorial_model(idf, list_doc, request_list:str, func_sim,threshold) :
    """TODO: implemnt this!

    Keyword arguments:
        idf             --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        liste_doc       --  {doc_id:{word:occurence},doc_id:{word:occurence_in_doc} }  
        threshold       --  threshold used in sim_functions  

    Returns:
        dictionnay {doc_num:{rsv_func:value_of_rsv},..}

    """
   
    req_words_vector =  {}
    results = {}
    for i in range(1,len(list_doc)+1): # parcourir les documents
        # generer vecteur requete 
        for req_term in request_list:
            # check si mot existe dans dictionaire!
            if  req_term in list_doc[str(i)].keys():
                req_words_vector[req_term] = 1

        # here we can call one of the functions to compute rsv
        if func_sim==1:
            res = rsv_produit_interne(idf, str(i) , req_words_vector,threshold)
        elif func_sim==2:
            res = rsv_dice_coef(idf, str(i) , req_words_vector,list_doc,threshold)
        elif func_sim==3:
            res = rsv_cosinus(idf, str(i) , req_words_vector,list_doc,threshold)
        else:
            res = rsv_jaccard(idf, str(i) , req_words_vector,list_doc,threshold)
        
        if res != None:
            results[i]= res
        
        req_words_vector.clear()#clear the list!

    return results


def rsv_produit_interne(idf,doc_num:str,req_words_vector,threshold):
    """Inner product rsv compute.

    Keyword arguments:
        idf                 --  {word: {document_it_appears_in : num_occurences_in_this_doc,..},{},...}   (contains all the words!)
        doc_num             --  document number (or id) 
        req_words_vector    --  {word:1} (containt only words that exists!)

    Returns:
        inner_product rsv.
    """
    res = 0
    for i in req_words_vector.keys(): #parcourir les mots du request seulement qui appartiennent au doc
        w_i_q = req_words_vector[i]

        if (doc_num in idf[i].keys()):
            w_i_j = idf[i][doc_num]
        else:
            w_i_j  = 0
        
        res = res + w_i_j * w_i_q

    if res >= threshold:
        return res
    else :
        return None


def rsv_dice_coef(idf,doc_num:str,req_words_vector,list_doc,threshold):
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

    for i in list_doc[doc_num]: #parcourir les termes du document courant
        w_i_j = idf[i][doc_num]

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0
        res_w_ij2 = res_w_ij2 + w_i_j**2
        res_w_iq2 = res_w_iq2 + w_i_q**2
        res_top = res_top + w_i_j * w_i_q

    res_top = 2 *res_top

    result = res_top / ( res_w_ij2 +res_w_iq2 )
    if result >threshold:
        return result
    
    return None
    


def rsv_cosinus(idf,doc_num:str,req_words_vector, list_doc,threshold):
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

    if len(req_words_vector)==0 :
        return None
    
    for i in list_doc[doc_num]: #parcourir tt les mots du doc
        w_i_j = idf[i][doc_num]

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0
        res_w_ij2 = res_w_ij2 + w_i_j**2
        res_w_iq2 = res_w_iq2 + w_i_q**2
        res_top = res_top + w_i_j * w_i_q

    
    res_down = math.sqrt( res_w_ij2  * res_w_iq2 )
    result = res_top / res_down
    if result >=threshold :
        return result
    else:
        return None
    


def rsv_jaccard(idf,doc_num:str,req_words_vector,list_doc,threshold):
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

    for i in list_doc[doc_num]: #parcourir tt les mots du doc
        w_i_j = idf[i][doc_num]

        if i in req_words_vector:
            w_i_q = req_words_vector[i]
        else:
            w_i_q = 0

        res_top = res_top + w_i_j * w_i_q

        res_w_ij2 = res_w_ij2 + w_i_j**2
        res_w_iq2 = res_w_iq2 + w_i_q**2

    
    res_down = res_w_ij2 + res_w_iq2 - res_top

    result = res_top / res_down
    
    if result>threshold:
        return result
    
    return None
   

