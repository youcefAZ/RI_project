"""All the functions related to the Boolean Model."""
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
    """Take a list  of the request with True or False when the term
        is in the document or not, and 0 when it's a logical operator (or, and, not, "(", ")" )
        And transform it into an str logical formula  that can be evaluated!

    Keyword arguments:
        lilst_boolean       -- list of tuples example: [("word":"True"), ( "(" , 0) ), ("not", 0), ("zrodiya","False"),...]

    Returns:
        str: the logical formula
    """
    logical_str_req = ""
    for i in list_boolean:

        if (i[1] == 0 ):
            logical_str_req = logical_str_req + " " + str(i[0])

        else:
            logical_str_req = logical_str_req+" "+ str(i[1])
    
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
        TODO-middle prio-: take care of non boolean requests!
    """
    request = request.lower()
    operator_list={'and','or','not','(',')'} # les operation possible dans le modéle booleen
    request_list = request.split() # list des mot de la requete
    termes_in_doc = [] 
    pertinent_docs = []  

    for i in range(1,len(list_doc)+1): # parcourir les documents
        for term in request_list: # parcourir liste des mot de la requete
            if term not in operator_list and term in list_doc[str(i)].keys():
                termes_in_doc.append( (term,"True") ) 

            elif term in operator_list:
                # the error is that, it's the or doesnt print twice because it's a dictionary!
                termes_in_doc.append ( (term, 0) )

            else: 
                termes_in_doc.append( (term , "False") )
        
        str_logic = create_boolean_request(termes_in_doc)
        if rsv_boolean(str_logic):
            #add to pertinent 
            pertinent_docs.append(i)

        termes_in_doc.clear()

    return pertinent_docs


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

def speed_test():
    """ just a function to debug the boolean model fast"""
    #from utilities import *
    list_doc = openPkl("list_doc.pkl","pickle/")
    request="something or anything or ibm"
    a = boolean_model(request, list_doc)
    print(a)
