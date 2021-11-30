import tp

stopwordsfile='stopwords/stopwords_eng.txt'
datapath='data/cacm.all'
stopword_list=open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

#from file, makes dictionarry with doc_id as its key, and
#title+ resume as its content
def read_data() :
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

    file.close()
    return docs


#cleans list_doc
def tokenization(docs) :
    detailed_doc={}
    for key in docs:
        title=doc[key]['title']
        resume=doc[key]['resume']
        
        title = tp.Stopword_elimination(title)
        resume = tp.Stopword_elimination(resume)
        content=title+resume
        content=tp.dict_freq(content)

        detailed_doc[key]=content
        
    return detailed_doc
        

#list of terms, contains list of docs it appears in + its frequency
def idf(data):
    idf_list={}
    for d in data :
        for element in data[d]:
            if element not in idf_list :
                doc_fr={}
                for d2 in data :
                    if element in data[d2]:
                        doc_fr[d2]={'freq':data[d2][element]}
                idf_list[element]={'doc':doc_fr}
    return idf_list
                

def get_doc_details(data_doc,di):
    return data_doc[di]

def get_term_details(data_term,term):
    return data_term[term]



doc=read_data()
list_doc=tokenization(doc)
idf_list=idf(list_doc)

print(get_term_details(idf_list,'isolating'))
print(get_doc_details(list_doc,'3000'))

