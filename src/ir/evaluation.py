import tp
import numpy as np

path_query='data/query.text'
path_qrels='data/qrels.text'

def read_query() :
    '''
    Read requests from query.text, we only get the .W
    returns request list : request_list
        request_list[i]= words of request numero i
    '''
    res=''
    request_list={}
    with open(path_query, 'r+', encoding='utf-8') as file :
        for lines in file:
            
            if (len(lines)>1) :
                if (lines[0]=='.') & (lines[1]=='I') :
                    id=lines.strip('.I ')
                    id=id.strip()

                    
                if (lines[0]=='.') & (lines[1]=='W'):
                    nex=next(file).strip()
                    while(nex[0]!='.'):
                        res=res+' '+nex
                        nex=next(file).strip()

                    request_list[int(id)]=res
                    res=''
    
    for request in request_list.keys():
        request_list[request]=tp.Stopword_elimination(request_list[request])
        request_list[request]=tp.dict_freq(request_list[request])

    return request_list


def read_qrels():
    '''
    returns pertinent documents for every request
    '''
    pertinent_terms_in_request={}
    init_list=[]
    with open(path_qrels, 'r+', encoding='utf-8') as file :
        for lines in file:
            elements_init= lines.split(' ')
            init_list.append(elements_init)

        id=init_list[0][0]
        temp=[]
        for element in init_list:
            if element[0]==id:
                temp.append(int(element[1]))
            else:
                pertinent_terms_in_request[int(id)]=temp
                id=element[0]
                temp=[]
                temp.append(int(element[1]))
        pertinent_terms_in_request[int(id)]=temp

    return pertinent_terms_in_request
            

def precision(pertinent_docs, selected_docs):
    counter=0 #pertinent_selected_docs
    for pert_doc in pertinent_docs:
        if pert_doc in selected_docs:
            counter+=1
    
    return (counter/len(selected_docs))


def recall(pertinent_docs,selected_docs):
    counter=0 #pertinent_selected_docs
    for pert_doc in pertinent_docs:
        if pert_doc in selected_docs:
            counter+=1
    
    return (counter/len(pertinent_docs))
    

if __name__ == '__main__':
    print(read_query())
